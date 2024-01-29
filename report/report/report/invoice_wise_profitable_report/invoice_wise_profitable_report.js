// Copyright (c) 2024, Huda Infotech and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Invoice Wise Profitable Report"] = {
	"filters": [
		{
			"fieldname":"name",
			"label":("Invoice"), // Displayed label for the filter
			"fieldtype":"Link", // Type of the field (Link field, in this case)
			"options":"Sales Invoice", // Options for the Link field (referencing the "Item" doctype)
		},
		{
			"fieldname":"customer",
			"label":("Customer"), // Displayed label for the filter
			"fieldtype":"Link", // Type of the field (Link field, in this case)
			"options":"Customer", // Options for the Link field (referencing the "Item" doctype)
		}
	]
};
