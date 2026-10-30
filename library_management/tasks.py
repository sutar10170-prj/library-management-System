import frappe
import string
import random


def all():
    pass


def cron():
    print("Creating a random Note")

    letters = string.ascii_letters

    title = "".join(random.choice(letters) for i in range(20))
    note = "".join(random.choice(letters) for i in range(20))

    new_note = frappe.get_doc({
        "doctype": "Notes",
        "title": title,
        "content": note
    })

    new_note.insert()
    frappe.db.commit()

    print("Note inserted successfully")
