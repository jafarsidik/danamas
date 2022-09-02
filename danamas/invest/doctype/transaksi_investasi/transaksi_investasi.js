// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transaksi Investasi', {
	// refresh: function(frm) {
		
	// }
	transaksi_investasi:function(frm){
		frm.toggle_display([
			'profit',
		], frm.doc.transaksi_investasi === 'Penciran Dana');
	}
});
