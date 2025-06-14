import os
import unittest

from trading212 import client
from dotenv import load_dotenv


class TestInstrumentMetadata(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        token = os.getenv("TOKEN")
        self.client = client.Client(token, demo=True)

    def test_get_exchanges(self):
        exchanges = self.client.get_exchanges()
        self.assertIsInstance(exchanges, list)

    def test_get_instruments(self):
        instruments = self.client.get_instruments()
        self.assertIsInstance(instruments, list)

