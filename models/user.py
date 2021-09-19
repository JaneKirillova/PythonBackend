from models.one_item import Item
from models.request import Request


class User:
    def __init__(self):
        self.items = dict()

    def add_item_from_request(self, request: Request):
        if request.item_name not in self.items:
            self.items[request.item_name] = Item(request.item_name, request.price_for_one_item, request.item_amount)
        else:
            self.items[request.item_name].change_amount(request.item_amount)

    def get_items_amount(self):
        return len(self.items)

    def get_item(self, item_name):
        return self.items[item_name]

