# Copyright (c) 2022, mjs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Investasi(Document):
	def after_insert(self):
		docInvest = frappe.get_doc(doctype='Estatement Investasi', cif=self.nasabah)

		if docInvest is None:
			doc = frappe.new_doc('Estatement Investasi')
			doc.cif = self.nasabah
			doc.nama_lengkap = self.nama_nasabah
			doc.mata_uang = 'IDR'
			doc.append("estatement_investasi_transaksi",{
			 	"nomor_rekening":self.no_rekening,
			 	"tanggal_pendaftaran":self.tanggal_pendaftaran,
			 	"tanggal_berakhir":self.tanggal_jatuh_tempo,
			 	"produk":self.produk_investasi,
			 	"nominal":self.nominal,
			 	"tenor":self.tenor,
			 	"rate":self.rate,
			 	"status_aro":self.status_aro,
			 	"bilyet":self.bilyet,
			 	"status_bilyet":self.status_bilyet
			})
			doc.insert()
		if docInvest is not None:
			docInvestEl = frappe.get_doc(doctype='Estatement Investasi', cif=self.nasabah)
			docInvestEl.cif = self.nasabah
			docInvestEl.nama_lengkap = self.nama_nasabah
			docInvestEl.mata_uang = 'IDR'
			docInvestEl.append("estatement_investasi_transaksi",{
			 	"nomor_rekening":self.no_rekening,
			 	"tanggal_pendaftaran":self.tanggal_pendaftaran,
			 	"tanggal_berakhir":self.tanggal_jatuh_tempo,
			 	"produk":self.produk_investasi,
			 	"nominal":self.nominal,
			 	"tenor":self.tenor,
			 	"rate":self.rate,
			 	"status_aro":self.status_aro,
			 	"bilyet":self.bilyet,
			 	"status_bilyet":self.status_bilyet
			})
			docInvestEl.insert(ignore_if_duplicate=True)
	def after_delete(self):
		frappe.delete_doc('Estatement Investasi', self.nasabah+"-"+self.bilyet)
