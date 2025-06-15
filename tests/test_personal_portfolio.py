import json
import os
import unittest

from trading212 import client
from dotenv import load_dotenv


class TestPersonalPortfolio(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        token = os.getenv("TOKEN")
        self.client = client.Client(token, demo=True)

    def test_get_open_positions(self):
        positions = self.client.get_open_positions()

        self.assertIsInstance(positions, list)
        for position in positions:
            self.assertIsInstance(position, dict)
            self.assertIn("ticker", position)
            self.assertIn("quantity", position)
            self.assertIn("averagePrice", position)

    def test_search_position_by_ticker(self):
        positions = self.client.search_position_by_ticker("TSLA_US_EQ")

        self.assertIsInstance(positions, dict)
        self.assertEqual(positions["ticker"], "TSLA_US_EQ")

    def test_get_position(self):
        positions = self.client.get_position("TSLA_US_EQ")

        self.assertIsInstance(positions, dict)
        self.assertEqual(positions["ticker"], "TSLA_US_EQ")
