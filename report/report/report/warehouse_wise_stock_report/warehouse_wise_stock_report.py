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
            "label": _("Item"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 140
        }
    ]

	# Get warehouse names dynamically and add them as columns
    warehouse_names = get_warehouse_data(filters)
    columns.extend([
        {
            "label": _(name),
            "fieldname": frappe.scrub(name),
            "fieldtype": "Float",
            "width": 120
        } for name in warehouse_names
    ])

	# Add a column for total stock quantity
    columns.append({
        "label": _("Total Stock Qty"),
        "fieldname": "total_stock_qty",
        "fieldtype": "Float",
        "width": 120
    })
    
    return columns

# Build conditions based on filters
def get_conditions(filters):
    conditions = ""

    if filters.get("item_code"):
        conditions += " AND rv.item_code = %(item_code)s"

    return conditions, filters

# Fetch data from the database using SQL query
def get_data(conditions, filters):
    data = frappe.db.sql("""
        SELECT rv.item_code, rv.warehouse, SUM(rv.actual_qty) as actual_qty
        FROM `tabBin` rv 
        LEFT JOIN `tabWarehouse` rvi ON rvi.name = rv.warehouse 
        WHERE 1=1 {conditions}
        GROUP BY rv.item_code, rv.warehouse
    """.format(conditions=conditions), filters, as_dict=1)

	# Format the data for report rendering
    formatted_data = format_data(data)

    return formatted_data

# Get warehouse names from the database
def get_warehouse_data(filters):
    warehouse_names = frappe.db.sql_list("SELECT name FROM `tabWarehouse`")
    return warehouse_names

# Format the data for better rendering
def format_data(data):
    formatted_data = []
    total_stock_qty_dict = {}
    for row in data:
        item_code = row.get("item_code")
        warehouse = frappe.scrub(row.get("warehouse"))
        actual_qty = row.get("actual_qty")
        total_stock_qty_dict[item_code] = total_stock_qty_dict.get(item_code, 0) + actual_qty
        total_stock_qty = total_stock_qty_dict.get(item_code, 0)

        existing_item = next((item for item in formatted_data if item["item_code"] == item_code), None)

        if existing_item:
            existing_item[warehouse] = actual_qty
            existing_item["total_stock_qty"] = total_stock_qty
        else:
            new_item = {"item_code": item_code, warehouse: actual_qty, "total_stock_qty": total_stock_qty}
            formatted_data.append(new_item)

    return formatted_data
