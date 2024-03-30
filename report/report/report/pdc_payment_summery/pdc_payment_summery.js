// Copyright (c) 2024, hidayat and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PDC Payment Summery"] = {
	"filters": [
		{
            "fieldname": "pdc_type",
            "label": __("PDC Type"),
            "fieldtype": "Select",
            "options": ["", "Receive", "Pay"],
            "on_change": function() {
                var pdc_type = frappe.query_report.get_filter_value('pdc_type');
                var customer_filter = frappe.query_report.get_filter('customer');
                var supplier_filter = frappe.query_report.get_filter('supplier');

                if (pdc_type === 'Receive') {
                   
                    customer_filter.df.hidden = 0;
                    customer_filter.refresh();
                    
                    supplier_filter.df.hidden = 1;
                    supplier_filter.refresh();
                   
                    frappe.query_report.set_filter_value('supplier', '');
                } else if (pdc_type === 'Pay') {
                    
                    supplier_filter.df.hidden = 0;
                    supplier_filter.refresh();
    
                    customer_filter.df.hidden = 1;
                    customer_filter.refresh();
                    frappe.query_report.set_filter_value('customer', '');
                } else {
                    customer_filter.df.hidden = 1;
                    customer_filter.refresh();
                    supplier_filter.df.hidden = 1;
                    supplier_filter.refresh();
                    frappe.query_report.set_filter_value('customer', '');
                    frappe.query_report.set_filter_value('supplier', '');
                }
            }
        },
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "hidden": 1 
        },
        {
            "fieldname": "supplier",
            "label": __("Supplier"),
            "fieldtype": "Link",
            "options": "Supplier",
            "hidden": 1 
        },
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname":"bank",
			"label": __("Bank"),
			"fieldtype": "Link",
			"options":"Bank"
		},
	]
};
