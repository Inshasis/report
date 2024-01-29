# Copyright (c) 2024, Huda Infotech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    conditions, filters = get_conditions(filters)
    columns = get_columns(filters)
    data = get_data(conditions, filters)

    return columns, data

# Define columns for the report
def get_columns(filters):
    columns = [
        {
            "label": _("Inv. Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 140
        },
        {
            "label": _("Sales Inv No."),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 140
        },
        {
            "label": _("Customer Name"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 140
        },
        {
            "label": _("Inv Amount without VAT"),
            "fieldname": "total",
            "fieldtype": "Float",
            "width": 140
        },
        {
            "label": _("VAT"),
            "fieldname": "total_taxes_and_charges",
            "fieldtype": "Float",
            "width": 140
        },
        {
            "label": _("Total Amt of Inv"),
            "fieldname": "grand_total",
            "fieldtype": "Float",
            "width": 140
        },
        {
            "label": _("Cost of Inv"),
            "fieldname": "cost_invoice",
            "fieldtype": "Float",
            "width": 140
        },
        {
            "label": _("Gross/Profit or Loss"),
            "fieldname": "gpl",
            "fieldtype": "Float",
            "width": 140
        },
        {
            "label": _("Per"),
            "fieldname": "per",
            "fieldtype": "Data",
            "width": 140
        },
    ]
    
    
    return columns

# Build conditions based on filters
def get_conditions(filters):
    conditions = ""

    if filters.get("name"):conditions += " AND rv.name = %(name)s"
    if filters.get("customer"):conditions += " AND rv.customer = %(customer)s"

    return conditions, filters

# Fetch data from the database using SQL query
def get_data(conditions, filters):
    data = frappe.db.sql("""
        SELECT rv.name, rv.customer,rv.posting_date, rv.total, rv.total_taxes_and_charges, rv.grand_total
        FROM `tabSales Invoice` rv 
        WHERE 1=1 {conditions}
    """.format(conditions=conditions), filters, as_dict=1)

    return data
