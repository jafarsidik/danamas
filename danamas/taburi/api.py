import frappe
import requests
import json

from frappe import _
from frappe import publish_progress
from frappe.utils import today,add_to_date
from datetime import datetime # from python std library
from frappe.utils import money_in_words, get_url,validate_phone_number

from frappe.query_builder import DocType
from frappe.query_builder.functions import Count
from pypika.terms import Case
#from frappe.core.doctype.file.file import create_new_folder
from frappe.utils.file_manager import save_file
from frappe.utils.pdf import get_pdf
from frappe.utils.print_format import download_pdf
from frappe.model.document import Document


def createEstatement():
    list_data = []
    #before_30_days = add_to_date(today(), days=-30, as_string=True)
    start_date = add_to_date(today(), days=-30, as_string=True)
    end_date = add_to_date(today(), days=-1, as_string=True)

    get_nasabah = frappe.db.get_list('Customers',
        fields=['name', 'full_name','phone_number'],
        order_by='name asc'
    )
   
    for rows in get_nasabah:
       
        #create EStatement
        doc = frappe.new_doc('EStatement')
        doc.customers = rows.name
        doc.start_date = start_date
        doc.end_date = end_date
        
        get_transaksi = frappe.db.sql(
            f"""
            select 
                t.transaction_date,
                t.notes,
                t.ao_name,
                t.debit,
                t.credit,
                t.customers
                from tabTransaction t
                WHERE t.customers = "{rows.name}"
                and t.transaction_date >= "{start_date}"
                and t.transaction_date <= "{end_date}" 
            """,as_dict=True)
       
        debit = 0
        credit = 0
       
        for details in get_transaksi:
            doc.append("detail_transaksi", {
                "tanggal": details.transaction_date,
                "keterangan": details.notes,
                "pic": details.ao_name,
                "debit": details.debit,
                "credit":details.credit
            })
            debit += details.debit
            credit += details.credit
        
        doc.total_debit = debit
        doc.total_credit = credit
        doc.saldo_transaksi = debit - credit

        data_total = frappe.db.sql(
            f"""
            SELECT 
                sum(debit) as debit,
                sum(credit) as credit,
                sum(debit - credit) as grand_total
                FROM tabTransaction
                where customers = "{rows.name}"
            """,as_dict=True)
        doc.total_saldo = data_total[0].grand_total
        
        x = doc.insert()
        
        #create Append Notif WA
        docwa = frappe.new_doc('WA Blash Estatement Notif')
        url_file = f"""{get_url()}/api/method/danamas.taburi.api.download_pdf?doctype=EStatement&name={doc.name}&format=E-State"""
        docwa.nasabah = rows.name
        docwa.estatement = x.name
        docwa.no_hp = rows.phone_number
        docwa.total = data_total[0].grand_total
        docwa.start_date = start_date
        docwa.end_date = end_date
        docwa.link_download = url_file
        docwa.redaksi = f"""Halo *Bpk/Ibu {rows.full_name},*\nTerimakasih telah menabung di *Danamas*. dan memilih Produk *TABURI* sebagai *Sarana anda untuk Meraih Masa Depan.* \n*Saat ini saldo anda* sudah *Terkumpul sejumlah Rp.{data_total[0].grand_total}* \n*TABUNGAN TANPA BIAYA ADMIN*\n Untuk Info lebih lanjut serta permintaan *Penyetoran/Penarikan*, silahkan hubungi nomor berikut :  0822-2278-2668 *HASLINDA*\nTingkatkan terus jumlah saldo tabungan anda untuk mendapatkan return s/d 5% PA\n\n\nSilahkan download bukti E-Statement dengan mengklik link di bawah ini:\n{url_file}"""
        docwa.insert()
   

@frappe.whitelist(allow_guest=True)
def download_pdf(doctype, name, format=None, doc=None, no_letterhead=0):
    htmlvar = frappe.get_print(doctype, name, format, doc=doc, no_letterhead=no_letterhead)
    frappe.local.response.filename = "{name}.pdf".format(name=name.replace(" ", "-").replace("/", "-"))
    frappe.local.response.filecontent = get_pdf(htmlvar)
    frappe.local.response.type = "download"

@frappe.whitelist()
def sendWA(**kwargs):
    args = frappe._dict(kwargs)
    url = "https://starsender.online/api/sendText"
    getWA = frappe.get_doc('WA Blash Estatement Notif',args.docname)

    #production
    headers = { 'apikey': '19c4018fb8e6802e6df74964e67e7026f3ee61c9' }
    payload = { 'tujuan': getWA.no_hp,'message': getWA.redaksi}
    #development
    #headers = { 'apikey': '52527f0d29a2b60c55ef7374fe9f57b700ed10ff' }
    #payload = { 'tujuan': '087771859551','message': getWA.redaksi}

    requests.request("POST", url, headers=headers, data=payload)
    progress = ( ( int(args.key) / int(args.count) ) * 100 ) 
    frappe.publish_progress(progress, title="Proses Pengiriman Notifikasi Whatsapp",description = 'Proses Pengiriman '+str(progress)+' %')
        
    getWA.status_pengiriman = "Sudah Dikirim"
    getWA.save()
    res = [progress,int(args.key),int(args.count)]
    return res

def sendTextDMI(docname, phone_number, full_name, total_saldo):
    url = "https://starsender.online/api/sendText"
    url_file = get_url()+"/api/method/danamas.taburi.api.download_pdf?doctype=EStatement&name="+docname+"&format=E-State"
    
    payload={
        'tujuan': phone_number,
        'message': f"""
            Halo *Bpk/Ibu {full_name},*\nTerimakasih telah menabung di *Danamas*. dan memilih Produk *TABURI* sebagai *Sarana anda untuk Meraih Masa Depan.* \n*Saat ini saldo anda* sudah *Terkumpul sejumlah Rp.{total_saldo}* \n*TABUNGAN TANPA BIAYA ADMIN*\n Untuk Info lebih lanjut serta permintaan *Penyetoran/Penarikan*, silahkan hubungi nomor berikut :  0822-2278-2668 *HASLINDA*\nTingkatkan terus jumlah saldo tabungan anda untuk mendapatkan return s/d 5% PA\n\n\nSilahkan download bukti E-Statement dengan mengklik link di bawah ini:\n{url_file}
            """
    }
    headers = {
        'apikey': '19c4018fb8e6802e6df74964e67e7026f3ee61c9'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def sendTextIDMS(docname, phone_number, full_name, total_saldo):
    url = "https://starsender.online/api/sendText"
    url_file = get_url()+"/api/method/danamas.taburi.api.download_pdf?doctype=EStatement&name="+docname+"&format=E-State"
    
    payload={
        'tujuan': "087771859551",
        'message': f"""
            Halo *Bpk/Ibu {full_name},*\nTerimakasih telah menabung di *Danamas*. dan memilih Produk *TABURI* sebagai *Sarana anda untuk Meraih Masa Depan.* \n*Saat ini saldo anda* sudah *Terkumpul sejumlah Rp.{total_saldo}* \n*TABUNGAN TANPA BIAYA ADMIN*\n Untuk Info lebih lanjut serta permintaan *Penyetoran/Penarikan*, silahkan hubungi nomor berikut :  0822-2278-2668 *HASLINDA*\nTingkatkan terus jumlah saldo tabungan anda untuk mendapatkan return s/d 5% PA\n\n\nSilahkan download bukti E-Statement dengan mengklik link di bawah ini:\n{url_file}
            """
    }
    headers = {
        'apikey': '52527f0d29a2b60c55ef7374fe9f57b700ed10ff'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()