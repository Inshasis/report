# # Copyright (c) 2024, Huda Infotech and contributors
# # For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    conditions, filters = get_conditions(filters)
    columns = get_columns(filters)
    data = get_data(conditions, filters)

    return columns, data

def get_columns(filters):
    columns = [
        {
            "label": _("Item"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 140
        },
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Link",
            "options": "Item",
            "width": 140
        },
        {
            "label": _("Item Group"),
            "fieldname": "item_group",
            "fieldtype": "Link",
            "options": "Item",
            "width": 140
        }
    ]

    # Get warehouse names dynamically and add them as columns
    warehouse_names = get_warehouse_data(filters)

    columns.extend([
        {
            "label": _(warehouse["name"]),  # Use a specific field from the warehouse data
            "fieldname": frappe.scrub(warehouse["name"]),  # Use a specific field from the warehouse data
            "fieldtype": "Float",
            "width": 120
        } for warehouse in warehouse_names
    ])

    # Add columns for valuation rate and total stock quantity
    columns.extend([
        {
            "label": _("Valuation Rate (Finished Goods)"),
            "fieldname": "valuation_rate_finished_goods",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Total Stock Qty"),
            "fieldname": "total_stock_qty",
            "fieldtype": "Float",
            "width": 120
        }
    ])

    return columns

def get_conditions(filters):
    conditions = ""

    if filters.get("item_code"):
        conditions += " AND rv.item_code = %(item_code)s"

    return conditions, filters

def get_data(conditions, filters):
    data = frappe.db.sql("""
        SELECT 
            rv.item_code,
            i.item_name,
            i.item_group,
            rv.warehouse, 
            SUM(rv.actual_qty) as actual_qty,
            item.valuation_rate as valuation_rate_finished_goods
        FROM `tabBin` rv 
        LEFT JOIN `tabWarehouse` rvi ON rvi.name = rv.warehouse 
        LEFT JOIN `tabItem` i ON i.item_code = rv.item_code
        LEFT JOIN `tabBin` item ON item.item_code = rv.item_code and item.warehouse = "Finished Goods - HI" 
        WHERE 1=1 {conditions}
        GROUP BY rv.item_code, rv.warehouse
    """.format(conditions=conditions), filters, as_dict=1)

    formatted_data = format_data(data)
    
    return formatted_data

# Define the function to fetch warehouse data based on filters
def get_warehouse_data(filters):
    conditions = ""
    if filters.get("warehouse"):
        conditions += " AND w.name = %(warehouse)s"
    
    warehouse_data = frappe.db.sql(f"""
        SELECT 
            *
        FROM `tabWarehouse` w
        WHERE 1=1 {conditions}
    """, filters, as_dict=True)

    return warehouse_data


def format_data(data):
    formatted_data = []
    total_stock_qty_dict = {}

    for row in data:
        item_code = row.get("item_code")
        item_name = row.get("item_name")
        item_group = row.get("item_group")
        warehouse = frappe.scrub(row.get("warehouse"))
        actual_qty = row.get("actual_qty")
        valuation_rate_finished_goods = row.get("valuation_rate_finished_goods")

        # Calculate total stock quantity
        total_stock_qty_dict[item_code] = total_stock_qty_dict.get(item_code, 0) + actual_qty
        total_stock_qty = total_stock_qty_dict.get(item_code, 0)

        existing_item = next((item for item in formatted_data if item["item_code"] == item_code), None)

        if existing_item:
            existing_item[item_name] = item_name
            existing_item[item_group] = item_group
            existing_item[warehouse] = actual_qty
            existing_item["total_stock_qty"] = total_stock_qty
            existing_item["valuation_rate_finished_goods"] = valuation_rate_finished_goods 
        else:
            new_item = {
                "item_code": item_code,
                "item_name": item_name,
                "item_group": item_group,
                warehouse: actual_qty,
                "total_stock_qty": total_stock_qty,
                "valuation_rate_finished_goods": valuation_rate_finished_goods
            }
            formatted_data.append(new_item)

    return formatted_data
