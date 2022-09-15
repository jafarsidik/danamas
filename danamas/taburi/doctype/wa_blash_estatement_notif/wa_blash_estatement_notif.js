// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt


frappe.ui.form.on('WA Blash Estatement Notif', {
	refresh: function(frm) {
		frappe.show_progress('Loading..', 70, 100, 'Please wait');
		frm.add_custom_button(__('Send'), function(){
			
			frappe.confirm(
				'Apakah Anda Yakin akan Mengirim Pesan Ini?',
				function(){
					frappe.call({
						method:'danamas.taburi.api.sendWA', 
						args:{
							'docname': frm.doc.name
						}
					}).then(r => {
						console.log(r.message)
					})
					//frappe.show_progress(title, count, total, description)
					//show_alert('Thanks for continue here!')
				}
			)
			
		}, __("Send WA"));
	}
	
});
