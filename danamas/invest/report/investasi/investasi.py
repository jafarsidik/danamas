# Copyright (c) 2022, mjs and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Count
from pypika.terms import Case

def execute(filters=None):
	columns = [{
		"fieldname": "full_name",
		"label": "Nama",
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
		"fieldname": "bank",
		"label": "Bank",
		"fieldtype": "Data"
	},
	{
		"fieldname": "atas_nama",
		"label": "Nama Pemilik Rekening",
		"fieldtype": "Data"
	},
	{
		"fieldname": "no_rekening",
		"label": "Nomor Rekening",
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
		"fieldname": "nominal",
		"label": "Nominal",
		"fieldtype": "Currency"
	},
	{
		"fieldname": "profit_perbulan",
		"label": "Profit Perbulan",
		"fieldtype": "Currency"
	},
	{
		"fieldname": "profit_pertahun",
		"label": "Profit Pertahun",
		"fieldtype": "Currency"
	},
	{
		"fieldname": "tenor",
		"label": "Tenor",
		"fieldtype": "Data"
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
		"fieldname": "penarikan_komisi",
		"label": "Penarikan Profit",
		"fieldtype": "Select"
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
	status_nasabahsql = "ni.status = '{status_nasabah}'".format(status_nasabah=filters.status_nasabah) if filters.status_nasabah  else "1 = 1"
	startdatetemposql = "i.tanggal_jatuh_tempo >=Date('{from_date}')".format(from_date=filters.from_date) if filters.from_date  else "1 = 1"
	enddatetemposql = "i.tanggal_jatuh_tempo <=Date('{to_date}')".format(to_date=filters.to_date) if filters.to_date  else "1 = 1"
	
	data = frappe.db.sql(
		f"""
		SELECT 
			ni.nama_lengkap as full_name,
			ni.no_hp_1 as no_hp,
			ni.alamat as alamat,
			ni.status as status_nasabah,
			i.nama_bank as bank,
			i.a_n as atas_nama,
			i.no_rekening as no_rekening,
			i.tanggal_pendaftaran as tanggal_daftar,
			i.tanggal_jatuh_tempo as tanggal_berakhir,
			i.produk_investasi as produk,
			i.nominal as nominal,
			i.profit_nasabah as profit_perbulan,
			i.profit_pertahun as profit_pertahun,
			i.tenor as tenor,
			i.rate as rate,
			i.penarikan_komisi as penarikan_komisi,
			i.status_aro as status_aro,
			i.nasabah as cif,
			i.bilyet as bilyet,
			i.status_bilyet as status_bilyet,
			i.tanggal_jatuh_tempo as tanggal_jatuh_tempo
		FROM tabInvestasi i
		left join `tabNasabah Invest` ni on i.nasabah = ni.name
		left join tabAdvisor ad on ad.name = i.marketing
		WHERE ({cifsql}) and ({status_nasabahsql}) and ({startdatetemposql}) and ({enddatetemposql})
		""".format(cifsql=cifsql,status_nasabahsql=status_nasabahsql,startdatetemposql=startdatetemposql,enddatetemposql=enddatetemposql),as_dict=1)
	return columns, data
