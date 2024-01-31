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
            "fieldname": "total_valuation_rate",
            "fieldtype": "Float",
            "width": 140
        },
        {
            "label": _("Gross/Profit or Loss"),
            "fieldname": "gross_profit_or_loss",
            "fieldtype": "Float",
            "width": 140
        },
        {
            "label": _("Percentage"),
            "fieldname": "percentage",
            "fieldtype": "Data",
            "width": 140
        },
    ]
    
    
    return columns

# Build conditions based on filters
def get_conditions(filters):
    conditions = ""

    if filters.get("name"):conditions += " AND si.name = %(name)s"
    if filters.get("customer"):conditions += " AND si.customer = %(customer)s"

    return conditions, filters

# Fetch data from the database using SQL query
def get_data(conditions, filters):
    data = frappe.db.sql("""
        SELECT si.name, si.customer,si.posting_date, si.total, si.total_taxes_and_charges, si.grand_total,
        COALESCE(SUM(item.valuation_rate * sii.qty), 0) as total_valuation_rate
        FROM `tabSales Invoice` si 
        LEFT JOIN `tabSales Invoice Item` sii ON sii.parent = si.name
        LEFT JOIN `tabBin` item ON item.item_code = sii.item_code and item.warehouse = "Finished Goods - HI"
        WHERE 1=1 {conditions}
        GROUP BY si.name, si.customer, si.posting_date, si.total, si.total_taxes_and_charges, si.grand_total
    """.format(conditions=conditions), filters, as_dict=1)

    for row in data:
        if row['total_valuation_rate'] == 0:
            row['gross_profit_or_loss'] = 0.0
        else:
            row['gross_profit_or_loss'] = row['grand_total'] - row['total_valuation_rate']
            

        if row['total_valuation_rate'] == 0:
            row['percentage'] = 0.0
        else:
            per = row['grand_total'] - row['total_valuation_rate']  
            row['percentage'] = per / row['total_valuation_rate'] * 100
            

    return data
    
