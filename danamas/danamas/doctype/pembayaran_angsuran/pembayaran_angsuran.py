# Copyright (c) 2022, mjs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now

class PembayaranAngsuran(Document):
	def after_insert(self):
		if(self.kelebihan_pembayaran > 0 ):
			doc = frappe.new_doc('Simpanan Sementara')
			doc.nasabah = self.nasabah
			doc.tanggal = self.tanggal_pembayaran
			doc.nominal_rp = self.kelebihan_pembayaran
			doc.aplikasi =  self.aplikasi_number
			doc.debit_kredit = 'D'
			doc.insert()
		#if(self.saldo_simpanan > 0 ):
		if self.saldo_simpanan is not None:
			doc = frappe.new_doc('Simpanan Sementara')
			doc.nasabah = self.nasabah
			doc.tanggal = self.tanggal_pembayaran
			doc.nominal_rp = self.saldo_simpanan
			doc.aplikasi =  self.aplikasi_number
			doc.debit_kredit = 'K'
			doc.insert()

@frappe.whitelist()		
def getsaldonasabahsimpanansementara(nasabah):
	datas = frappe.db.sql(
            f"""
            select 
				SUM(CASE WHEN t.debit_kredit = 'D'  THEN t.nominal_rp ELSE 0 END) as debit,
				SUM(CASE WHEN t.debit_kredit = 'K' THEN t.nominal_rp ELSE 0 END) as kredit,
				SUM( IF( t.debit_kredit =  'D', t.nominal_rp, -t.nominal_rp ) ) as saldo
				from `tabSimpanan Sementara` t
				where t.nasabah = "{nasabah}"
            """,as_dict=True)
	return datas[0].saldo

@frappe.whitelist()		
def tanggalcicilan(aplikasi):
	ex = aplikasi.split('|')
	datas = frappe.db.sql(
            f"""
			select
				ap.tanggal_tagihan,
				ap.idx as cicilan_ke
				from `tabAplikasi` a
				left join `tabList Angsuran Pinjaman` ap on a.name = ap.parent
				where a.name = "{ex[0]}" and ap.idx = "{ex[1]}"
            """,as_dict=True)
	return datas[0]