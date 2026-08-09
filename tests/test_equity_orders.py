import os
import time
import unittest

import requests
from trading212 import client
from dotenv import load_dotenv

TICKER = "AAPL_US_EQ"
# Far enough below any plausible market price that the order rests instead of filling, while
# still clearing the minimum order value the API enforces (~1.16 EUR, an FX-converted floor).
LIMIT_PRICE = 10.0
# Stop prices are rejected as "price too far" beyond roughly 30% from the market price.
STOP_PRICE = 260.0
STOP_LIMIT_PRICE = 265.0


class TestEquityOrders(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        token = os.getenv("TOKEN")
        self.client = client.Client(token, demo=True)

    def await_order(self, order_id, attempts=10):
        """The API returns an order id before that order can be fetched or cancelled; both
        404 for about a second afterwards. Poll until it lands so cancellation cannot leak a
        resting order onto the account."""
        for _ in range(attempts):
            try:
                return self.client.get_order(order_id)
            except requests.exceptions.HTTPError:
                time.sleep(1)
        self.fail("order {} never became visible".format(order_id))

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
            fetched = self.await_order(order["id"])

            self.assertIsInstance(order, dict)
            self.assertEqual(order["ticker"], TICKER)
            self.assertEqual(order["type"], "LIMIT")
            self.assertEqual(order["limitPrice"], LIMIT_PRICE)

            self.assertEqual(fetched["id"], order["id"])
            self.assertEqual(fetched["ticker"], TICKER)

            pending = self.client.get_orders()
            self.assertIn(order["id"], [item["id"] for item in pending])
        finally:
            self.client.cancel_order(order["id"])

    def test_place_and_cancel_stop_order(self):
        order = self.client.place_stop_order(TICKER, 1, STOP_PRICE, "GOOD_TILL_CANCEL")

        try:
            self.await_order(order["id"])
            self.assertEqual(order["ticker"], TICKER)
            self.assertEqual(order["type"], "STOP")
            self.assertEqual(order["stopPrice"], STOP_PRICE)
        finally:
            self.client.cancel_order(order["id"])

    def test_place_and_cancel_stop_limit_order(self):
        order = self.client.place_stop_limit_order(
            TICKER, 1, STOP_LIMIT_PRICE, STOP_PRICE, "GOOD_TILL_CANCEL"
        )

        try:
            self.await_order(order["id"])
            self.assertEqual(order["ticker"], TICKER)
            self.assertEqual(order["type"], "STOP_LIMIT")
            self.assertEqual(order["stopPrice"], STOP_PRICE)
            self.assertEqual(order["limitPrice"], STOP_LIMIT_PRICE)
        finally:
            self.client.cancel_order(order["id"])

    def test_get_order_not_found(self):
        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.get_order(1)
