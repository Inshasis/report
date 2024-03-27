# Copyright (c) 2024, hidayat and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.data import flt
from pydantic import NoneStrBytes

class PDCEntry(Document):
	def on_cancel(self):
		if self.payment_entry_reference:
			sales = frappe.get_doc('Payment Entry', self.payment_entry_reference)
			sales.submit()
			sales.docstatus = 2
			sales.save()
		frappe.msgprint(msg='Payment Entry Cancelled Successfully',
						title='Message',
						indicator='red')

@frappe.whitelist()
def make_pdc_entry_on_submit(clearance_date,invoice,paid_amount,pdc_type,posting_date,mode_of_payment,party,
							 account_paid_from,account_paid_to,paid_from_account_currency,paid_to_account_currency,
							 reference_no,reference_date,name,bank):
	if clearance_date:
		sales_invoice = frappe.get_doc("Sales Invoice",invoice)
		p_entry = frappe.new_doc("Payment Entry")
		# for i in self.accounting:
		p_entry.append("references", {
			'reference_doctype': "Sales Invoice",
			'reference_name': invoice,
			"total_amount": sales_invoice.grand_total,
			"outstanding_amount":sales_invoice.outstanding_amount,
			"allocated_amount":flt(paid_amount)
		})
		p_entry.payment_type = pdc_type
		p_entry.posting_date = posting_date
		p_entry.mode_of_payment = mode_of_payment
		p_entry.party_type = "Customer"
		p_entry.party = party
		p_entry.party_name = ""
		p_entry.bank = bank
		p_entry.paid_from = account_paid_from
		p_entry.paid_to = account_paid_to
		p_entry.paid_from_account_currency = paid_from_account_currency
		p_entry.paid_to_account_currency = paid_to_account_currency
		p_entry.received_amount = flt(paid_amount)
		p_entry.paid_amount = flt(paid_amount)
		p_entry.reference_no = reference_no
		p_entry.reference_date = reference_date
		p_entry.staidentus = "Draft"
		p_entry.ignore_permissions = True
		p_entry.insert()
		frappe.db.sql("""update `tabPDC Entry` set payment_entry_reference ="{0}" where name="{1}" """.format(p_entry.name, name))
		frappe.msgprint(msg='Payment Entry Created Successfully',
						title='Message',
						indicator='green')
	else:
		frappe.ValidationError()
		frappe.throw("Please Mention the Clearance Date First")