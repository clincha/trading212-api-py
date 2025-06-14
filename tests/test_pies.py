import datetime
import json
import os
import unittest

from trading212 import client
from dotenv import load_dotenv

HELPER_PIE = {
    "name": "Test Pie",
    "icon": "Unicorn",
    "instrumentShares": {
        "RPIl_EQ": 1.0
    },
    "goal": 1000,
    "dividendCashAction": "REINVEST",
    "endDate": "2030-09-10T10:00:00Z"
}


class TestPies(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        token = os.getenv("TOKEN")
        self.client = client.Client(token, demo=True)

    def assert_helper_pie(self, pie):
        """
        Helper function to assert the properties of the helper pie.
        This is used to ensure that the pie has the same properties as the helper pie created.
        """
        self.assertIsInstance(pie, dict)

        self.assertIn('settings', pie)
        self.assertIn('instruments', pie)

        self.assertEqual(pie['settings']['name'], HELPER_PIE['name'])
        self.assertEqual(pie['settings']['icon'], HELPER_PIE['icon'])
        self.assertEqual(pie['instruments'][0]['ticker'], 'RPIl_EQ')
        self.assertEqual(pie['instruments'][0]['expectedShare'], HELPER_PIE['instrumentShares']['RPIl_EQ'])
        self.assertEqual(pie['settings']['goal'], HELPER_PIE['goal'])
        self.assertEqual(pie['settings']['dividendCashAction'], HELPER_PIE['dividendCashAction'])

        # The API does not return the endDate in the same format as the helper pie. Nor does it return the correct time.
        helper_time = datetime.datetime.strptime(HELPER_PIE["endDate"], '%Y-%m-%dT%H:%M:%SZ')
        api_time = datetime.datetime.strptime(pie['settings']['endDate'], '%Y-%m-%dT%H:%M:%S.%f%z')
        self.assertEqual(helper_time.strftime('%Y-%m-%d'), api_time.strftime('%Y-%m-%d'))

    def test_create_pie(self):
        response = self.client.create_pie(HELPER_PIE)

        self.assert_helper_pie(response)

        self.client.delete_pie(response['settings']['id'])

    def test_get_pies(self):
        self.client.create_pie(HELPER_PIE)
        pies = self.client.get_pies()

        self.assertIsInstance(pies, list)

        self.client.delete_pie(pies[0]['id'])

    def test_get_pie(self):
        pie_id = self.client.create_pie(HELPER_PIE)['settings']['id']
        pie = self.client.get_pie(pie_id)

        self.assert_helper_pie(pie)

        self.client.delete_pie(pie_id)

    def test_update_pie(self):
        pie = self.client.create_pie(HELPER_PIE)
        new_pie = {
            "name": "Updated Pie",
            "instrumentShares": {
                "RPIl_EQ": 0.5,
                "AAPL_US_EQ": 0.5
            },
            "goal": 2000,
        }
        updated_pie = self.client.update_pie(pie['settings']['id'], new_pie)

        print(json.dumps(updated_pie, indent=4))

        self.assertEqual(updated_pie['settings']['name'],
                         new_pie['name'])
        self.assertEqual(updated_pie['instruments'][0]['expectedShare'],
                         new_pie['instrumentShares']['RPIl_EQ'])
        self.assertEqual(updated_pie['instruments'][1]['expectedShare'],
                         new_pie['instrumentShares']['AAPL_US_EQ'])
        self.assertEqual(updated_pie['settings']['goal'],
                         new_pie['goal'])

        self.client.delete_pie(pie['settings']['id'])

    def test_duplicate_pie(self):
        pie = self.client.create_pie(HELPER_PIE)
        new_pie = {
            "name": "Duplicated Pie"
        }
        duplicated_pie = self.client.duplicate_pie(pie['settings']['id'], new_pie)

        self.assertEqual(new_pie['name'], duplicated_pie['settings']['name'])

        self.client.delete_pie(pie['settings']['id'])
        self.client.delete_pie(duplicated_pie['settings']['id'])

    def test_delete_pie(self):
        pie = self.client.create_pie(HELPER_PIE)
        response = self.client.delete_pie(pie['settings']['id'])

        self.assertIsNone(response)
