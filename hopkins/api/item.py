import frappe


class ProductQuery:
    def __init__(self, page=1, limit=50000, filters=None):
        offset = (page - 1) * limit
        self.start = offset
        self.page_length = limit
        self.page = page
        self.filters = filters

    def validate_page(self):
        try:
            self.page = int(self.page)
            limit = int(self.page_length)
        except ValueError:
            return {"error": "Invalid page or limit value"}

        if self.page < 1 or limit < 1:
            return {"error": "Page and limit must be greater than 0"}

    def get_filters(self):
        conditions = []
        values = []

        if not self.filters:
            return "1=1", values

        for field, condition in self.filters.items():
            if isinstance(condition, list) and condition[0].lower() in ["in", "not in"]:
                operator = condition[0].upper()
                placeholders = ", ".join(["%s"] * len(condition[1]))
                conditions.append(f"{field} {operator} ({placeholders})")
                values.extend(condition[1])
            elif isinstance(condition, list) and len(condition) == 2:
                operator = condition[0]
                conditions.append(f"{field} {operator} %s")
                values.append(condition[1])
            else:
                conditions.append(f"{field} = %s")
                values.append(condition)

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        return where_clause, values

    def get_query(self):
        where_clause, values = self.get_filters()
        query = f"""
            SELECT
                i.name,
                i.item_name,
                i.item_code,
                i.custom_route,
                i.image,
                i.standard_rate,
                i.custom_oem_part_no,
                i.description,
                ip.price_list_rate AS item_price
            FROM `tabItem` i
            LEFT JOIN `tabItem Price` ip ON i.item_code = ip.item_code AND ip.selling = 1
            WHERE {where_clause}
            ORDER BY i.creation ASC
            LIMIT %s OFFSET %s
        """

        values.extend([self.page_length, self.start])
        return query, values

    def get_products(self, as_dict=False):
        query, values = self.get_query()
        products = frappe.db.sql(query, values, as_dict=as_dict)
        default_currency = frappe.defaults.get_global_default("currency")

        for product in products:
            currency = product.get("item_currency", default_currency)
            product["standard_rate"] = frappe.utils.fmt_money(product["item_price"], currency=currency)
            if not product.get("image"):
                product['image'] = '/assets/hopkins/img/no-image-250x250.png'

        return products


@frappe.whitelist(allow_guest=True)
def get_products():
    query = ProductQuery()
    products = query.get_products(as_dict=True)
    return products


@frappe.whitelist(allow_guest=True)
def get_product():
    category_route = frappe.form_dict.get('category_route')
    item_route = frappe.form_dict.get('item_route')

    route = '/shop/' + category_route + '/' + item_route
    filters = {
        "custom_publish_to_website": 1,
        "custom_route": route,
    }
    query = ProductQuery(filters=filters, limit=1)
    products = query.get_products(as_dict=True)
    if len(products) > 0:
        return products[0]
    else:
        return None


@frappe.whitelist(allow_guest=True)
def get_similar_products(category):
    filters = {
        "custom_publish_to_website": 1,
        "item_group": category.get('name') if category else "",
    }
    query = ProductQuery(filters=filters, limit=5)
    products = query.get_products(as_dict=True)
    return products
