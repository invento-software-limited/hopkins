import frappe


class ProductQuery:
    def __init__(self, page=1, limit=100, filters=None):
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
                ip.price_list_rate AS item_price
            FROM `tabItem` i
            LEFT JOIN `tabItem Price` ip ON i.item_code = ip.item_code AND ip.selling = 1
            WHERE {where_clause}
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

        return products


@frappe.whitelist(allow_guest=True)
def get_products():
    query = ProductQuery()
    products = query.get_products(as_dict=True)
    return products
