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

@frappe.whitelist()
def createEstatement():
    list_data = []
    #before_30_days = add_to_date(today(), days=-30, as_string=True)
    start_date = add_to_date(today(), days=-32, as_string=True)
    end_date = add_to_date(today(), days=-2, as_string=True)

    get_nasabah = frappe.db.get_list('Customers',
        fields=['name', 'full_name','phone_number'],
        order_by='name asc'
    )
    for i, rows in enumerate(get_nasabah):
       
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
        doc.insert()
        #pengiriman Wa No Production 
        # sendText(rows.phone_number,rows.full_name,data_total[0].grand_total)
        # sendAttachFile(doc.name,rows.phone_number)

        sendText(doc.name,"087771859551",rows.full_name,data_total[0].grand_total)
        # #sendAttachFile(doc.name,"082213137001")
        # updatedoc = frappe.get_doc('EStatement',doc.name)
        # updatedoc.status_pengriman = 'Sudah Dikirim'
        # updatedoc.save( ignore_permissions=True )
    #return list_data
    #return get_transaksi

def sendText(docname, phone_number, full_name, total_saldo):
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

def sendAttachFile(docname,phone_number):
    url = "https://starsender.online/api/sendFiles"
    url_file = get_url()+"/api/method/danamas.taburi.api.download_pdf?doctype=EStatement&name="+docname+"&format=E-State"
    
    payload={
        'tujuan': phone_number,
        'message': "attach",
        'file' : url_file
    }
    files=[

    ]
    headers = {
        'apikey': '19c4018fb8e6802e6df74964e67e7026f3ee61c9'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    message_id = response.json()
    return response.json()

@frappe.whitelist(allow_guest=True)
def download_pdf(doctype, name, format=None, doc=None, no_letterhead=0):
 	html = frappe.get_print(doctype, name, format, doc=doc, no_letterhead=no_letterhead)
 	frappe.local.response.filename = "{name}.pdf".format(name=name.replace(" ", "-").replace("/", "-"))
 	frappe.local.response.filecontent = get_pdf(html)
 	frappe.local.response.type = "download"

@frappe.whitelist(allow_guest=True)
def testKirim():
    url = "https://starsender.online/api/sendText"
    urlfiles = get_url()+"/api/method/danamas.taburi.api.download_pdf?doctype=EStatement&name=TH-0011-0822-0022&format=E-State"
    payload={
        'tujuan': "087771859551",
        'message': f"Halo *Bpk/Ibu Jafar,*\nTerimakasih telah menabung di *Danamas*. dan memilih Produk *TABURI* sebagai *Sarana anda untuk Meraih Masa Depan.* \n*Saat ini saldo anda* sudah *Terkumpul sejumlah Rp.* ( ,'IDR') )\n*TABUNGAN TANPA BIAYA ADMIN*\nUntuk Info lebih lanjut serta permintaan *Penyetoran/Penarikan*, silahkan hubungi nomor berikut :  0821-1071-2188 *SYAHRIL*\nTingkatkan terus jumlah saldo tabungan anda untuk mendapatkan return s/d 5% PA \n dan silahkan download E-Statement nya Disini  "+urlfiles,
        'file': urlfiles
    }
    files=[

    ]
    headers = {
        'apikey': '19c4018fb8e6802e6df74964e67e7026f3ee61c9'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    message_id = response.json()
    updatedoc = frappe.get_doc('EStatement','TH-0232-0722-19274')
    updatedoc.status_pengriman = 'Sudah Dikirim'
    updatedoc.save( ignore_permissions=True )