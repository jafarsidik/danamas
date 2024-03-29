from . import __version__ as app_version
from croniter import croniter
app_name = "danamas"
app_title = "Danamas"
app_publisher = "mjs"
app_description = "Apps Danamas"
app_email = "jeff.sidik@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
fixtures = [
    {"doctype": "Role",
		"filters": {
			"name": [ "in", [
                "Admin Investasi",
                "Admin Pinjaman",
                "Admin Taburi",
                "Head Of Admin & Database",
                "Relationship Manager",
                "Account Officer",
                "PLT. Branch Manager",
                "Human Resources & General Affair",
                "Accountant & Finance",
                "Business Development",
                "BOD",
                "General Operational",
                ] ]
		}
	},
    {"doctype":"Custom DocPerm"},
    {"doctype":"Custom Role"},
    #{"doctype":"Custom Field"},
    {"doctype":"Bank"},
    {"doctype":"Web Form"},
    #{"doctype":"Notification"},
    {"doctype":"Workspace"},
    {"doctype":"Workflow State"},
    {"doctype": "Workflow",
		"filters": {
			"name": [ "in", ["Pengajuan Pinjaman Nasabah"] ]
		}
	},

]
# include js, css files in header of desk.html
# app_include_css = "/assets/danamas/css/danamas.css"
# app_include_js = "/assets/danamas/js/danamas.js"

# include js, css files in header of web template
# web_include_css = "/assets/danamas/css/danamas.css"
# web_include_js = "/assets/danamas/js/danamas.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "danamas/public/scss/website"

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
# 	"methods": "danamas.utils.jinja_methods",
# 	"filters": "danamas.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "danamas.install.before_install"
# after_install = "danamas.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "danamas.uninstall.before_uninstall"
# after_uninstall = "danamas.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "danamas.notifications.get_notification_config"

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

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"danamas.tasks.all"
# 	],
# 	"daily": [
# 		"danamas.tasks.daily"
# 	],
# 	"hourly": [
# 		"danamas.tasks.hourly"
# 	],
# 	"weekly": [
# 		"danamas.tasks.weekly"
# 	],
# 	"monthly": [
# 		"danamas.tasks.monthly"
# 	],
    "cron":{
        "0 15 10 * *":[
            "danamas.taburi.api.createEstatement"
        ],
        #"40 11 19 * *":[
        #    "danamas.taburi.api.createEstatement"
        #],
        # "10 * * * *":[
        #     "danamas.taburi.api.createEstatement"
        # ]
        #"3 7 10 * * ":[
        #    "danamas.taburi.api.createEstatementNotificationWA"
        #]
    }
}

# Testing
# -------

# before_tests = "danamas.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "danamas.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "danamas.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


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
# 	"danamas.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
