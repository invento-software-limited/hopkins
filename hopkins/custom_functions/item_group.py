from frappe.utils.data import slug
from erpnext.setup.doctype.item_group.item_group import ItemGroup


class CustomItemGroup(ItemGroup):
    def validate(self):
        print("Hello")
        if not self.custom_route:
            self.custom_route = slug(self.item_group_name)
