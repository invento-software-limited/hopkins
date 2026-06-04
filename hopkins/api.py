import frappe


@frappe.whitelist(allow_guest=True)
def submit_inquiry(name, email, company, enquiry_type, country, message):
	doc = frappe.get_doc(
		{
			"doctype": "Lead",
			"lead_name": name,
			"email_id": email,
			"company_name": company,
			"country": country,
		}
	)
	doc.insert(ignore_permissions=True)

	# Add note for enquiry type & message
	doc.add_comment("Comment", text=f"Type: {enquiry_type}\nMessage: {message}")
	return {"status": "success"}


@frappe.whitelist(allow_guest=True)
def subscribe_newsletter(email, first_name=None):
	email_group_name = "Newsletter"

	# 1. Create the Email Group if it doesn't exist yet
	if not frappe.db.exists("Email Group", email_group_name):
		group_doc = frappe.get_doc({"doctype": "Email Group", "title": email_group_name})
		group_doc.insert(ignore_permissions=True)

	# 2. Check if already subscribed
	if frappe.db.exists("Email Group Member", {"email_group": email_group_name, "email": email}):
		return {"status": "already_subscribed", "message": "You are already subscribed!"}

	# 3. Insert the new subscriber
	member_doc = frappe.get_doc(
		{"doctype": "Email Group Member", "email_group": email_group_name, "email": email, "unsubscribed": 0}
	)
	member_doc.insert(ignore_permissions=True)

	return {"status": "success", "message": "Thank you for subscribing!"}
