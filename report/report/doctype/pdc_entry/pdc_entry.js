// Copyright (c) 2024, hidayat and contributors
// For license information, please see license.txt

frappe.ui.form.on('PDC Entry', {
	refresh: function (frm) {
		if (cur_frm.doc.docstatus === 1 && !cur_frm.doc.payment_entry_reference) {
			frm.add_custom_button(__("Payment Deposit"), () => {
				const dialog = frappe.prompt([
					{
						fieldtype: 'Link',
						fieldname: 'bank',
						label: __('Bank'),
						options: "Bank",
						reqd: 1,
					},
				], function (r) {
					frappe.run_serially([
						() => {
							frappe.call({
								method: "report.report.doctype.pdc_entry.pdc_entry.make_pdc_entry_on_submit",
								args: {
									name: cur_frm.doc.name,
									clearance_date: cur_frm.doc.clearance_date,
									invoice: cur_frm.doc.invoice,
									paid_amount: cur_frm.doc.paid_amount,
									pdc_type: cur_frm.doc.pdc_type,
									posting_date: cur_frm.doc.posting_date,
									mode_of_payment: cur_frm.doc.mode_of_payment,
									party: cur_frm.doc.party,
									account_paid_from: cur_frm.doc.account_paid_from,
									account_paid_to: cur_frm.doc.account_paid_to,
									paid_from_account_currency: cur_frm.doc.paid_from_account_currency,
									paid_to_account_currency: cur_frm.doc.paid_to_account_currency,
									reference_no: cur_frm.doc.reference_no,
									reference_date: cur_frm.doc.reference_date,
									bank:dialog.get_values().bank,
								},
								callback: function (s) {
								}
							})
						}
					])
				}
				)

			});
		}

	}
});
