// Copyright (c) 2024, hidayat and contributors
// For license information, please see license.txt

frappe.ui.form.on('Petty Cash', {
	before_save: function(frm,cdt,cdn) {
		var d = locals[cdt][cdn];
		var ce = 0.0;
		var de = 0.0;
		for (let item of d.accounting) {
			de = de + item.debit_in_account_currency;
			ce = ce + item.credit_in_account_currency;
		}
		frappe.model.set_value(d.doctype, d.name, "total_debit", de);
		frappe.model.set_value(d.doctype, d.name, "total_credit", ce);
		frappe.model.set_value(d.doctype, d.name, "difference", ce - de);
	}
});
