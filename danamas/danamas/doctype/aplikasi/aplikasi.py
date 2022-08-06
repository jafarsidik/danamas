# Copyright (c) 2022, mjs and contributors
# For license information, please see license.txt

import json
import math

from frappe import _
from frappe.utils import add_months, add_days,flt, get_last_day, getdate, now_datetime,add_to_date

from frappe.model.document import Document

class Aplikasi(Document):

	#def on_update_after_submit(self):
	#	if self.is_transfer == 'Yes':
	#		self.make_repayment_schedule()

	def make_repayment_schedule(self):
		self.list_angsuran_pinjaman = []
		payment_date = self.tanggal_pencairan
		plafon = self.plafon_pembiayaan
		if self.jenis_pembiayaan == 'Flat':
			i = 0
			while  i < int(self.tenor):
				
				pokok_angsuran = self.pokok_angsuran
				bunga_angsuran = self.bunga_angsuran
				angsuran = self.angsuran
				plafon = flt(plafon - angsuran)
				if plafon < 0:
					plafon = 0.0

				if self.periode_angsuran == 'Bulanan':
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
					
				if self.periode_angsuran == 'Mingguan Per 24 Hari':
					self.append(
						"list_angsuran_pinjaman",
						{
							"tanggal_tagihan": add_single_week_24(payment_date),
							"pokok": pokok_angsuran,
							"bunga": bunga_angsuran,
							"angsuran": angsuran,
							"saldo_sisa": plafon,
						},
					)
					next_date = add_single_week_24(payment_date)
					payment_date = next_date
				if self.periode_angsuran == 'Mingguan Per 14 Hari':
					self.append(
						"list_angsuran_pinjaman",
						{
							"tanggal_tagihan": add_single_week_14(payment_date),
							"pokok": pokok_angsuran,
							"bunga": bunga_angsuran,
							"angsuran": angsuran,
							"saldo_sisa": plafon,
						},
					)
					next_date = add_single_week_14(payment_date)
					payment_date = next_date
				if self.periode_angsuran == 'Mingguan Per 10 Hari':
					self.append(
						"list_angsuran_pinjaman",
						{
							"tanggal_tagihan": add_single_week_10(payment_date),
							"pokok": pokok_angsuran,
							"bunga": bunga_angsuran,
							"angsuran": angsuran,
							"saldo_sisa": plafon,
						},
					)
					next_date = add_single_week_10(payment_date)
					payment_date = next_date
				if self.periode_angsuran == 'Mingguan Per 7 Hari':
					self.append(
						"list_angsuran_pinjaman",
						{
							"tanggal_tagihan": add_single_week_7(payment_date),
							"pokok": pokok_angsuran,
							"bunga": bunga_angsuran,
							"angsuran": angsuran,
							"saldo_sisa": plafon,
						},
					)
					next_date = add_single_week_7(payment_date)
					payment_date = next_date

				if self.periode_angsuran == 'Harian':
					self.append(
						"list_angsuran_pinjaman",
						{
							"tanggal_tagihan": add_single_days(payment_date),
							"pokok": pokok_angsuran,
							"bunga": bunga_angsuran,
							"angsuran": angsuran,
							"saldo_sisa": plafon,
						},
					)
					next_date = add_single_days(payment_date)
					payment_date = next_date
				i += 1
	
def add_single_month(date):
	if getdate(date) == get_last_day(date):
		return get_last_day(add_months(date, 1))
	else:
		return add_months(date, 1)

def add_single_week_24(date):
	if getdate(date) == get_last_day(date):
		return add_days(date, 24)
	else:
		return add_days(date, 24)

def add_single_week_14(date):
	if getdate(date) == get_last_day(date):
		return add_days(date, 14)
	else:
		return add_days(date, 14)

def add_single_week_10(date):
	if getdate(date) == get_last_day(date):
		return add_days(date, 10)
	else:
		return add_days(date, 10)

def add_single_week_7(date):
	if getdate(date) == get_last_day(date):
		return add_days(date, 7)
	else:
		return add_days(date, 7)

def add_single_days(date):
	if getdate(date) == get_last_day(date):
		return add_days(date, 1)
	else:
		return add_days(date, 1)