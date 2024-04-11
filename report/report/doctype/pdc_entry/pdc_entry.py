# Copyright (c) 2024, hidayat and contributors
# For license information, please see license.txt

import json
from erpnext.accounts.utils import get_outstanding_invoices
import frappe
from frappe.model.document import Document
from frappe.utils.data import flt

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
def make_pdc_entry_on_submit(doc):
	args = json.loads(doc)
	if args.get("clearance_date"):
		p_entry = frappe.new_doc("Payment Entry")
		for item in args.get("pdc_entry_reference"):
			p_entry.append("references", {
				'reference_doctype': item['reference_doctype'],
				'reference_name': item['reference_name'],
				"total_amount": flt(item['total_amount']),
				"outstanding_amount":flt(item['outstanding_amount']),
				"allocated_amount":flt(item['allocated_amount'])
			})

		p_entry.payment_type = args.get("pdc_type")
		p_entry.posting_date = args.get("posting_date")
		p_entry.mode_of_payment = args.get("mode_of_payment")
		p_entry.party_type = args.get("party_type")
		p_entry.party = args.get("party")
		p_entry.party_name = ""
		p_entry.bank = args.get("bank")
		p_entry.paid_from = args.get("account_paid_from")
		p_entry.paid_to = args.get("account_paid_to")
		p_entry.paid_from_account_currency = args.get("paid_from_account_currency")
		p_entry.paid_to_account_currency = args.get("paid_to_account_currency")
		p_entry.received_amount = flt(args.get("paid_amount"))
		p_entry.paid_amount = flt(args.get("paid_amount"))
		p_entry.reference_no = args.get("reference_no")
		p_entry.reference_date = args.get("reference_date")
		p_entry.staidentus = "Draft"
		p_entry.ignore_permissions = True
		p_entry.insert()
		frappe.db.sql("""update `tabPDC Entry` set payment_entry_reference ="{0}" where name="{1}" """.format(p_entry.name, args.get("name")))
		frappe.msgprint(msg='Payment Entry Created Successfully',
						title='Message',
						indicator='green')
	else:
		frappe.ValidationError()
		frappe.throw("Please Mention the Clearance Date First")


@frappe.whitelist()
def get_reference_docs(party_type, party, party_account):
	outstanding_invoices = get_outstanding_invoices(
		party_type,
		party,
		party_account
	)
	return outstanding_invoices