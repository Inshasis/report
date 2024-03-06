// Copyright (c) 2024, hidayat and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Collection Report"] = {
	"filters": [
		{
			"fieldname":"customer",
			"label":("Customer"), // Displayed label for the filter
			"fieldtype":"Link", // Type of the field (Link field, in this case)
			"options":"Customer", // Options for the Link field (referencing the "Item" doctype)
		},
	]
};
