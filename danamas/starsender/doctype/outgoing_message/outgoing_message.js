// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Outgoing Message', {
	// refresh: function(frm) {

	// }
	after_save:function(frm){
		let to_ = frm.doc.to;
		let apikey = frm.doc.apikey;
		
		to_.forEach(function(item, index, arr) { 
			
		// 	var myHeaders = new Headers();
		// 	myHeaders.append("apikey", apikey);
			
		// 	var formdata = new FormData();
		// 	formdata.append("tujuan", item.phone_number);
		// 	formdata.append("message", frm.doc.message);
			

			frappe.call({
				method: 'danamas.starsender.api.sendText',
				args: {
					apikey: apikey,
					tujuan: item.phone_number,
					message:frm.doc.message
				},
			}).then(r => {
				console.log(r.message)
			})
			
		})
	}
});
