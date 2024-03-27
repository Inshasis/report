import json
import frappe
from frappe.utils.data import flt, today
from pytz import country_names

@frappe.whitelist()
def create_imei_on_submit(doc, handler=""):
    count = 0.0
    r_count = 0.0
    for item in doc.items:
        # crsn = json.loads(item.custom_reference_serial_number)
        if doc.is_return == 0:
            values = item.custom_reference_serial_number.split('\n')
            for rec in values:
                if rec:
                    # Check if IMEI No with the same name already exists
                    if not frappe.db.exists("IMEI No", rec):
                        imei = frappe.new_doc("IMEI No")
                        imei.name1 = rec  # Assign rec to name1 field
                        imei.posting_date = today()
                        imei.customer = doc.customer
                        imei.reference_type = doc.doctype
                        imei.reference_number = doc.name
                        imei.imei_status = "Activate"
                        imei.ignore_permissions = True
                        imei.save()
                        imei.submit()
                        count = flt(count) + 1.0
                        
                    else:
                        frappe.msgprint(msg=f'IMEI No '+ rec +' already exists.',
                                        title='Warning',
                                        indicator='orange')

        else:
            values = item.custom_reference_serial_number.split('\n')
            for rec in values:
                if rec:
                    name = frappe.db.get_value(
                        'IMEI No', {'name1': rec}, ['name'])
                    if name:
                        r_count = flt(r_count) + 1.0
                        imei = frappe.get_doc('IMEI No', name)
                        imei.reference_type = ""
                        imei.reference_number = ""
                        imei.imei_status = "Deactivate"
                        imei.save(ignore_permissions = True)
            
    if flt(count) != 0.0:
        frappe.msgprint(msg='IMEI No '+ str(count) +' Activate Successfully',
                                        title='Message',
                                        indicator='green')
    if flt(r_count) != 0.0:
        frappe.msgprint(msg='IMEI No '+ str(r_count) +' Deactivate Successfully',
                            title='Message',
                            indicator='red')

def cancel_imei_on_cancel(doc, method):
    count = 0.0
    for item in doc.items:
        values = item.custom_reference_serial_number.split('\n')
        for rec in values:
            if rec:
                name = frappe.db.get_value(
                    'IMEI No', {'name1': rec}, ['name'])
                if name:
                    count = flt(count) + 1.0
                    imei = frappe.get_doc('IMEI No', name)
                    imei.reference_type = ""
                    imei.reference_number = ""
                    imei.imei_status = "Deactivate"
                    imei.save(ignore_permissions = True)
    frappe.msgprint(msg='IMEI No '+ str(count) +' Deactivate Successfully',
                    title='Message',
                    indicator='red')
