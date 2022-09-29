# Copyright (c) 2022, mjs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TransaksiInvestasi(Document):
	def before_save(self):
		if(self.transaksi_investasi == "Setoran Dana"):
			inv = frappe.get_doc("Investasi",self.investasi)
			inv.status_setoran_dana = 'Sudah'
			inv.save()
		if(self.transaksi_investasi == "Penarikan Dana"):
			inv = frappe.get_doc("Investasi",self.investasi)
			inv.status_penarikan_dana = 'Sudah'
			inv.save()
	def after_insert(self):
		doc = frappe.get_doc('Estatement Investasi',self.cif_nasabah+"-"+self.investasi)
		doc.append("transaksi",{
			"tanggal_transaksi":self.tanggal_transaksi,
			"jenis_transaksi":self.transaksi_investasi,
			"nominal":self.nominal
		})
		doc.save()
