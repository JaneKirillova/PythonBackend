import unittest
import requests


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:8000'

    def test_integration_add_users(self):
        response = requests.get(self.url)
        self.assertEqual("You are using your purchases tracker", response.text)
        response_clear = requests.get(self.url + "/clear_base")
        self.assertEqual("Base was cleared", response_clear.text)
        response = requests.get(self.url + "/add_user")
        self.assertEqual("User successfully added", response.text)
        requests.get(self.url + "/add_user")
        users_amount = requests.get(self.url + "/users_amount")
        self.assertEqual(int(users_amount.text), 2)

    def test_integration_add_item(self):
        requests.get(self.url + "/clear_base")
        requests.get(self.url + "/add_user")
        request = {"item_name": "carrot", "price_for_one_item": "10", "item_amount": "2"}
        response = requests.post(self.url + "/add_item/0", json=request)
        self.assertEqual("Added items price: 20.0", response.text)
        added_item = requests.get(self.url + "/get_item/0/carrot")
        self.assertEqual('{"name":"carrot","price":10.0,"amount":2}', added_item.text)
        added_items_amount = requests.get(self.url + "/items_amount/0/")
        self.assertEqual("1", added_items_amount.text)

    def test_integration_bad_requests(self):
        requests.get(self.url + "/clear_base")
        requests.get(self.url + "/add_user")
        bad_user_req = requests.get(self.url + "/items_amount/10/")
        self.assertEqual(404, bad_user_req.status_code)
        self.assertEqual('{"detail":"User not found"}', bad_user_req.text)

        bad_item = {"item_name": "carrot", "price_for_one_item": "-10", "item_amount": "2"}
        bad_item_request = requests.post(self.url + "/add_item/0", json=bad_item)
        print(bad_item_request.text)
        self.assertEqual(404, bad_item_request.status_code)
        self.assertEqual('{"detail":"Item price can not be negative"}', bad_item_request.text)


if __name__ == "__main__":
    unittest.main()
