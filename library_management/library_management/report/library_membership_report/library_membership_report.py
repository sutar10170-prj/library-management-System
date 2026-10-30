import frappe


def execute(filters=None):
    columns = [
        {
            "label": "Library Member",
            "fieldname": "library_member",
            "fieldtype": "Link",
            "options": "Library Member",
            "width": 180,
        },
        {
            "label": "Full Name",
            "fieldname": "full_name",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": "From Date",
            "fieldname": "from_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "To Date",
            "fieldname": "to_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "Paid",
            "fieldname": "paid",
            "fieldtype": "Check",
            "width": 80,
        },
    ]

    data = frappe.get_all(
        "Library Membership",
        fields=[
            "library_member",
            "full_name",
            "form_date",
            "to_date",
            "paid",
        ],
    )

    return columns, data