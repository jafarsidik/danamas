// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Jenis Pinjaman', {
	refresh: function(frm) {

		frm.toggle_display(['minimal_bayar_cicilan'], frm.doc.multi_pinjaman === 'Ya');
		frm.toggle_display(['berapa_x_cicilan'], frm.doc.hold_cicilan === 'Ya');
	},
	multi_pinjaman:function(frm){
		frm.toggle_display(['minimal_bayar_cicilan'], frm.doc.multi_pinjaman === 'Ya');
	},
	hold_cicilan:function(frm){
		frm.toggle_display(['berapa_x_cicilan'], frm.doc.hold_cicilan === 'Ya');
	}
});
