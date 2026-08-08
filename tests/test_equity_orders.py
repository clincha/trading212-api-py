import os
import unittest

import requests
from trading212 import client
from dotenv import load_dotenv

TICKER = "AAPL_US_EQ"
# Far enough below any plausible market price that the order rests instead of filling.
LIMIT_PRICE = 1.0


class TestEquityOrders(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        token = os.getenv("TOKEN")
        self.client = client.Client(token, demo=True)

    def test_get_orders(self):
        orders = self.client.get_orders()

        self.assertIsInstance(orders, list)
        for order in orders:
            self.assertIsInstance(order, dict)
            self.assertIn("id", order)
            self.assertIn("ticker", order)
            self.assertIn("type", order)

    def test_place_and_cancel_limit_order(self):
        order = self.client.place_limit_order(TICKER, 1, LIMIT_PRICE, "GOOD_TILL_CANCEL")

        try:
            self.assertIsInstance(order, dict)
            self.assertEqual(order["ticker"], TICKER)
            self.assertEqual(order["type"], "LIMIT")
            self.assertEqual(order["limitPrice"], LIMIT_PRICE)

            fetched = self.client.get_order(order["id"])
            self.assertEqual(fetched["id"], order["id"])
            self.assertEqual(fetched["ticker"], TICKER)

            pending = self.client.get_orders()
            self.assertIn(order["id"], [item["id"] for item in pending])
        finally:
            self.client.cancel_order(order["id"])

    def test_get_order_not_found(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.get_order(1)
