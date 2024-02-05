# Copyright (c) 2024, hidayat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PDCEntry(Document):
	def before_submit(self):
		if self.clearance_date:
			sales_invoice = frappe.get_doc("Sales Invoice",self.invoice)
			p_entry = frappe.new_doc("Payment Entry")
			# for i in self.accounting:
			p_entry.append("references", {
				'reference_doctype': "Sales Invoice",
				'reference_name': self.invoice,
				"total_amount": sales_invoice.grand_total,
				"outstanding_amount":sales_invoice.outstanding_amount,
				"allocated_amount":self.paid_amount
			})
			p_entry.payment_type = self.pdc_type
			p_entry.posting_date = self.posting_date
			p_entry.mode_of_payment = self.mode_of_payment
			p_entry.party_type = "Customer"
			p_entry.party = self.party
			p_entry.party_name = self.party_name
			p_entry.paid_from = self.account_paid_from
			p_entry.paid_to = self.account_paid_to
			p_entry.paid_from_account_currency = self.paid_from_account_currency
			p_entry.paid_to_account_currency = self.paid_to_account_currency
			p_entry.received_amount = self.paid_amount
			p_entry.paid_amount = self.paid_amount
			p_entry.reference_no = self.reference_no
			p_entry.reference_date = self.reference_date
			p_entry.staidentus = "Draft"
			p_entry.ignore_permissions = True
			p_entry.save()
			# frappe.db.sql("""update `tabPDC Entry`  set payment_entry_reference ="{0}" where name="{1}" """.format(p_entry.name, self.name))
			frappe.msgprint(msg='Payment Entry Created Successfully',
							title='Message',
							indicator='green')
		else:
			frappe.ValidationError()
			frappe.throw("Please Mention the Clearance Date First")
		

	# def on_cancel(self):
	# 	if self.payment_entry_reference:
	# 		sales = frappe.get_doc('Payment Entry', self.payment_entry_reference)
	# 		sales.submit()
	# 		sales.docstatus = 2
	# 		sales.save()
	# 	frappe.msgprint(msg='Payment Entry Canceled Successfully',
	# 					title='Message',
	# 					indicator='red')

