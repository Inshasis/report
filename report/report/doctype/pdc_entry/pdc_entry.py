# Copyright (c) 2024, hidayat and contributors
# For license information, please see license.txt

import json
from erpnext.accounts.doctype.account.account import get_account_currency
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_dimensions
from erpnext.accounts.utils import get_outstanding_invoices
from erpnext.controllers.accounts_controller import get_supplier_block_status
import frappe
from frappe import ValidationError, _, qb, scrub, throw
from frappe.model.document import Document
from frappe.utils.data import flt, getdate, nowdate
from pydantic import NoneStrBytes
from frappe import _, scrub

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
	# party_type = ""
	# invoice_type = ""
	# if args.get("pdc_type") == "Receive":
	# 	party_type = "Customer"
	# 	invoice_type = "Sales Invoice"
	# else:
	# 	party_type = "Supplier"
	# 	invoice_type = "Purchase Invoice"
	if args.get("clearance_date"):
		# invoice = frappe.get_doc(invoice_type,args.get("invoice"))
		p_entry = frappe.new_doc("Payment Entry")
		# for i in args.get("accounting:
		p_entry.append("references", {
			'reference_doctype': args.get("reference_doctype"),
			'reference_name': args.get("reference_name"),
			"total_amount": flt(args.get("total_amount")),
			"outstanding_amount":flt(args.get("outstanding_amount")),
			"allocated_amount":flt(args.get("allocated_amount"))
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
def get_reference_docs(args,party_account):
	args = json.loads(args)
	party_type = ""
	if args.get("pdc_type") == "Receive":
		party_type = "Customer"
	else:
		party_type = "Supplier"

	outstanding_invoices = get_outstanding_invoices(
		party_type,
		args.get("party"),
		party_account
	)
	return outstanding_invoices