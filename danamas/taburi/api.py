import frappe
import requests

from frappe.utils import today,add_to_date
from datetime import datetime # from python std library
from frappe.utils import money_in_words
from frappe.utils import validate_phone_number
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count
from pypika.terms import Case

@frappe.whitelist()
def createEstatement():
    #before_30_days = add_to_date(today(), days=-30, as_string=True)
    start_date = add_to_date(today(), days=-30, as_string=True)
    end_date = add_to_date(today(), days=-1, as_string=True)

    get_nasabah = frappe.db.get_list('Customers',
        fields=['name', 'full_name'],
        order_by='name asc'
    )
    
    for rows in get_nasabah:
        doc = frappe.new_doc('EStatement')
        doc.customers = rows.name
        doc.start_date = start_date
        doc.end_date = end_date
        
        get_transaksi = frappe.db.get_list('Transaction',
            filters=[
                ["customers","=",rows.name],
                ['transaction_date', 'between', [start_date, end_date]],
            ],
            fields=['transaction_date', 'notes','ao_name','debit','credit'],
        )
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
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        
    return get_transaksi

@frappe.whitelist()
def createEstatementNotificationWA():
    start_date = add_to_date(today(), days=-30, as_string=True)
    end_date = add_to_date(today(), days=-1, as_string=True)

    getstatement = frappe.db.get_list('EStatement',
        filters=[
            ['start_date',"=", start_date],
            ['end_date',"=" ,end_date],
            ['status_pengriman',"=", "Belum Dikirim"],
        ],
        fields=['name','nama_nasabah', 'saldo'],
    )
    for rows in getstatement:
        customers = frappe.db.get_value('Customers', rows.customers)
        
        url = "https://starsender.online/api/sendText"

        payload={
            'tujuan': rows.phone_number,
            'message': f"Halo *Bpk/Ibu {rows.nama_nasabah},*\nTerimakasih telah menabung di *Danamas*. dan memilih Produk *TABURI* sebagai *Sarana anda untuk Meraih Masa Depan.* \n*Saat ini saldo anda* sudah *Terkumpul sejumlah Rp.{rows.saldo}* ( {money_in_words(rows.saldo,'IDR')} )\n*TABUNGAN TANPA BIAYA ADMIN*\nUntuk Info lebih lanjut serta permintaan *Penyetoran/Penarikan*, silahkan hubungi nomor berikut :  0821-1071-2188 *SYAHRIL*\nTingkatkan terus jumlah saldo tabungan anda untuk mendapatkan return s/d 5% PA"
        }
        files=[

        ]
        headers = {
            'apikey': '19c4018fb8e6802e6df74964e67e7026f3ee61c9'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        message_id = response.json()
        
        while True:
            #getStatusMessage
        
            urlMessage = "	https://starsender.online/api/getMessage"
            payloadMessage ={
                'message_id': message_id['data']['message_id']
            }
            
            headersMessage  = {
                'apikey': '19c4018fb8e6802e6df74964e67e7026f3ee61c9'
            }

            responGetStatusMessage = requests.request("POST", urlMessage , headers=headersMessage, data=payloadMessage)
            getStatus = responGetStatusMessage.json()
            if (getStatus['data'][0]['status'] == 'terkirim'):
                updatedoc = frappe.get_doc('EStatement',rows.name)
                updatedoc.status_pengriman = 'Sudah Dikirim'
                updatedoc.save( ignore_permissions=True )
                frappe.db.commit()
                break

    return getstatement
