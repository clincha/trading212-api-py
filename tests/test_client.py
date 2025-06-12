import os
import unittest

from trading212 import client
from dotenv import load_dotenv


class TestClient(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        token = os.getenv("TOKEN")
        self.client = client.Client(token, demo=True)

    def test_init(self):
        # Test with default environment (live)
        live_client = client.Client(token="test_token")
        self.assertEqual(live_client.base_url, "https://live.trading212.com/api/v0/")
        self.assertEqual(live_client.headers['Authorization'], "test_token")
        self.assertEqual(live_client.headers['Content-Type'], 'application/json')

        # Test with live environment
        live_client = client.Client(token="test_token", demo=False)
        self.assertEqual(live_client.base_url, "https://live.trading212.com/api/v0/")
        self.assertEqual(live_client.headers['Authorization'], "test_token")
        self.assertEqual(live_client.headers['Content-Type'], 'application/json')

        # Test with demo environment
        demo_client = client.Client(token="test_token", demo=True)
        self.assertEqual(demo_client.base_url, "https://demo.trading212.com/api/v0/")
        self.assertEqual(demo_client.headers['Authorization'], "test_token")
        self.assertEqual(demo_client.headers['Content-Type'], 'application/json')

    def test_get_exchanges(self):
        exchanges = self.client.get_exchanges()
        self.assertIsInstance(exchanges, list)

    def test_get_instruments(self):
        instruments = self.client.get_instruments()
        self.assertIsInstance(instruments, list)

    def test_get_pies(self):
        pies = self.client.get_pies()
        self.assertIsInstance(pies, list)

    def test_create_pie(self):
        pie = {
            "dividendCashAction": "REINVEST",
            "endDate": "2024-12-31",
            "goal": "1000",
            "icon": "string",
            "instrumentShares": {
                "APPL_US_EQ": 10,
                "MSFT_US_EQ": 5
            },
            "name": "Test Pie",
        }
        response = self.client.create_pie(pie)
        self.assertIsInstance(response, dict)
