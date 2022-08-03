# Copyright (c) 2022, mjs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

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
		

