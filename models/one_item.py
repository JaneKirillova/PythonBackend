class Item:
    def __init__(self, name="", price=0, amount=0):
        self.name = name
        self.price = price
        self.amount = amount

    def change_amount(self, delta):
        if self.amount + delta < 0:
            raise Exception('Can not change  amount')
        self.amount += delta
