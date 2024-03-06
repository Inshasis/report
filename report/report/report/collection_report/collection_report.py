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
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer"},
        {"label": "Credit Limit", "fieldname": "credit_limit", "fieldtype": "Currency"},
        {"label": "Credit Limit Date", "fieldname": "credit_limit_date", "fieldtype": "Data"},
        {"label": "Used Credit Limit", "fieldname": "used_credit_limit", "fieldtype": "Currency"},
        {"label": "Available Credit Limit", "fieldname": "available_credit_limit", "fieldtype": "Currency"},
        {"label": "Total Due", "fieldname": "total_due", "fieldtype": "Currency"},
        {"label": ("0-30 Days"), "fieldname": "0-30 days", "fieldtype": "Currency", "width": 120},
        {"label": ("31-60 Days"), "fieldname": "31-60 days", "fieldtype": "Currency", "width": 120},
        {"label": ("61-90 Days"), "fieldname": "61-90 days", "fieldtype": "Currency", "width": 120},
        {"label": ("91-120 Days"), "fieldname": "91-120 days", "fieldtype": "Currency", "width": 120},
        {"label": ("120-360 Days"), "fieldname": "120-360 days", "fieldtype": "Currency", "width": 120},
        {"label": ("Above Days"), "fieldname": "above days", "fieldtype": "Currency", "width": 120},
        {"label": "PDC Amount", "fieldname": "pdc_amount", "fieldtype": "Currency"}
    ]
    return columns

def get_conditions(filters):
    conditions = ""

    if filters.get("customer"):conditions += " AND si.customer = %(customer)s"

    return conditions, filters
# Fetch data for the report
def get_data(conditions,filters):
    data = frappe.db.sql("""
        SELECT 
            si.customer,
            ccl.credit_limit,
            SUM(si.outstanding_amount) as used_credit_limit,
            SUM(CASE WHEN DATEDIFF(CURDATE(), si.due_date) BETWEEN 0 AND 30 THEN si.outstanding_amount ELSE 0 END) AS `0-30 days`,
            SUM(CASE WHEN DATEDIFF(CURDATE(), si.due_date) BETWEEN 31 AND 60 THEN si.outstanding_amount ELSE 0 END) AS `31-60 days`,
            SUM(CASE WHEN DATEDIFF(CURDATE(), si.due_date) BETWEEN 61 AND 90 THEN si.outstanding_amount ELSE 0 END) AS `61-90 days`,
            SUM(CASE WHEN DATEDIFF(CURDATE(), si.due_date) BETWEEN 91 AND 120 THEN si.outstanding_amount ELSE 0 END) AS `91-120 days`,
            SUM(CASE WHEN DATEDIFF(CURDATE(), si.due_date) BETWEEN 121 AND 360 THEN si.outstanding_amount ELSE 0 END) AS `120-360 days`,
            SUM(CASE WHEN DATEDIFF(CURDATE(), si.due_date) > 360 THEN si.outstanding_amount ELSE 0 END) AS `above days`
        FROM `tabSales Invoice` si 
        LEFT JOIN `tabSales Invoice Item` sii ON sii.parent = si.name
        LEFT JOIN `tabCustomer` c ON si.customer = c.name
        LEFT JOIN `tabCustomer Credit Limit` ccl ON c.name = ccl.parent
        WHERE 1=1 {conditions}
        GROUP BY si.customer;

    """.format(conditions=conditions), filters, as_dict=1)
    for row in data:
        row['credit_limit_date'] = "30 Days"
        row['total_due'] = flt(row['used_credit_limit'])
        acl = flt(row['credit_limit']) - flt(row['used_credit_limit'])
        if acl >= 0.0:
            row['available_credit_limit'] = flt(acl)
        else:
            row['available_credit_limit'] = 0.0
                  
    return data