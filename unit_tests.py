import unittest
from models.one_item import Item
from models.user import User
from models.user import Request
from models.users_container import Users_container
from main import PurchasesManager


class TestItem(unittest.TestCase):
    def setUp(self):
        self.item_for_tests = Item("a", 1, 1)

    def test_initialization(self):
        self.assertEqual(self.item_for_tests.name, "a")
        self.assertEqual(self.item_for_tests.amount, 1)
        self.assertEqual(self.item_for_tests.price, 1)

    def test_increase_amount(self):
        self.item_for_tests.change_amount(10)
        self.assertEqual(self.item_for_tests.amount, 11)

    def test_decrease_amount_right(self):
        self.item_for_tests.change_amount(10)
        self.item_for_tests.change_amount(-5)
        self.assertEqual(self.item_for_tests.amount, 6)

    def test_decrease_amount_wrong(self):
        self.assertRaises(Exception, self.item_for_tests.change_amount, -10)


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def test_initialization(self):
        self.assertFalse(self.user.items)

    def test_add_one_new_item(self):
        request = Request(item_name="carrot", price_for_one_item=10, item_amount=2)
        self.user.add_item_from_request(request)
        self.assertEqual(self.user.get_different_items_amount(), 1)

    def test_add_some_items(self):
        request1 = Request(item_name="carrot", price_for_one_item=10, item_amount=2)
        request2 = Request(item_name="potatoes", price_for_one_item=5, item_amount=10)
        request3 = Request(item_name="chips", price_for_one_item=50, item_amount=1)
        self.user.add_item_from_request(request1)
        self.user.add_item_from_request(request2)
        self.user.add_item_from_request(request3)
        self.assertEqual(self.user.get_different_items_amount(), 3)

    def test_add_the_same_item(self):
        request1 = Request(item_name="carrot", price_for_one_item=10, item_amount=2)
        request2 = Request(item_name="carrot", price_for_one_item=10, item_amount=10)
        self.user.add_item_from_request(request1)
        self.user.add_item_from_request(request2)
        self.assertEqual(self.user.get_different_items_amount(), 1)
        self.assertEqual(self.user.get_item("carrot").amount, 12)
        self.assertEqual(self.user.get_item("carrot").price, 10)

    def test_add_with_exception(self):
        request1 = Request(item_name="carrot", price_for_one_item=10, item_amount=2)
        request2 = Request(item_name="potatoes", price_for_one_item=5, item_amount=10)
        self.user.add_item_from_request(request1)
        self.user.add_item_from_request(request2)
        self.assertRaises(Exception, self.user.get_item, "carot")


class TestUserContainer(unittest.TestCase):
    def setUp(self):
        self.user_container = Users_container()

    def test_initialization(self):
        self.assertFalse(self.user_container.users)

    def test_add_user(self):
        self.user_container.add_user(User())
        self.user_container.add_user(User())
        self.assertEqual(self.user_container.users_amount(), 2)

    def test_get_user(self):
        user = User()
        request1 = Request(item_name="carrot", price_for_one_item=10, item_amount=2)
        request2 = Request(item_name="potatoes", price_for_one_item=5, item_amount=10)
        user.add_item_from_request(request1)
        user.add_item_from_request(request2)
        self.user_container.add_user(user)
        self.assertEqual(self.user_container.get_user(0).get_different_items_amount(), 2)


class TestPurchasesManager(unittest.TestCase):
    def setUp(self):
        self.manager = PurchasesManager()

    def test_initialization(self):
        self.assertEqual(self.manager.users.users_amount(), 0)

    def test_check_user_id_without_exception(self):
        self.manager.users.add_user(User())
        self.manager.users.add_user(User())
        self.manager.check_user_id(1)

    def test_check_user_id_with_exception(self):
        self.assertRaises(Exception, self.manager.check_user_id, 0)
        self.manager.users.add_user(User())
        self.manager.users.add_user(User())
        self.assertRaises(Exception, self.manager.check_user_id, 2)

    def test_check_item_amount(self):
        self.manager.check_item_amount(12)
        self.assertRaises(Exception, self.manager.check_item_amount, 0)
        self.assertRaises(Exception, self.manager.check_item_amount, -3)

    def test_check_price_for_one_item(self):
        self.manager.check_price_for_one_item(12.123)
        self.manager.check_price_for_one_item(0)
        self.assertRaises(Exception, self.manager.check_price_for_one_item, -3)

    def test_answer_for_request(self):
        request = Request(item_name="carrot", price_for_one_item=10, item_amount=2)
        self.assertEqual("Added items price: 20.0", self.manager.make_answer_for_request(request))

    def test_clear_base(self):
        self.manager.users.add_user(User())
        self.manager.users.add_user(User())
        self.manager.clear_base()
        self.assertEqual(self.manager.users.users_amount(), 0)


if __name__ == "__main__":
    unittest.main()
