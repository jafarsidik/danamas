// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Portofolio Account Estatement"] = {
	"filters": [
		{
            "fieldname":"cif",
            "label":"CIF",
            "fieldtype": "Link",
            "options": "Nasabah Invest"
        },
		{
            "fieldname": "from_date",
            "label":"Start Periode ",
            "fieldtype": "Date",
			"default": frappe.datetime.year_start()
        },
        {
            "fieldname": "to_date",
            "label": "End Periode Date",
            "fieldtype": "Date",
			"default": frappe.datetime.year_end()
			
        },
	]
};
