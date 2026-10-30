# Copyright (c) 2026, Gayatri Sutar and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document


class CustomPackingSlip(Document):
    pass


@frappe.whitelist()
def get_delivery_note_items(delivery_note):
    doc = frappe.get_doc("Delivery Note", delivery_note)

    if doc.docstatus != 1:
        frappe.throw("Please select a submitted Delivery Note.")

    items = []

    for item in doc.items:
        # 5. Collect the required fields
        items.append({
            "item_code": item.item_code,
            "item_name": item.item_name,
            "batch_no": item.batch_no,
            "description": item.description,
            "qty": item.qty,
            "total_weight": item.total_weight,
            "stock_uom": item.stock_uom,
            "weight_uom": item.weight_uom,
            "page_break": item.page_break,
            "dn_detail": item.name
        })

    return items