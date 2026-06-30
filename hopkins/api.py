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


@frappe.whitelist(allow_guest=True)
def get_products(page: int = 1, page_length: int = 8, search: str | None = None, category: str | None = None):
	import math

	from invento_webshop.webshop_functions.items import ProductQuery

	try:
		page = int(page)
		page_length = int(page_length)
	except ValueError:
		page = 1
		page_length = 8

	start = (page - 1) * page_length

	pq = ProductQuery()
	res = pq.query(filters={"page_length": page_length}, search_term=search, start=start, item_group=category)

	items = res.get("items", [])
	total_count = res.get("items_count", 0)
	total_pages = math.ceil(total_count / page_length) if total_count else 1

	products = []
	for item in items:
		price = item.get("price_list_rate") or 0.0
		products.append(
			{
				"item_code": item.item_code,
				"item_name": item.item_name,
				"image": item.image or "https://placehold.co/400x300",
				"description": item.description,
				"price": price,
				"price_formatted": f"£{price:,.2f}",
				"stock_code_formatted": f"Stock Code: {item.item_code}",
			}
		)

	return {
		"products": products,
		"total_pages": total_pages,
		"current_page": page,
		"total_products": total_count,
	}
