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
		"fieldname": "total",
		"label": "Total",
		"fieldtype": "Currency"
	},
	{
		"fieldname": "komission_fee",
		"label": "Komision Fee",
		"fieldtype": "Currency"
	}
	]
	data = frappe.db.sql(
		f"""
		SELECT
			c.advisor,
			month(t.transaction_date),
			sum(t.debit - t.credit) as total,
			sum((t.debit-t.credit)*1/100) as komission_fee
		FROM `tabTransaction` AS t
		left join `tabCustomers` as c on `c`.`name` = `t`.`customers`
		where year(transaction_date) = year(curdate())
		group by c.advisor
		""", as_dict=1)

	return columns, data,message
