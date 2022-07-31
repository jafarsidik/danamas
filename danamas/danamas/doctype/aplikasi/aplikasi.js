// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Aplikasi', {

	//refresh: function(frm) {

		//frm.toggle_display(['angsuran_x'], frm.doc.metode_angsuran === 'Manual');
	//},
	nama_produk: function (frm) {

		frappe.db.get_doc('Jenis Pinjaman',frm.doc.nama_produk).then(result => {
			
			frm.set_value('potongan_adm', result.administrasi);
			frm.set_value('potongan_provisi', result.provisi);
			frm.set_value('potongan_asuransi', result.asuransi);
			frm.set_value('potongan_bunga', result.bunga);
			frm.set_value('potongan_jasa', result.jasa_);
			let plafon = frm.doc.plafon_pembiayaan;
		
			//total angsuran
			let total_pokok = plafon;
			frm.set_value('total_pokok', total_pokok);
			let total_bunga = ((plafon * frm.doc.potongan_bunga) / 100 );
			frm.set_value('total_bunga', total_bunga);
			let total_angsuran = (total_pokok+total_bunga)
			frm.set_value('total_angsuran', total_angsuran);
			//Angsuran Per
			let pokok = (total_pokok / frm.doc.tenor);
			frm.set_value('pokok_angsuran', pokok);
			let bunga_angsuran = ( total_bunga / frm.doc.tenor);
			frm.set_value('bunga_angsuran', bunga_angsuran);
			let angsuran = (pokok + bunga_angsuran);
			frm.set_value('angsuran', angsuran);
			
			//biaya pencairan
			let total = ((100 - frm.doc.potongan_asuransi - frm.doc.potongan_adm - frm.doc.potongan_provisi - frm.doc.potongan_jasa) * frm.doc.plafon_pembiayaan / 100);
			frm.set_value('total', total);
			let x_cicilan = frm.doc.berapa_x_cicilan
			if(x_cicilan > 0){
				
				let total_after_hold = (total - (frm.doc.angsuran*x_cicilan))
				
				frm.set_value('total_after_hold', total_after_hold);
				let grand_total = (total_after_hold - frm.doc.biaya_transfer);
				frm.set_value('grand_total_', grand_total);
			}else{
				let grand_total = (total - frm.doc.biaya_transfer);
				frm.set_value('grand_total_', grand_total);
				
			}
			frm.toggle_display(['total_after_hold'], frm.doc.hold_cicilan === 'Ya');
		})
	},
	potongan_asuransi:function(frm){
		//biaya pencairan
		let total = ((100 - frm.doc.potongan_asuransi - frm.doc.potongan_adm - frm.doc.potongan_provisi - frm.doc.potongan_jasa) * frm.doc.plafon_pembiayaan / 100);
		frm.set_value('total', total);
		let x_cicilan = frm.doc.berapa_x_cicilan
		if(x_cicilan > 0){
			let total_after_hold = (total - (frm.doc.angsuran*x_cicilan))
			frm.set_value('total_after_hold', total_after_hold);
			let grand_total = (total_after_hold - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
		}else{
			let grand_total = (total - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
		}
	},
	potongan_adm:function(frm){
		//biaya pencairan
		let total = ((100 - frm.doc.potongan_asuransi - frm.doc.potongan_adm - frm.doc.potongan_provisi - frm.doc.potongan_jasa) * frm.doc.plafon_pembiayaan / 100);
		frm.set_value('total', total);
		let x_cicilan = frm.doc.berapa_x_cicilan
		if(x_cicilan > 0){
			let total_after_hold = (total - (frm.doc.angsuran*x_cicilan))
			frm.set_value('total_after_hold', total_after_hold);
			let grand_total = (total_after_hold - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
		}else{
			let grand_total = (total - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
		}
	},
	potongan_provisi:function(frm){
		//biaya pencairan
		let total = ((100 - frm.doc.potongan_asuransi - frm.doc.potongan_adm - frm.doc.potongan_provisi - frm.doc.potongan_jasa) * frm.doc.plafon_pembiayaan / 100);
		frm.set_value('total', total);
		let x_cicilan = frm.doc.berapa_x_cicilan
		if(x_cicilan > 0){
			let total_after_hold = (total - (frm.doc.angsuran*x_cicilan))
			frm.set_value('total_after_hold', total_after_hold);
			let grand_total = (total_after_hold - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
		}else{
			let grand_total = (total - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
		}
	},
	potongan_bunga:function(frm){
		//biaya pencairan
		let total = ((100 - frm.doc.potongan_asuransi - frm.doc.potongan_adm - frm.doc.potongan_provisi - frm.doc.potongan_jasa) * frm.doc.plafon_pembiayaan / 100);
		frm.set_value('total', total);
		let x_cicilan = frm.doc.berapa_x_cicilan
		if(x_cicilan > 0){
			let total_after_hold = (total - (frm.doc.angsuran*x_cicilan))
			frm.set_value('total_after_hold', total_after_hold);
			let grand_total = (total_after_hold - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
		}else{
			let grand_total = (total - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
		}
	},
	potongan_jasa: function (frm) {
		//biaya pencairan
		let total = ((100 - frm.doc.potongan_asuransi - frm.doc.potongan_adm - frm.doc.potongan_provisi - frm.doc.potongan_jasa) * frm.doc.plafon_pembiayaan / 100);
		frm.set_value('total', total);
		let x_cicilan = frm.doc.berapa_x_cicilan
		if(x_cicilan > 0){
			let total_after_hold = (total - (frm.doc.angsuran*x_cicilan))
			frm.set_value('total_after_hold', total_after_hold);
			let grand_total = (total_after_hold - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
		}else{
			let grand_total = (total - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
		}
	},
	biaya_transfer: function (frm) {
		
		
		let x_cicilan = frm.doc.berapa_x_cicilan
		if(x_cicilan > 0){
			let grand_total = (frm.doc.total_after_hold - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
		}else{
			let grand_total = frm.doc.total - frm.doc.biaya_transfer;
			frm.set_value('grand_total_', grand_total);
		}
	},
	potongan_bunga: function(frm){
		let plafon = frm.doc.plafon_pembiayaan;

		//total angsuran
		let total_pokok = plafon;
		frm.set_value('total_pokok', total_pokok);
		let total_bunga = ((plafon * frm.doc.potongan_bunga) / 100 );
		frm.set_value('total_bunga', total_bunga);
		let total_angsuran = (total_pokok+total_bunga)
		frm.set_value('total_angsuran', total_angsuran);
		//Angsuran Per
		let pokok = (total_pokok / frm.doc.tenor);
		frm.set_value('pokok_angsuran', pokok);
		let bunga_angsuran = ( total_bunga / frm.doc.tenor);
		frm.set_value('bunga_angsuran', bunga_angsuran);
		let angsuran = (pokok + bunga_angsuran);
		frm.set_value('angsuran', angsuran);
		
		
		//biaya pencairan
		let total = ((100 - frm.doc.potongan_asuransi - frm.doc.potongan_adm - frm.doc.potongan_provisi - frm.doc.potongan_jasa) * frm.doc.plafon_pembiayaan / 100);
		frm.set_value('total', total);
		let x_cicilan = frm.doc.berapa_x_cicilan
		if(x_cicilan > 0){
			
			let total_after_hold = (total - (frm.doc.angsuran*x_cicilan))
			frm.set_value('total_after_hold', total_after_hold);
			let grand_total = (total_after_hold - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
		}else{
			let grand_total = (total - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
			
		}
		
	},
	tenor:function(frm){
		let plafon = frm.doc.plafon_pembiayaan;

		//total angsuran
		let total_pokok = plafon;
		frm.set_value('total_pokok', total_pokok);
		let total_bunga = ((plafon * frm.doc.potongan_bunga) / 100 );
		frm.set_value('total_bunga', total_bunga);
		let total_angsuran = (total_pokok+total_bunga)
		frm.set_value('total_angsuran', total_angsuran);
		//Angsuran Per
		let pokok = (total_pokok / frm.doc.tenor);
		frm.set_value('pokok_angsuran', pokok);
		let bunga_angsuran = ( total_bunga / frm.doc.tenor);
		frm.set_value('bunga_angsuran', bunga_angsuran);
		let angsuran = (pokok + bunga_angsuran);
		frm.set_value('angsuran', angsuran);
		

		//biaya pencairan
		let total = ((100 - frm.doc.potongan_asuransi - frm.doc.potongan_adm - frm.doc.potongan_provisi - frm.doc.potongan_jasa) * frm.doc.plafon_pembiayaan / 100);
		frm.set_value('total', total);
		let x_cicilan = frm.doc.berapa_x_cicilan
		if(x_cicilan > 0){
			
			let total_after_hold = (total - (frm.doc.angsuran*x_cicilan))
			frm.set_value('total_after_hold', total_after_hold);
			let grand_total = (total_after_hold - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
		}else{
			let grand_total = (total - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
			
		}
	},
	plafon_pembiayaan: function (frm) {
		
		let plafon = frm.doc.plafon_pembiayaan;

		//total angsuran
		let total_pokok = plafon;
		frm.set_value('total_pokok', total_pokok);
		let total_bunga = ((plafon * frm.doc.potongan_bunga) / 100 );
		frm.set_value('total_bunga', total_bunga);
		let total_angsuran = (total_pokok+total_bunga)
		frm.set_value('total_angsuran', total_angsuran);
		//Angsuran Per
		let pokok = (total_pokok / frm.doc.tenor);
		frm.set_value('pokok_angsuran', pokok);
		let bunga_angsuran = ( total_bunga / frm.doc.tenor);
		frm.set_value('bunga_angsuran', bunga_angsuran);
		let angsuran = (pokok + bunga_angsuran);
		frm.set_value('angsuran', angsuran);
		
		
		//biaya pencairan
		let total = ((100 - frm.doc.potongan_asuransi - frm.doc.potongan_adm - frm.doc.potongan_provisi - frm.doc.potongan_jasa) * frm.doc.plafon_pembiayaan / 100);
		frm.set_value('total', total);
		let x_cicilan = frm.doc.berapa_x_cicilan
		if(x_cicilan > 0){
			
			let total_after_hold = (total - (frm.doc.angsuran*x_cicilan))
			frm.set_value('total_after_hold', total_after_hold);
			let grand_total = (total_after_hold - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
		}else{
			let grand_total = (total - frm.doc.biaya_transfer);
			frm.set_value('grand_total_', grand_total);
			
		}
	}
});
