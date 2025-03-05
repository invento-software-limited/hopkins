app_name = "hopkins"
app_title = "Hopkins"
app_publisher = "Invento Software Limited"
app_description = "N\\A"
app_email = "munim@invento.com.bd"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "hopkins",
# 		"logo": "/assets/hopkins/logo.png",
# 		"title": "Hopkins",
# 		"route": "/hopkins",
# 		"has_permission": "hopkins.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/hopkins/css/hopkins.css"
# app_include_js = "/assets/hopkins/js/hopkins.js"

# include js, css files in header of web template
# web_include_css = "/assets/hopkins/css/hopkins.css"
# web_include_js = "/assets/hopkins/js/hopkins.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "hopkins/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "hopkins/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "hopkins.utils.jinja_methods",
# 	"filters": "hopkins.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "hopkins.install.before_install"
# after_install = "hopkins.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "hopkins.uninstall.before_uninstall"
# after_uninstall = "hopkins.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "hopkins.utils.before_app_install"
# after_app_install = "hopkins.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "hopkins.utils.before_app_uninstall"
# after_app_uninstall = "hopkins.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "hopkins.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Item": "hopkins.custom_functions.item.CustomItem",
	"Item Group": "hopkins.custom_functions.item_group.CustomItemGroup",
	"Website Slideshow": "hopkins.custom_functions.website_slideshow.CustomWebsiteSlideshow",
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"hopkins.tasks.all"
# 	],
# 	"daily": [
# 		"hopkins.tasks.daily"
# 	],
# 	"hourly": [
# 		"hopkins.tasks.hourly"
# 	],
# 	"weekly": [
# 		"hopkins.tasks.weekly"
# 	],
# 	"monthly": [
# 		"hopkins.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "hopkins.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "hopkins.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "hopkins.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["hopkins.utils.before_request"]
# after_request = ["hopkins.utils.after_request"]

# Job Events
# ----------
# before_job = ["hopkins.utils.before_job"]
# after_job = ["hopkins.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"hopkins.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    'Builder Page',
    'Builder Project Folder',
    'Builder Settings',
    'Builder Client Script',
    'Builder Page Client Script',
    'Builder Component',
    'Block Template',
    'User Font'
]
