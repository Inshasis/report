// Copyright (c) 2024, hidayat and contributors
// For license information, please see license.txt

frappe.ui.form.on('PDC Entry', {
	recalc: function (frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.pdc_type === "Receive"){
			frappe.model.set_value(d.doctype, d.name, "party_type", "Customer");
			frappe.model.set_value(d.doctype, d.name,"account_paid_from", "Debtors - A");
			
		}else{
			frappe.model.set_value(d.doctype, d.name, "party_type", "Supplier");
			frappe.model.set_value(d.doctype, d.name, "account_paid_from", "Creditors - A");
		}
	},
    onload: function (frm, cdt, cdn) {
        frm.trigger("recalc", cdt, cdn);
    },
    pdc_type: function (frm, cdt, cdn) {
        frm.trigger("recalc", cdt, cdn);
    }
});

frappe.ui.form.on('PDC Entry', {
	refresh: function (frm) {
		if (cur_frm.doc.docstatus === 1 && !cur_frm.doc.payment_entry_reference) {
			frm.add_custom_button(__("Payment Deposit"), () => {
				frappe.run_serially([
					() => {
						frappe.call({
							method: "report.report.doctype.pdc_entry.pdc_entry.make_pdc_entry_on_submit",
							args: {
								doc: cur_frm.doc,
							},
							callback: function (s) {
							}
						})
					}
				])
			})
		}
	}
});

frappe.ui.form.on('PDC Entry', {
	get_data: function (frm) {
		frappe.run_serially([
			() => {
				frappe.call({
					method: "report.report.doctype.pdc_entry.pdc_entry.get_reference_docs",
					args: {
						party_type: frm.doc.party_type,
						party: frm.doc.party,
						party_account: cur_frm.doc.pdc_type=="Receive" ? cur_frm.doc.account_paid_from : cur_frm.doc.account_paid_to,
					},
					callback: function (r) {
						if(r.message) {
							let ar = []; 
							for(let d of r.message){ 
								var c = frm.add_child("pdc_entry_reference");
								c.reference_doctype = d.voucher_type;
								c.reference_name = d.voucher_no;
								c.due_date = d.due_date
								c.total_amount = d.invoice_amount;
								c.outstanding_amount = d.outstanding_amount;
								c.bill_no = d.bill_no;
								c.payment_term = d.payment_term;
								c.allocated_amount = d.allocated_amount;

								ar.push(c.idx); 
								frm.refresh_field('pdc_entry_reference'); 
							}
						}
					}
				})
			}
		])
	}
})