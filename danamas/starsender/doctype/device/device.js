// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Device', {
	// refresh: function(frm) {

	// }
	get_log:function(frm){
		fetch('https://starsender.online/api/v1/getDevice', {
			method: 'POST',
			headers: {
				'apikey': frm.doc.apikey,
				'Content-Type': 'application/json',
				'Access-Control-Allow-Origin': '*',
				'Access-Control-Allow-Methods': 'POST'
			},
		}).then(r => {
			frm.set_value('logs', r.json());
		});

	}
});
