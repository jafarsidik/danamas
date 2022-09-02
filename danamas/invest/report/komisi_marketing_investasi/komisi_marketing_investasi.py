# Copyright (c) 2022, mjs and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count
from pypika.terms import Case

def execute(filters=None):
	columns = [{
		"fieldname": "kode_marketing",
		"label": "AO",
		"fieldtype": "Link",
		"options":"Advisor"
	},
	{
		"fieldname": "nama_marketing",
		"label": "Nama Marketing",
		"fieldtype": "Data"
	},
	{
		"fieldname": "full_name",
		"label": "Nama Investor",
		"fieldtype": "Data"
	},
	{
		"fieldname": "no_hp",
		"label": "No HP",
		"fieldtype": "Data"
	},
	{
		"fieldname": "alamat",
		"label": "Alamat",
		"fieldtype": "Data"
	},
	{
		"fieldname": "tanggal_daftar",
		"label": "Tanggal Pendaftaran",
		"fieldtype": "Date"
	},
	{
		"fieldname": "tanggal_berakhir",
		"label": "Tanggal Berakhir",
		"fieldtype": "Date"
	},
	{
		"fieldname": "produk",
		"label": "Produk",
		"fieldtype": "Data"
	},
	{
		"fieldname": "tenor",
		"label": "Tenor",
		"fieldtype": "Data"
	},
	{
		"fieldname": "nominal",
		"label": "Nominal",
		"fieldtype": "Currency"
	},
	{
		"fieldname": "komisi",
		"label": "Komisi",
		"fieldtype": "Currency"
	},
	{
		"fieldname": "rate",
		"label": "Rate",
		"fieldtype": "Percent"
	},
	{
		"fieldname": "status_aro",
		"label": "Status ARO",
		"fieldtype": "Data"
	},
	{
		"fieldname": "cif",
		"label": "CIF",
		"fieldtype": "Link",
		"options":"Nasabah Invest"
	},
	{
		"fieldname": "bilyet",
		"label": "Bilyet",
		"fieldtype": "Link",
		"options":"Investasi"
	},
	{
		"fieldname": "status_bilyet",
		"label": "Status Bilyet",
		"fieldtype": "Data"
	}]
	cifsql = "i.nasabah = '{cif}'".format(cif=filters.cif) if filters.cif  else "1 = 1"
	marketingsql = "i.marketing = '{nama_marketing}'".format(nama_marketing=filters.nama_marketing) if filters.nama_marketing  else "1 = 1"
	startdatetemposql = "i.tanggal_jatuh_tempo >=Date('{from_date}')".format(from_date=filters.from_date) if filters.from_date  else "1 = 1"
	enddatetemposql = "i.tanggal_jatuh_tempo <=Date('{to_date}')".format(to_date=filters.to_date) if filters.to_date  else "1 = 1"
	
	data = frappe.db.sql(
		f"""
		SELECT 
			i.marketing as kode_marketing,
			ad.full_name as nama_marketing,
			ni.nama_lengkap as full_name,
			ni.no_hp_1 as no_hp,
			ni.alamat as alamat,
			i.tanggal_pendaftaran as tanggal_daftar,
			i.tanggal_jatuh_tempo as tanggal_berakhir,
			i.produk_investasi as produk,
			i.nominal as nominal,
			i.tenor as tenor,
			i.rate as rate,
			i.status_aro as status_aro,
			ni.name as cif,
			i.bilyet as bilyet,
			i.status_bilyet as status_bilyet,
			case 
				when (i.tenor = 12) and (i.nominal >=500000000) then (i.nominal*7/100) 
				when (i.tenor = 12) and (i.nominal <500000000) then (i.nominal*5/100)
				when (i.tenor = 6) and (i.nominal >=500000000) then (i.nominal*3.5/100)
				when (i.tenor = 6) and (i.nominal <500000000) then (i.nominal*2.5/100)
				when (i.tenor = 3) and (i.nominal >=500000000) then (i.nominal*1.25/100)
				when (i.tenor = 3) and (i.nominal <500000000) then (i.nominal*1.75/100)
				else 0 end as komisi
			FROM tabInvestasi i
			left join `tabNasabah Invest` ni on i.nasabah = ni.name
			left join tabAdvisor ad on ad.name = i.marketing
		WHERE i.status_penarikan_dana = "Belum" and ({cifsql}) and ({marketingsql}) and  ({startdatetemposql}) and ({enddatetemposql})
		""".format(cifsql=cifsql,marketingsql=marketingsql,startdatetemposql=startdatetemposql,enddatetemposql=enddatetemposql),as_dict=1)
	return columns, data
