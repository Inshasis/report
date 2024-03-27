from . import __version__ as app_version

app_name = "report"
app_title = "Report"
app_publisher = "hidayat"
app_description = "Report"
app_email = "hidayat@inshasis.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/report/css/report.css"
# app_include_js = "/assets/report/js/report.js"

# include js, css files in header of web template
# web_include_css = "/assets/report/css/report.css"
# web_include_js = "/assets/report/js/report.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "report/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "report.utils.jinja_methods",
#	"filters": "report.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "report.install.before_install"
# after_install = "report.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "report.uninstall.before_uninstall"
# after_uninstall = "report.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "report.utils.before_app_install"
# after_app_install = "report.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "report.utils.before_app_uninstall"
# after_app_uninstall = "report.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "report.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Delivery Note": {
		"on_submit": "report.utils.delivery_note.create_imei_on_submit",
        "on_cancel": "report.utils.delivery_note.cancel_imei_on_cancel"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"report.tasks.all"
#	],
#	"daily": [
#		"report.tasks.daily"
#	],
#	"hourly": [
#		"report.tasks.hourly"
#	],
#	"weekly": [
#		"report.tasks.weekly"
#	],
#	"monthly": [
#		"report.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "report.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "report.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "report.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["report.utils.before_request"]
# after_request = ["report.utils.after_request"]

# Job Events
# ----------
# before_job = ["report.utils.before_job"]
# after_job = ["report.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"report.auth.validate"
# ]
