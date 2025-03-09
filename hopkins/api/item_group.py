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
        fields=["name", "item_group_name", "custom_route", "custom_description", "image"]
    )

    def get_subcategories(parent_name):
        subcategories = frappe.get_all(
            "Item Group",
            filters={"parent_item_group": parent_name, "custom_publish_to_website": 1},
            fields=["name", "item_group_name", "custom_route", "custom_description", "image"]
        )
        for subcategory in subcategories:
            subcategory["subcategories"] = get_subcategories(subcategory["name"])
        return subcategories

    category_tree = []
    for category in categories:
        category["subcategories"] = get_subcategories(category["name"])
        category_tree.append(category)

    return category_tree


@frappe.whitelist(allow_guest=True)
def search_category(categories, category_route):
    """Recursively searches for a category by its custom_route."""
    if not category_route.startswith("/shop/"):
        category_route = "/shop/" + category_route

    for category in categories:
        if category.get("custom_route") == category_route:
            return category

        if "subcategories" in category and category["subcategories"]:
            found = search_category(category["subcategories"], category_route)
            if found:
                return found
    return None

@frappe.whitelist(allow_guest=True)
def get_products(category_name, page=1, limit=12):
    """Returns paginated products for a given category name and its descendants."""

    # Ensure page and limit are integers
    try:
        page = int(page)
        limit = int(limit)
    except ValueError:
        return {"error": "Invalid page or limit value"}

    if page < 1 or limit < 1:
        return {"error": "Page and limit must be greater than 0"}

    # Fetch category details
    try:
        category = frappe.get_cached_doc("Item Group", category_name)
    except frappe.DoesNotExistError:
        return {"error": "Category not found"}

    # Get descendant categories recursively
    def get_descendant_categories(parent_name):
        """Recursively fetches all descendant categories."""
        subcategories = frappe.get_all(
            "Item Group",
            filters={"parent_item_group": parent_name, "custom_publish_to_website": 1},
            fields=["name"]
        )
        descendants = [subcategory["name"] for subcategory in subcategories]
        for subcategory in subcategories:
            descendants.extend(get_descendant_categories(subcategory["name"]))
        return descendants

    # Fetch all descendant categories including the current category
    descendant_categories = get_descendant_categories(category.name)
    descendant_categories.append(category.name)  # Include the category itself

    # Pagination logic
    offset = (page - 1) * limit

    # Fetch products in the category and its descendants
    products = frappe.get_all(
        "Item",
        filters={
            "item_group": ["in", descendant_categories],
            "custom_publish_to_website": 1
        },
        fields=["name", "item_name", "item_code", "custom_route", "image", "standard_rate"],
        start=offset,
        page_length=limit
    )

    # Return paginated product data
    return {
        "category": {
            "name": category.name,
            "custom_route": category.custom_route,
        },
        "products": products,
        "page": page,
        "limit": limit,
        "total_products": frappe.db.count(
            "Item",
            filters={
                "item_group": ["in", descendant_categories],
                "custom_publish_to_website": 1
            }
        )
    }
