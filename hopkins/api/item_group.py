import frappe


@frappe.whitelist(allow_guest=True)
def get_categories():
    categories = frappe.get_all(
        "Item Group",
        filters={
            "parent_item_group": ["in", ["", "All Item Groups"]],
            "custom_publish_to_website": 1,
            "name": ["!=", "All Item Groups"]
        },
        fields=["name", "item_group_name", "custom_route"]
    )

    def get_subcategories(parent_name):
        subcategories = frappe.get_all("Item Group",
                                       filters={"parent_item_group": parent_name, "custom_publish_to_website": 1},
                                       fields=["name", "item_group_name", "custom_route"])
        for subcategory in subcategories:
            subcategory["subcategories"] = get_subcategories(subcategory["name"])
        return subcategories

    category_tree = []
    for category in categories:
        category["subcategories"] = get_subcategories(category["name"])
        category_tree.append(category)

    return category_tree
