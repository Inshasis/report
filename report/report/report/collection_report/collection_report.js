// Copyright (c) 2024, hidayat and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Collection Report"] = {
	"filters": [
		{
			"fieldname":"customer",
			"label":("Customer"), 
			"fieldtype":"Link", 
			"options":"Customer", 
		},
		{
			"fieldtype": 'Select',
			"fieldname": 'status',
			"label":('Status'),
			"options": ['', 'Partly Paid', 'Unpaid', 'Unpaid and Discounted', 'Partly Paid and Discounted', 'Overdue and Discounted', 'Overdue']
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Warehouse', txt, {
					is_group:0
				});
			}
		},
	]
};
