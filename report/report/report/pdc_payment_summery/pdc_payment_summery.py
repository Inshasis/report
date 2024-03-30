# Copyright (c) 2024, hidayat and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate
from frappe.utils.data import flt

# Function to fetch data for the report
def execute(filters=None):
    conditions, filters = get_conditions(filters)
    columns = get_columns(filters)
    data = get_data(conditions, filters)

    return columns, data

# Define columns for the report
def get_columns(filters):
    columns = [
        {"label": "Customer Name", "fieldname": "party", "fieldtype": "Data","width": 150},
        {"label": "Cheque Date", "fieldname": "reference_date", "fieldtype": "Date","width": 150},
        {"label": "Cheque No", "fieldname": "reference_no", "fieldtype": "Data","width": 200},
        {"label": "Cheque Bank", "fieldname": "bank_name", "fieldtype": "Data","width": 180},
        {"label": "Amount", "fieldname": "paid_amount", "fieldtype": "Currency","width": 180}
    ]
    return columns

def get_conditions(filters):
    conditions = ""

    if filters.get("customer"):conditions += " AND party = %(customer)s"
    if filters.get("supplier"):conditions += " AND party = %(supplier)s"
    
    if filters.get("from_date"):conditions += " AND posting_date >= %(from_date)s"

    if filters.get("to_date"):conditions += " AND posting_date <= %(to_date)s"
    
    if filters.get("bank"):conditions += " AND bank_name = %(bank)s"
    if filters.get("pdc_type"):conditions += " AND pdc_type = %(pdc_type)s"

    return conditions, filters

# Fetch data for the report
def get_data(conditions, filters):
    data = frappe.db.sql("""
        SELECT 
            *
        FROM `tabPDC Entry`
        WHERE docstatus = 1
            {conditions}
        GROUP BY party;

    """.format(conditions=conditions), filters, as_dict=1)
    
    return data
