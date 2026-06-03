import frappe


@frappe.whitelist(allow_guest=True)
def get_trusted_clients():
	"""Return a list of trusted clients with their name, logo, and website URL."""
	return frappe.get_all(
		"Trusted Client", fields=["client_name", "logo", "website_url"], order_by="creation desc"
	)


@frappe.whitelist(allow_guest=True)
def get_testimonials():
	"""Return a list of published client testimonials."""
	return frappe.get_all(
		"Client Testimonial",
		filters={"publish_to_website": 1},
		fields=["person_name", "trusted_client", "description"],
		order_by="creation desc",
	)
