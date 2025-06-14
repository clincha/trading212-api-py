import json
import os
import unittest

from dotenv import load_dotenv

from trading212 import client


class TestAccountData(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        token = os.getenv("TOKEN")
        self.client = client.Client(token, demo=True)

    def test_get_account_cash(self):
        response = self.client.get_account_cash()

        self.assertIn("free", response)
        self.assertIsInstance(response["free"], float)
        self.assertIn("total", response)
        self.assertIsInstance(response["total"], float)
        self.assertIn("result", response)
        self.assertIsInstance(response["result"], float)

    def test_get_account_metadata(self):
        response = self.client.get_account_metadata()

        self.assertIn("id", response)
        self.assertIsInstance(response["id"], int)
        self.assertIn("currencyCode", response)
        self.assertIsInstance(response["currencyCode"], str)
