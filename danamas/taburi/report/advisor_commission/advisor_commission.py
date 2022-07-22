# Copyright (c) 2022, mjs and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count
from pypika.terms import Case

def execute(filters=None):
	message = ["Komisi 1% Untuk Advisor"]
	columns = [{
		"fieldname": "advisor",
		"label": "Advisor Code",
		"fieldtype": "Link",
		"options": "Advisor"
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
			c.advisor,
			month(t.transaction_date),
			sum(t.debit) as debit,
			sum(case when (month(t.transaction_date) ='01') then (t.debit*1/100) else 0 end) as januari,
			sum(case when (month(t.transaction_date) ='02') then (t.debit*1/100) else 0 end) as februari,
			sum(case when (month(t.transaction_date) ='03') then (t.debit*1/100) else 0 end) as maret,
			sum(case when (month(t.transaction_date) ='04') then (t.debit*1/100) else 0 end) as april,
			sum(case when (month(t.transaction_date) ='05') then (t.debit*1/100) else 0 end) as mei,
			sum(case when (month(t.transaction_date) ='06') then (t.debit*1/100) else 0 end) as juni,
			sum(case when (month(t.transaction_date) ='07') then (t.debit*1/100) else 0 end) as juli,
			sum(case when (month(t.transaction_date) ='08') then (t.debit*1/100) else 0 end) as agustus,
			sum(case when (month(t.transaction_date) ='09') then (t.debit*1/100) else 0 end) as september,
			sum(case when (month(t.transaction_date) ='10') then (t.debit*1/100) else 0 end) as oktober,
			sum(case when (month(t.transaction_date) ='11') then (t.debit*1/100) else 0 end) as november,
			sum(case when (month(t.transaction_date) ='12') then (t.debit*1/100) else 0 end) as desember
		FROM `tabTransaction` AS t
		left join `tabCustomers` as c on `c`.`name` = `t`.`customers`
		where year(transaction_date) = year(curdate())
		group by c.advisor
		""", as_dict=1)

	return columns, data,message
