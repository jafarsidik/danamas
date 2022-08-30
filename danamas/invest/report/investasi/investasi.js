// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Investasi"] = {
	"filters": [
		{
            "fieldname":"cif",
            "label":"CIF",
            "fieldtype": "Link",
            "options": "Nasabah Invest"
        },
		{
            "fieldname":"status_nasabah",
            "label":"Status Nasabah",
            "fieldtype": "Select",
            "options": [
                'Aktif',
                'Non Aktif'
            ],
			"default": 'Aktif',
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
