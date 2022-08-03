// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pembayaran Angsuran', {
	refresh: function(frm) {
		if(frm.is_new()){
			frappe.db.count('Pembayaran Angsuran', {'aplikasi_number': frm.doc.aplikasi_number}).then(count => {
				let angsuran = count+1;
				frm.set_value('angsuran_ke', angsuran);
			});
		}
	},
	pembayaran:function(frm){
	
		frm.set_value('total_pembayaran', frm.doc.pembayaran);
		let kembalian = frm.doc.total_pembayaran - frm.doc.angsuran;
		frm.set_value('kelebihan_pembayaran', kembalian);
	},
	penambahan_pembayaran_via_simpanan_sementara:function(frm){
		if(frm.doc.penambahan_pembayaran_via_simpanan_sementara == 1){
			
			frappe.db.get_doc('Simpanan Sementara', null, {nasabah: frm.doc.nasabah}).then(res => {
				let val = res.nominal_rp;
				console.log(res)
				let total_pembayaran = frm.doc.pembayaran;
				frm.set_value('total_pembayaran', total_pembayaran);
			});
			
		}else{
			frm.refresh_field('total_pembayaran');
		}
	}
});
