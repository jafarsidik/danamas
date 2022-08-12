# Copyright (c) 2022, mjs and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count
from pypika.terms import Case


def execute(filters=None):
	columns = [{
		"fieldname": "customers",
		"label": "CIF",
		"fieldtype": "Link",
		"options": "Customers",
		"width": 80
	},
	{
		"fieldname": "full_name",
		"label": "Nasabah",
		"fieldtype": "Data",
		"width": 150
	},
	{
		"fieldname": "ao_name",
		"label": "Advisor Name",
		"fieldtype": "Data",
		"width": 150
	},
	{
		"fieldname": "join_date",
		"label": "Join Date",
		"fieldtype": "Date",
	},
	{
		"fieldname": "debit",
		"label": "Credit",
		"fieldtype": "Currency",
		"width": 100
	},
	{
		"fieldname": "credit",
		"label": "Debit",
		"fieldtype": "Currency",
		"width": 100
	},
	{
		"fieldname": "saldo",
		"label": "Saldo",
		"fieldtype": "Currency",
		"width": 100,
	},
	{ "fieldname": "3_month", "label": "3 Month", "fieldtype": "Currency" },
	{ "fieldname": "6_month", "label": "6 Month", "fieldtype": "Currency" },
	{ "fieldname": "9_month", "label": "9 Month", "fieldtype": "Currency" },
	{ "fieldname": "12_month", "label": "12 Month", "fieldtype": "Currency" },
	{ "fieldname": "grand_total", "label": "Grand Total", "fieldtype": "Currency","width": 110}
	]
	data = frappe.db.sql(
		f"""
		SELECT 
			c.name as customers,
			c.full_name,
			ad.full_name as ao_name,
			c.join_date,
			sum(t.debit) as debit,
			sum(t.credit) as credit,
			sum(t.debit - t.credit) as saldo,
			sum(case when (month(t.join_date+interval 3 month) and t.time_periode = "3 Month") then (t.debit*0.5/100) else 0 end) as 3_month,
			sum(case when (month(t.join_date+interval 6 month) and t.time_periode = "6 Month") then (t.debit*1/100) else 0 end) as 6_month,
			sum(case when (month(t.join_date+interval 9 month) and t.time_periode = "9 Month") then (t.debit*1.5/100) else 0 end) as 9_month,
			sum(case when (month(t.join_date+interval 12 month)and t.time_periode = "12 Month") then (t.debit*2/100) else 0 end) as 12_month,
			sum(
				case 
				when (month(t.join_date+interval 3 month) and t.time_periode = "3 Month") then (t.debit*0.5/100)+(t.debit - t.credit)
				when (month(t.join_date+interval 6 month) and t.time_periode = "6 Month") then (t.debit*1/100)+(t.debit - t.credit)
				when (month(t.join_date+interval 9 month) and t.time_periode = "9 Month") then (t.debit*1.5/100)+(t.debit - t.credit)
				when (month(t.join_date+interval 12 month)and t.time_periode = "12 Month") then (t.debit*2/100)+(t.debit - t.credit)
				else 0 end
			) as grand_total
			FROM tabTransaction t
			left join tabCustomers c on c.name= t.customers
			left join tabAdvisor ad on c.advisor = ad.name
			group by c.name
		""", as_dict=1)
	return columns, data
