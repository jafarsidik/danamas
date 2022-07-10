// Copyright (c) 2022, mjs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Aplikasi Kredit', {
	// refresh: function(frm) {

	// }
	nama_produk: function (frm) {

		frappe.db.get_doc('Setting').then(result => {

			if (frm.doc.nama_produk == "DMIBBU") {

				frm.set_value('potongan_adm', result.dmibbu_adm);
				frm.set_value('potongan_provisi', result.dmibbu_provisi);
				frm.set_value('potongan_asuransi', result.dmibbu_asuransi);
				frm.set_value('biaya_transfer', '0');
				frm.set_value('bunga_angsuran', result.dmibbu_bunga);

			} else if (frm.doc.nama_produk == "DMIPRIA") {

				frm.set_value('potongan_adm', result.dmipria_adm)
				frm.set_value('potongan_provisi', result.dmipria_provisi)
				frm.set_value('potongan_asuransi', result.dmipria_suransi)
				frm.set_value('biaya_transfer', '0')
				frm.set_value('bunga_angsuran', result.dmipria_bunga);
				// let total_pemotongan = ((100 - result.dmipria_adm - result.dmipria_provisi - result.dmipria_bunga - result.dmipria_suransi) * frm.doc.plafon_pembiayaan);
				// frm.set_value('total', total_pemotongan)
			} else if (frm.doc.nama_produk == "DMIPACAR") {

				frm.set_value('potongan_adm', result.dmipacar_adm)
				frm.set_value('potongan_provisi', result.dmipacar_provisi)
				frm.set_value('potongan_asuransi', result.dmipacar_suransi)
				frm.set_value('biaya_transfer', '0')
				frm.set_value('bunga_angsuran', result.dmipacar_bunga);
			}
			//frm.toggle_display(['minggu_per_sepuluh'], frm.doc.nama_produk == "DMIBBU");
			//frm.toggle_display(['per_bulan'], frm.doc.nama_produk == "DMIPRIA");
		})
	},
	plafon_pembiayaan: function (frm) {
		//biaya pencairan
		let total = ((100 - frm.doc.potongan_asuransi - frm.doc.potongan_adm - frm.doc.potongan_provisi) * frm.doc.plafon_pembiayaan / 100);
		frm.set_value('total', total);
		frm.set_value('biaya_transfer', frm.doc.biaya_transfer);
		let grand_total = total - frm.doc.biaya_transfer;
		frm.set_value('grand_total_', grand_total);


	},
	biaya_transfer: function (frm) {
		let grand_total = frm.doc.total - frm.doc.biaya_transfer;
		frm.set_value('grand_total_', grand_total);
	},
	metode_angsuran: function (frm) {
		let plafon = frm.doc.plafon_pembiayaan;
		let total_bunga = ((plafon * frm.doc.bunga_angsuran) / 100);
		frm.set_value('total_bunga', total_bunga);
		let angsuran = (plafon + total_bunga) / frm.doc.metode_angsuran;
		frm.set_value('angsuran', angsuran);
		let pokok = plafon / frm.doc.metode_angsuran;
		frm.set_value('pokok', pokok);
		let bunga = total_bunga / frm.doc.metode_angsuran;
		frm.set_value('bunga', bunga);
	},
	bunga_angsuran: function (frm) {
		let plafon = frm.doc.plafon_pembiayaan;
		let total_bunga = ((plafon * frm.doc.bunga_angsuran) / 100);
		frm.set_value('total_bunga', total_bunga);
		let angsuran = (plafon + total_bunga) / frm.doc.metode_angsuran;
		frm.set_value('angsuran', angsuran);
		let pokok = plafon / frm.doc.metode_angsuran;
		frm.set_value('pokok', pokok);
		let bunga = total_bunga / frm.doc.metode_angsuran;
		frm.set_value('bunga', bunga);

	}

});
