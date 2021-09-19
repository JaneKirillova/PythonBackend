class Item():
    def __init__(self, name, price, amount):
        self.name = name
        self.price = price
        self.amount = amount

    def change_amount(self, delta):
        self.amount += delta