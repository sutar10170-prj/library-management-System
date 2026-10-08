# Copyright (c) 2026, Gayatri Sutar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryMembership(Document):
	def before_submit(self):
		exists= frappe.db.exists(
			"Library Membership",
			{
				"library_member" : self.library_member,
				"docstatus":DocStatus.submitted(),
				"to_date" : (">", self.form_date)
			},
		)
		if exists:
			frappe.throw("There is an acive membership for this member")
			
		loan_period = frappe.db.get_single_value("Library Settings","loan_member")
		self.to_date =frappe.utils.add_days(self.form_date , loan_period or 30)
