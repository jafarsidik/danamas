// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pembayaran Angsuran', {
	refresh: function(frm) {
		if(frm.is_new()){
			frappe.db.count('Pembayaran Angsuran', {'aplikasi_number': frm.doc.aplikasi_number}).then(count => {
				let angsuran = count+1;
				frm.set_value('angsuran_ke', angsuran);
				frappe.call('danamas.danamas.doctype.pembayaran_angsuran.pembayaran_angsuran.tanggalcicilan', {
					aplikasi: frm.doc.aplikasi_number+"|"+angsuran
				}).then(r => {
					
					frm.set_value('tanggal_tempo', r.message.tanggal_tagihan);
					frm.set_value('tanggal_pembayaran',frappe.datetime.nowdate());
					// let time_diff_in_days = moment(frm.doc.tanggal_pembayaran).diff(frm.doc.tanggal_tempo, 'days');
					// if(time_diff_in_days > 0){
					// 	let denda = (frm.doc.angsuran*1)/100;
					// 	frm.set_value('denda', denda);
					// }
					
				});
			});
			
			
		}
	},
	tanggal_pembayaran:function(frm){
		let time_diff_in_days = moment(frm.doc.tanggal_pembayaran).diff(frm.doc.tanggal_tempo, 'days');
			if(time_diff_in_days > 0){
				let denda = (frm.doc.angsuran*1)/100;
				frm.set_value('denda', denda);
			}else{
				let denda = 0;
				frm.set_value('denda', denda);
			}
	},
	pembayaran:function(frm){
		
		frm.set_value('total_pembayaran', frm.doc.pembayaran);
		let kembalian = frm.doc.total_pembayaran - frm.doc.angsuran;
		frm.set_value('kelebihan_pembayaran', kembalian);
	},
	penambahan_pembayaran_via_simpanan_sementara:function(frm){
		if(frm.doc.penambahan_pembayaran_via_simpanan_sementara == 1){
			
			
			frappe.call('danamas.danamas.doctype.pembayaran_angsuran.pembayaran_angsuran.getsaldonasabahsimpanansementara', {
				nasabah: frm.doc.nasabah
			}).then(r => {
				let saldo = r.message
				let total_pembayaran = saldo+frm.doc.pembayaran;
				frm.set_value('saldo_simpanan', saldo);
				frm.set_value('total_pembayaran', total_pembayaran);
				let kembalian = frm.doc.total_pembayaran - frm.doc.angsuran;
				frm.set_value('kelebihan_pembayaran', kembalian);
			})
		}else{
			frm.refresh_field('total_pembayaran');
			frm.refresh_field('saldo_simpanan');
			frm.refresh_field('kelebihan_pembayaran');
			let total = frm.doc.total_pembayaran - frm.doc.saldo_simpanan;
			frm.set_value('total_pembayaran', total);
			frm.set_value('saldo_simpanan',0);
			let kembalian = frm.doc.total_pembayaran - frm.doc.angsuran;
			frm.set_value('kelebihan_pembayaran', kembalian);
		}
	}
});
