import frappe
from frappe import _
from builder_ecommerce.cart import add_new_address, create_party, create_contact, _get_cart_quotation, \
    update_address_with_customer, update_cart_address, add_items_to_quotation, get_party, set_price_list_and_rate, \
    set_taxes, _apply_shipping_rule
from erpnext.selling.doctype.quotation.quotation import _make_sales_order


@frappe.whitelist(allow_guest=True)
def place_order(doc=None, cart_items=None):
    if frappe.session.user == "Guest" and doc:
        doc = frappe.parse_json(doc)
        create_user(data=doc)
        first_name = doc.get("first_name", "")
        last_name = doc.get("last_name", "")
        address_title = f"{first_name} {last_name}".strip()
        doc["address_title"] = address_title
        address = add_new_address(frappe.as_json(doc))

        customer = {
            "customer_name": doc.first_name + " " + doc.last_name,
            "mobile_number": doc.telephone,
            "customer_email_address": doc.email
        }

        party = create_party(doc=customer)
        if party:
            contact = create_contact(doc, party.name)
            quotation = _get_cart_quotation(party=party, contact=contact)
            if address:
                update_address_with_customer(address.name, party.name)
                update_cart_address(address_type=address.address_type, address_name=address.name,
                                    quotation=quotation)

            # if not doc.get('deliver_same'):
            #     required_fields = ['deliver_address_line_1', 'deliver_town', 'deliver_country', 'deliver_postcode',
            #                        'deliver_state', 'phone', 'email_id']
            #
            #     # Ensure required fields are available
            #     missing_fields = [field for field in required_fields if not doc.get(field)]
            #     if missing_fields:
            #         frappe.throw(
            #             _("Missing required fields for delivery address: {0}").format(", ".join(missing_fields)))
            #
            #     deliver_address_json = {
            #         'address_title': address_title,
            #         'address_line1': doc['deliver_address_line_1'],
            #         'address_line2': doc.get('deliver_address_line_2', ''),
            #         'city': doc['deliver_town'],
            #         'country': doc['deliver_country'],
            #         'pincode': doc['deliver_postcode'],
            #         'state': doc['deliver_state'],
            #         'address_type': 'Shipping',
            #         'phone': doc['phone'],
            #         'email_id': doc['email_id']
            #     }
            #
            #     deliver_address = add_new_address(frappe.as_json(deliver_address_json))
            #
            #     if deliver_address:
            #         update_address_with_customer(deliver_address.name, party.name)
            #         update_cart_address(
            #             address_type=deliver_address.address_type,
            #             address_name=deliver_address.name,
            #             quotation=quotation
            #         )
            #     else:
            #         frappe.throw(_("Failed to create the delivery address."))

            cart_items = frappe.parse_json(cart_items) if cart_items else []
            if cart_items:
                add_items_to_quotation(quotation, cart_items)

    else:
        quotation = _get_cart_quotation()
        party = get_party()

    if not quotation:
        frappe.throw(_("Quotation could not be created"))

    set_price_list_and_rate(quotation)
    quotation.run_method("calculate_taxes_and_totals")
    set_taxes(quotation)
    _apply_shipping_rule(party, quotation)

    quotation.flags.ignore_permissions = True
    quotation.submit()

    if quotation.quotation_to == "Lead" and quotation.party_name:
        # company used to create customer accounts
        frappe.defaults.set_user_default("company", quotation.company)

    if not (quotation.shipping_address_name or quotation.customer_address):
        frappe.throw(_("Set Shipping Address or Billing Address"))

    sales_order = frappe.get_doc(
        _make_sales_order(
            quotation.name, ignore_permissions=True
        )
    )
    sales_order.payment_schedule = []

    sales_order.flags.ignore_permissions = True
    sales_order.insert()
    sales_order.submit()

    if hasattr(frappe.local, "cookie_manager"):
        frappe.local.cookie_manager.delete_cookie("cart_count")

    return sales_order.name


def create_user(data):
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if password != confirm_password:
        frappe.throw("Passwords do not match.")

    if len(password) < 8:
        frappe.throw("Password must be at least 8 characters long.")

    user = frappe.get_doc({
        "doctype": "User",
        "first_name": data.get('first_name'),
        "last_name": data.get('last_name'),
        "email": data.get('email_id'),
        "mobile": data.get('mobile'),
        "enabled": 1,
        "user_type": "Website User",
        "new_password": password
    })

    # Insert the user document
    user.insert(ignore_permissions=True)
    frappe.db.commit()
    if user.get("email") and hasattr(frappe.local, "login_manager"):
        frappe.local.login_manager.login_as(user.get("email"))
    return user
