import datetime
import os
import unittest

from trading212 import client
from dotenv import load_dotenv


class TestHistoricalItems(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        token = os.getenv("TOKEN")
        self.client = client.Client(token, demo=True)

    def assert_page(self, page):
        self.assertIsInstance(page, dict)
        self.assertIn("items", page)
        self.assertIn("nextPagePath", page)
        self.assertIsInstance(page["items"], list)

    def test_get_historical_orders(self):
        page = self.client.get_historical_orders()

        self.assert_page(page)
        for order in page["items"]:
            self.assertIn("id", order)
            self.assertIn("ticker", order)
            self.assertIn("status", order)

    def test_get_historical_orders_by_ticker(self):
        page = self.client.get_historical_orders(ticker="AAPL_US_EQ", limit=5)

        self.assert_page(page)
        self.assertLessEqual(len(page["items"]), 5)
        for order in page["items"]:
            self.assertEqual(order["ticker"], "AAPL_US_EQ")

    def test_get_dividends(self):
        page = self.client.get_dividends()

        self.assert_page(page)
        for dividend in page["items"]:
            self.assertIn("ticker", dividend)
            self.assertIn("amount", dividend)
            self.assertIn("paidOn", dividend)

    def test_get_transactions(self):
        page = self.client.get_transactions(limit=5)

        self.assert_page(page)
        self.assertLessEqual(len(page["items"]), 5)
        for transaction in page["items"]:
            self.assertIn("type", transaction)
            self.assertIn("amount", transaction)
            self.assertIn("dateTime", transaction)

    def test_get_exports(self):
        exports = self.client.get_exports()

        self.assertIsInstance(exports, list)
        for export in exports:
            self.assertIn("reportId", export)
            self.assertIn("status", export)
            self.assertIn("dataIncluded", export)

    def test_request_export(self):
        time_to = datetime.datetime.now(datetime.timezone.utc)
        time_from = time_to - datetime.timedelta(days=1)

        export = self.client.request_export(
            time_from.isoformat().replace("+00:00", "Z"),
            time_to.isoformat().replace("+00:00", "Z")
        )

        self.assertIsInstance(export, dict)
        self.assertIn("reportId", export)

        report_ids = [item["reportId"] for item in self.client.get_exports()]
        self.assertIn(export["reportId"], report_ids)
