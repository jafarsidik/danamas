import frappe
import requests

from frappe.utils.pdf import get_pdf
from frappe.utils import today,add_to_date
from datetime import datetime # from python std library

@frappe.whitelist(allow_guest=True)
def sendText(**kwargs):
    args = frappe._dict(kwargs)
    url = "https://starsender.online/api/sendText"

    payload={
        'tujuan': args.tujuan,
        'message': args.message
    }
    files=[

    ]
    headers = {
    'apikey': args.apikey
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response.text

@frappe.whitelist(allow_guest=True)
def sendFiles(**kwargs):
    args = frappe._dict(kwargs)
    
    url = "https://starsender.online/api/sendFiles"
    payload={
        'tujuan': args.tujuan,
        'message': args.message,
        'file': args.file
    }

    files=[

    ]

    headers = {
        'apikey': '19c4018fb8e6802e6df74964e67e7026f3ee61c9'#args.apikey
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response.text

@frappe.whitelist(allow_guest=True)
def download_pdf(name):
    response = Response()
    doc = frappe.get_doc("EStatement", name)
    html = frappe.get_print("EStatement", name, "My Print Format", doc=doc)
    frappe.response.filename = f"{name}.pdf"
    frappe.response.filecontent = get_pdf(html)
    frappe.response.type = "download"
    frappe.response.display_content_as = "attachment"
    return 

@frappe.whitelist(allow_guest=True)
def testing():
    start_date = add_to_date(today(), days=-30, as_string=True)
    end_date = add_to_date(today(), days=-1, as_string=True)
    print(start_date+" | "+end_date)

@frappe.whitelist()
def download(name):
  file = frappe.get_doc("File", name)
  frappe.response.filename = file.file_name
  frappe.response.filecontent = file.get_content()
  frappe.response.type = "download"
  frappe.response.display_content_as = "attachment"