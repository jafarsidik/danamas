
import frappe
from frappe.utils import today,add_to_date
from datetime import datetime # from python std library

@frappe.whitelist()
def runners():
    before_30_days = add_to_date(today(), days=-30, as_string=True)

    get_nasabah = frappe.db.get_list('Customers',
        fields=['name', 'full_name'],
        order_by='name asc'
    )
    
    for rows in get_nasabah:
        doc = frappe.new_doc('EStatement')
        doc.customers = rows.name
        doc.start_date = before_30_days
        doc.end_date = today()
        
        get_transaksi = frappe.db.get_list('Transaction',
            filters=[
                ["customers","=",rows.name],
                ['transaction_date', 'between', [before_30_days, today()]],
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
        doc.saldo = debit - credit

        doc.save(ignore_permissions=True)
        frappe.db.commit()
    return get_transaksi
