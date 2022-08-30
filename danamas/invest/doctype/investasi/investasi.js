// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Investasi', {
	
	tanggal_pendaftaran:function(frm){
		let x = frappe.datetime.add_months(frm.doc.tanggal_pendaftaran, frm.doc.tenor)
		
		// let end = moment(frm.doc.tanggal_pendaftaran).add(frm.doc.tenor, 'M')
		// alert(x)
		frm.set_value('tanggal_jatuh_tempo', x);
	},
	tenor:function(frm){
		let x = frappe.datetime.add_months(frm.doc.tanggal_pendaftaran, frm.doc.tenor)
		
		
		frm.set_value('tanggal_jatuh_tempo', x);
	},
	produk_investasi:function(frm){
		frappe.db.get_doc('Produk Investasi',frm.doc.produk_investasi).then(result => {
				
			frm.set_value('rate', result.rate);
			frm.set_value('m_fee', result.m_fee);
			
		})
	},
	nominal: function(frm){
		let nominal =  frm.doc.nominal
		let rate = ( frm.doc.rate  / 100)
		let m_fee = ( frm.doc.m_fee  / 100)

		let profit  = (nominal * rate);
		let fee = (profit* m_fee);
		let profit_nasabah = (profit - fee);
		let profit_pertahun = (profit_nasabah * 12)
		frm.set_value('profit', profit);
		frm.set_value('management_fee', fee);
		frm.set_value('profit_nasabah', profit_nasabah);
		frm.set_value('profit_pertahun', profit_pertahun);
		

	},
	rate: function(frm){
		let nominal =  frm.doc.nominal
		let rate = ( frm.doc.rate  / 100)
		let m_fee = ( frm.doc.m_fee  / 100)

		let profit  = (nominal * rate);
		let fee = (profit* m_fee);
		let profit_nasabah = (profit - fee);
		let profit_pertahun = (profit_nasabah * 12)
		frm.set_value('profit', profit);
		frm.set_value('management_fee', fee);
		frm.set_value('profit_nasabah', profit_nasabah);
		frm.set_value('profit_pertahun', profit_pertahun);
		

	},
	m_fee:function(frm){
		let nominal =  frm.doc.nominal
		let rate = ( frm.doc.rate  / 100)
		let m_fee = ( frm.doc.m_fee  / 100)

		let profit  = (nominal * rate);
		let fee = (profit* m_fee);
		let profit_nasabah = (profit - fee);
		let profit_pertahun = (profit_nasabah * 12)
		frm.set_value('profit', profit);
		frm.set_value('management_fee', fee);
		frm.set_value('profit_nasabah', profit_nasabah);
		frm.set_value('profit_pertahun', profit_pertahun);
	}
});
