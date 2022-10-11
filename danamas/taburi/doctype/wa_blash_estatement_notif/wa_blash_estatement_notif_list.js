
frappe.listview_settings['WA Blash Estatement Notif'] =  {
	onload: function(doclist) {
		doclist.page.add_action_item(__("Send WA"), function() {
			//frappe.msgprint( names );
			const docnames = doclist.get_checked_items(true);
			let names=[];
		    frappe.confirm(
			 	'Apakah Anda Yakin akan Mengirim Pesan Ini?',
			 	function(){
					
					$.each(docnames, function(key, value) {
						frappe.call({
							method:'danamas.taburi.api.sendWA', 
							args:{
								'docname': value,
								'count':docnames.length,
								'key':(key+1)
							},
							callback: (r) => {
								if(r.message[0] === 100){
									frappe.show_alert('Pengiriman Notifikasi E-Statement Nasabah Taburi Sukses')
								}
							},
						})
						
					});
					
			 	}
			 )
		});
	},
}
