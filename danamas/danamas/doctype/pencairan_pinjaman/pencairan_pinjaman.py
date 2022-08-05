# Copyright (c) 2022, mjs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PencairanPinjaman(Document):
	def on_submit(self):
		doc = frappe.get_doc('Aplikasi', self.aplikasi)
		doc.is_transfer = 'Yes'
		doc.tanggal_pencairan = self.tanggal_pencairan
		doc.make_repayment_schedule()
		doc.save()
