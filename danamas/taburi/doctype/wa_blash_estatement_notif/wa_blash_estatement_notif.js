// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt


frappe.ui.form.on('WA Blash Estatement Notif', {
	refresh: function(frm) {
		frm.add_custom_button(__('Send'), function(){
			
			frappe.confirm(
				'Apakah Anda Yakin akan Mengirim Pesan Ini?',
				function(){
					frappe.call({
						method:'danamas.taburi.api.sendWA', 
						args:{
							'docname': frm.doc.name,
							'count':1,
							'key':1
						},
						callback: (r) => {
							if(r.message[0] === 100){
								frappe.show_alert('Pengiriman Notifikasi E-Statement Nasabah Taburi Sukses')
							}
						}
					})
				}
			)
			
		}, __("Send WA"));
	}
	
});
