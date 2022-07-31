# Copyright (c) 2022, mjs and contributors
# For license information, please see license.txt

import json
import math

import frappe
from frappe import _
from frappe.utils import add_months, flt, get_last_day, getdate, now_datetime

from frappe.model.document import Document

class Aplikasi(Document):
	def validate(self):
		self.make_repayment_schedule()

	def make_repayment_schedule(self):
		self.list_angsuran_pinjaman = []
		payment_date = self.tanggal_pengajuan
		plafon = self.plafon_pembiayaan
		if self.jenis_pembiayaan == 'Flat':
			i = 0
			while  i < int(self.tenor):
				
				pokok_angsuran = self.pokok_angsuran
				bunga_angsuran = self.bunga_angsuran
				angsuran = self.angsuran

				plafon = flt(plafon - angsuran)
				if plafon < 0:
					#angsuran += plafon
					plafon = 0.0
				
				self.append(
					"list_angsuran_pinjaman",
					{
						"tanggal_tagihan": add_single_month(payment_date),
						"pokok": pokok_angsuran,
						"bunga": bunga_angsuran,
						"angsuran": angsuran,
						"saldo_sisa": plafon,
					},
				)
				next_payment_date = add_single_month(payment_date)
				payment_date = next_payment_date
				i += 1
	
def add_single_month(date):
	if getdate(date) == get_last_day(date):
		return get_last_day(add_months(date, 1))
	else:
		return add_months(date, 1)