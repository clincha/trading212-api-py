import time

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

    def make_backoff_request(self, url, method='GET', data=None, backoff=30):
        """
        Make a request with a backoff timer for rate limiting.
        :param url: The URL to request.
        :param method: The HTTP method to use (default is GET).
        :param data: The data to send with the request (for POST/PUT).
        :param backoff: The number of seconds to wait before retrying on rate limit.
        :return: The response from the request.
        """
        response = requests.request(method, url, headers=self.headers, json=data)
        if response.status_code == 429:
            print(f"Rate limit exceeded. Retrying after {backoff} seconds...")
            time.sleep(backoff)
            response = requests.request(method, url, headers=self.headers, json=data)
        response.raise_for_status()

        if len(response.text) != 0:
            return response.json()
        return None

    def get_exchanges(self):
        """
        Get a list of available exchanges.
        https://t212public-api-docs.redoc.ly/#operation/exchanges
        :return: A list of exchanges.
        """
        return self.make_backoff_request(
            self.base_url + "equity/metadata/exchanges",
            backoff=30
        )

    def get_instruments(self):
        """
        Get a list of instruments.
        https://t212public-api-docs.redoc.ly/#operation/instruments
        :return: A list of instruments.
        """
        return self.make_backoff_request(
            self.base_url + "equity/metadata/instruments",
            backoff=30
        )

    def get_pies(self):
        """
        Get a list of pies.
        https://t212public-api-docs.redoc.ly/#operation/pies
        :return: A list of pies.
        """
        return self.make_backoff_request(
            self.base_url + "equity/pies",
            backoff=30
        )

    def create_pie(self, pie):
        """
        Create a new pie.
        https://t212public-api-docs.redoc.ly/#operation/create
        :param pie: JSON object representing pie to create. See the API documentation for the required fields.
        :return: The created pie.
        """
        return self.make_backoff_request(
            self.base_url + "equity/pies",
            method='POST',
            data=pie,
            backoff=5
        )

    def get_pie(self, pie_id):
        """
        Get a specific pie by its ID.
        https://t212public-api-docs.redoc.ly/#operation/getDetailed
        :param pie_id: The ID of the pie to retrieve.
        :return: The pie with the specified ID.
        """
        return self.make_backoff_request(
            self.base_url + "equity/pies/{}".format(pie_id),
            backoff=5
        )

    def update_pie(self, pie_id, updated_pie):
        """
        Update an existing pie.
        https://t212public-api-docs.redoc.ly/#operation/update
        :param pie_id: The ID of the pie to update.
        :param updated_pie: JSON object representing the updated pie. See the API documentation for the required fields.
        :return: The updated pie.
        """
        return self.make_backoff_request(
            self.base_url + "equity/pies/{}".format(pie_id),
            method='POST',
            data=updated_pie,
            backoff=5
        )

    def duplicate_pie(self, pie_id, duplicated_pie):
        """
        Duplicate an existing pie.
        https://t212public-api-docs.redoc.ly/#operation/duplicatePie
        :param pie_id: The ID of the pie to duplicate.
        :param duplicated_pie: JSON object representing the fields to change. Must include the 'name' field.
        :return: The duplicated pie.
        """
        return self.make_backoff_request(
            self.base_url + "equity/pies/{}/duplicate".format(pie_id),
            method='POST',
            data=duplicated_pie,
            backoff=5
        )

    def delete_pie(self, pie_id):
        """
        Delete a specific pie by its ID.
        https://t212public-api-docs.redoc.ly/#operation/delete
        :param pie_id: The ID of the pie to delete.
        :return: None if successful, raises HTTPError if the request fails.
        """
        return self.make_backoff_request(
            self.base_url + "equity/pies/{}".format(pie_id),
            method='DELETE',
            backoff=5
        )

    def get_account_cash(self):
        """
        Get the cash balance of the account.
        https://t212public-api-docs.redoc.ly/#operation/accountCash
        :return: The cash balance as a float.
        """
        return self.make_backoff_request(
            self.base_url + "equity/account/cash",
            backoff=2
        )

    def get_account_metadata(self):
        """
        Get metadata about the account.
        https://t212public-api-docs.redoc.ly/#operation/accountMetadata
        :return: A dictionary containing account metadata.
        """
        return self.make_backoff_request(
            self.base_url + "equity/account/info",
            backoff=2
        )

    def get_open_positions(self):
        """
        Get a list of open positions in the account.
        https://t212public-api-docs.redoc.ly/#operation/portfolio
        :return: A list of open positions.
        """
        return self.make_backoff_request(
            self.base_url + "equity/portfolio",
            backoff=5
        )

    def get_position(self, ticker):
        """
        Get details of a specific position by its ticker.
        https://t212public-api-docs.redoc.ly/#operation/positionByTicker
        :param ticker: The ticker symbol of the position to retrieve.
        :return: A dictionary containing the position details.
        """
        return self.make_backoff_request(
            self.base_url + "equity/portfolio/{}".format(ticker),
            backoff=1
        )

    def search_position_by_ticker(self, ticker):
        """
        Search for a position by its ticker.
        https://t212public-api-docs.redoc.ly/#operation/positionByTickerV2
        :param ticker: The ticker symbol to search for.
        :return: A dictionary containing the position details if found, otherwise an empty dictionary.
        """
        return self.make_backoff_request(
            self.base_url + "equity/portfolio/ticker",
            method='POST',
            data={"ticker": ticker},
            backoff=1
        )