import requests

API_VERSION = "v0"

LIVE_API_URL = "https://live.trading212.com/api/{}/".format(API_VERSION)
DEMO_API_URL = "https://demo.trading212.com/api/{}/".format(API_VERSION)


class Client:

    def __init__(self, token: str, demo: bool = False):
        self.base_url = DEMO_API_URL if demo else LIVE_API_URL
        self.headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }

    def get_exchanges(self):
        """
        Get a list of available exchanges.
        https://t212public-api-docs.redoc.ly/#operation/exchanges
        :return: A list of exchanges.
        """
        response = requests.get(self.base_url + "equity/metadata/exchanges", headers=self.headers)
        response.raise_for_status()
        return response.json()


    def get_instruments(self):
        """
        Get a list of instruments.
        https://t212public-api-docs.redoc.ly/#operation/instruments
        :return: A list of instruments.
        """
        response = requests.get(self.base_url + "equity/metadata/instruments", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_pies(self):
        """
        Get a list of pies.
        https://t212public-api-docs.redoc.ly/#operation/pies
        :return: A list of pies.
        """
        response = requests.get(self.base_url + "equity/pies", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_pie(self, pie):
        """
        Create a new pie.
        https://t212public-api-docs.redoc.ly/#operation/create
        :param pie: JSON object representing pie to create. See the API documentation for the required fields.
        :return: The created pie.
        """
        response = requests.post(self.base_url + "equity/pies", headers=self.headers, json=pie)
        response.raise_for_status()
        return response.json()