// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Komisi Marketing Investasi"] = {
	"filters": [
		{
            "fieldname":"cif",
            "label":"CIF",
            "fieldtype": "Link",
            "options": "Nasabah Invest"
        },
		{
            "fieldname":"nama_marketing",
            "label":"Nama Marketing",
            "fieldtype": "Link",
            "options": "Advisor"
        },
		{
            "fieldname": "from_date",
            "label":"From Date",
            "fieldtype": "Date",
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
        },
	]
};
