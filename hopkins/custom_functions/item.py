from frappe.utils.data import slug
from erpnext.stock.doctype.item.item import Item


class CustomItem(Item):
    def validate(self):
        super().validate()
        if not self.custom_route:
            self.custom_route = "/" + slug(self.item_group) + "/" + slug(self.item_name)
