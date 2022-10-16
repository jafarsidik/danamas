# Copyright (c) 2022, mjs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Investasi(Document):
	def after_insert(self):
		doc = frappe.new_doc('Estatement Investasi')
		doc.cif = self.nasabah
		doc.no_bilyet = self.bilyet
		doc.produk = self.produk_investasi
		doc.status_aro = self.status_aro
		doc.tanggal_pendaftaran = self.tanggal_pendaftaran
		doc.tanggal_berakhir = self.tanggal_jatuh_tempo
		doc.nominal = self.nominal
		doc.profit_perbulan = self.profit_per_bulan
		doc.profit_selama_tenor = self.profit_selama_tenor
		# doc.append("transaksi",{
		# 	"tanggal_transaksi":self.produk_investasi,
		# 	"jenis_transaksi":self.status_aro,
		# 	"nominal":self.tanggal_pendaftaran
		# })
		doc.insert()
	def after_delete(self):
		frappe.delete_doc('Estatement Investasi', self.nasabah+"-"+self.bilyet)
