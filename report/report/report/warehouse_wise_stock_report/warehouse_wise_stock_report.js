// Copyright (c) 2024, Huda Infotech and contributors
// For license information, please see license.txt

// Define filter configuration for the "Warehouse Wise Stock Report" Frappe Query Report
frappe.query_reports["Warehouse Wise Stock Report"] = {
	"filters": [
		{
			"fieldname":"item_code",
			"label":("Item"), // Displayed label for the filter
			"fieldtype":"Link", // Type of the field (Link field, in this case)
			"options":"Item", // Options for the Link field (referencing the "Item" doctype)
		},
	]
};
