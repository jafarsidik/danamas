// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Investasi', {
	// refresh: function(frm) {

	// }
	jenis_investasi:function(frm){
		frappe.db.get_doc('Jenis Investasi',frm.doc.jenis_investasi).then(result => {
			frm.set_value('suku_bunga', result.suku_bunga);
			frm.set_value('sistem_bunga', result.sistem_bunga);
			frm.set_value('saldo_min_pajak', result.saldo_min_pajak);
			frm.set_value('persen_pajak', result.persen_pajak);
			frm.set_value('jangka_waktu', result.waktu);
		});
	},
});
