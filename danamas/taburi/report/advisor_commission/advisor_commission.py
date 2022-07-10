# Copyright (c) 2022, mjs and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count
from pypika.terms import Case

def execute(filters=None):
	message = ["Komisi 1% Untuk Advisor"]
	columns = [{
		"fieldname": "ao",
		"label": "Advisor Code",
		"fieldtype": "Link",
		"options": "Advisor"
	},
	{
		"fieldname": "ao_name",
		"label": "Advisor Name",
		"fieldtype": "Data"
	},
	{
		"fieldname": "debit",
		"label": "Debit",
		"fieldtype": "Currency"
	},
	{ "fieldname": "januari", "label": "Januari", "fieldtype": "Currency" },
	{ "fieldname": "februari","label": "Februari","fieldtype": "Currency"},
	{ "fieldname": "maret","label": "Maret","fieldtype": "Currency"},
	{ "fieldname": "april","label": "April","fieldtype": "Currency"},
	{ "fieldname": "mei","label": "Mei","fieldtype": "Currency"},
	{ "fieldname": "juni","label": "Juni","fieldtype": "Currency"},
	{ "fieldname": "juli","label": "Juli","fieldtype": "Currency"},
	{ "fieldname": "agustus","label": "Agustus","fieldtype": "Currency"},
	{ "fieldname": "september","label": "September","fieldtype": "Currency"},
	{ "fieldname": "oktober","label": "Oktober","fieldtype": "Currency"},
	{ "fieldname": "november","label": "November","fieldtype": "Currency"},
	{ "fieldname": "desember","label": "Desember","fieldtype": "Currency"}
	]
	data = frappe.db.sql(
		f"""
		SELECT
			ao_name,
			ao,
			month(transaction_date),
			sum(debit) as debit,
			sum(case when (month(transaction_date) ='01') then (debit*1/100) else 0 end) as januari,
			sum(case when (month(transaction_date) ='02') then (debit*1/100) else 0 end) as februari,
			sum(case when (month(transaction_date) ='03') then (debit*1/100) else 0 end) as maret,
			sum(case when (month(transaction_date) ='04') then (debit*1/100) else 0 end) as april,
			sum(case when (month(transaction_date) ='05') then (debit*1/100) else 0 end) as mei,
			sum(case when (month(transaction_date) ='06') then (debit*1/100) else 0 end) as juni,
			sum(case when (month(transaction_date) ='07') then (debit*1/100) else 0 end) as juli,
			sum(case when (month(transaction_date) ='08') then (debit*1/100) else 0 end) as agustus,
			sum(case when (month(transaction_date) ='09') then (debit*1/100) else 0 end) as september,
			sum(case when (month(transaction_date) ='10') then (debit*1/100) else 0 end) as oktober,
			sum(case when (month(transaction_date) ='11') then (debit*1/100) else 0 end) as november,
			sum(case when (month(transaction_date) ='12') then (debit*1/100) else 0 end) as desember
		FROM `tabTransaction`
		where year(transaction_date) = year(curdate())
		group by ao
		""", as_dict=1)

	return columns, data,message
