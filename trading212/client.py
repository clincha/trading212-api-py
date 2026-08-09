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

    def make_backoff_request(self, url, method='GET', data=None, params=None, backoff=30):
        """
        Make a request with a backoff timer for rate limiting.
        :param url: The URL to request.
        :param method: The HTTP method to use (default is GET).
        :param data: The data to send with the request (for POST/PUT).
        :param params: Query parameters. Entries with a value of None are left off the URL.
        :param backoff: The number of seconds to wait before retrying on rate limit.
        :return: The response from the request.
        """
        response = requests.request(method, url, headers=self.headers, json=data, params=params)
        if response.status_code == 429:
            print(f"Rate limit exceeded. Retrying after {backoff} seconds...")
            time.sleep(backoff)
            response = requests.request(method, url, headers=self.headers, json=data, params=params)
        response.raise_for_status()

        if len(response.text) != 0:
            return response.json()
        return None

    def get_exchanges(self):
        """
        Get a list of available exchanges.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Instrument%20Metadata.md#exchanges
        :return: A list of exchanges.
        """
        return self.make_backoff_request(
            self.base_url + "equity/metadata/exchanges",
            backoff=30
        )

    def get_instruments(self):
        """
        Get a list of instruments.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Instrument%20Metadata.md#instruments
        :return: A list of instruments.
        """
        return self.make_backoff_request(
            self.base_url + "equity/metadata/instruments",
            backoff=30
        )

    def get_pies(self):
        """
        Get a list of pies.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Pies.md#get-pies
        :return: A list of pies.
        """
        return self.make_backoff_request(
            self.base_url + "equity/pies",
            backoff=30
        )

    def create_pie(self, pie):
        """
        Create a new pie.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Pies.md#create-pie
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
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Pies.md#get-pie
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
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Pies.md#update-pie
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
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Pies.md#duplicate-pie
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
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Pies.md#delete-pie
        :param pie_id: The ID of the pie to delete.
        :return: None if successful, raises HTTPError if the request fails.
        """
        return self.make_backoff_request(
            self.base_url + "equity/pies/{}".format(pie_id),
            method='DELETE',
            backoff=5
        )

    def get_orders(self):
        """
        Get a list of all pending orders.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Equity%20Orders.md#get-orders
        :return: A list of pending orders.
        """
        return self.make_backoff_request(
            self.base_url + "equity/orders",
            backoff=5
        )

    def place_limit_order(self, ticker, quantity, limit_price, time_validity="DAY"):
        """
        Place a limit order.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Equity%20Orders.md#place-limit-order
        :param ticker: The ticker of the instrument to trade.
        :param quantity: The quantity to trade. Negative values sell.
        :param limit_price: The price at or better than which the order should fill.
        :param time_validity: How long the order stays live: 'DAY' or 'GOOD_TILL_CANCEL'.
        :return: The placed order.
        """
        return self.make_backoff_request(
            self.base_url + "equity/orders/limit",
            method='POST',
            data={
                "ticker": ticker,
                "quantity": quantity,
                "limitPrice": limit_price,
                "timeValidity": time_validity
            },
            backoff=2
        )

    def place_market_order(self, ticker, quantity):
        """
        Place a market order.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Equity%20Orders.md#place-market-order
        :param ticker: The ticker of the instrument to trade.
        :param quantity: The quantity to trade. Negative values sell.
        :return: The placed order.
        """
        return self.make_backoff_request(
            self.base_url + "equity/orders/market",
            method='POST',
            data={
                "ticker": ticker,
                "quantity": quantity
            },
            backoff=1
        )

    def place_stop_order(self, ticker, quantity, stop_price, time_validity="DAY"):
        """
        Place a stop order.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Equity%20Orders.md#place-stop-order
        :param ticker: The ticker of the instrument to trade.
        :param quantity: The quantity to trade. Negative values sell.
        :param stop_price: The price at which the order is released to the market.
        :param time_validity: How long the order stays live: 'DAY' or 'GOOD_TILL_CANCEL'.
        :return: The placed order.
        """
        return self.make_backoff_request(
            self.base_url + "equity/orders/stop",
            method='POST',
            data={
                "ticker": ticker,
                "quantity": quantity,
                "stopPrice": stop_price,
                "timeValidity": time_validity
            },
            backoff=2
        )

    def place_stop_limit_order(self, ticker, quantity, limit_price, stop_price, time_validity="DAY"):
        """
        Place a stop-limit order.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Equity%20Orders.md#place-stop-limit-order
        :param ticker: The ticker of the instrument to trade.
        :param quantity: The quantity to trade. Negative values sell.
        :param limit_price: The price at or better than which the order should fill once released.
        :param stop_price: The price at which the order is released to the market.
        :param time_validity: How long the order stays live: 'DAY' or 'GOOD_TILL_CANCEL'.
        :return: The placed order.
        """
        return self.make_backoff_request(
            self.base_url + "equity/orders/stop_limit",
            method='POST',
            data={
                "ticker": ticker,
                "quantity": quantity,
                "limitPrice": limit_price,
                "stopPrice": stop_price,
                "timeValidity": time_validity
            },
            backoff=2
        )

    def get_order(self, order_id):
        """
        Get a specific pending order by its ID.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Equity%20Orders.md#get-order
        :param order_id: The ID of the order to retrieve.
        :return: The order with the specified ID.
        """
        return self.make_backoff_request(
            self.base_url + "equity/orders/{}".format(order_id),
            backoff=1
        )

    def cancel_order(self, order_id):
        """
        Cancel a specific pending order by its ID.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Equity%20Orders.md#cancel-order
        :param order_id: The ID of the order to cancel.
        :return: None if successful, raises HTTPError if the request fails.
        """
        return self.make_backoff_request(
            self.base_url + "equity/orders/{}".format(order_id),
            method='DELETE',
            backoff=1
        )

    def get_account_cash(self):
        """
        Get the cash balance of the account.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Account%20Data.md#get-account-cash
        :return: The cash balance as a float.
        """
        return self.make_backoff_request(
            self.base_url + "equity/account/cash",
            backoff=2
        )

    def get_account_metadata(self):
        """
        Get metadata about the account.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Account%20Data.md#get-account-metadata
        :return: A dictionary containing account metadata.
        """
        return self.make_backoff_request(
            self.base_url + "equity/account/info",
            backoff=2
        )

    def get_open_positions(self):
        """
        Get a list of open positions in the account.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Personal%20Portfolio.md#get-open-positions
        :return: A list of open positions.
        """
        return self.make_backoff_request(
            self.base_url + "equity/portfolio",
            backoff=5
        )

    def get_position(self, ticker):
        """
        Get details of a specific position by its ticker.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Personal%20Portfolio.md#get-position
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
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Personal%20Portfolio.md#search-position-by-ticker
        :param ticker: The ticker symbol to search for.
        :return: A dictionary containing the position details if found, otherwise an empty dictionary.
        """
        return self.make_backoff_request(
            self.base_url + "equity/portfolio/ticker",
            method='POST',
            data={"ticker": ticker},
            backoff=1
        )

    def get_historical_orders(self, cursor=None, ticker=None, limit=None):
        """
        Get a page of historical order data.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Historical%20Items.md#get-historical-orders
        :param cursor: Pagination cursor, taken from the 'nextPagePath' of a previous page.
        :param ticker: Only return orders for this ticker.
        :param limit: Number of items to return. The API caps this at 50.
        :return: A dictionary with an 'items' list and a 'nextPagePath'.
        """
        return self.make_backoff_request(
            self.base_url + "equity/history/orders",
            params={"cursor": cursor, "ticker": ticker, "limit": limit},
            backoff=10
        )

    def get_dividends(self, cursor=None, ticker=None, limit=None):
        """
        Get a page of paid out dividends.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Historical%20Items.md#get-dividends
        :param cursor: Pagination cursor, taken from the 'nextPagePath' of a previous page.
        :param ticker: Only return dividends for this ticker.
        :param limit: Number of items to return. The API caps this at 50.
        :return: A dictionary with an 'items' list and a 'nextPagePath'.
        """
        return self.make_backoff_request(
            self.base_url + "history/dividends",
            params={"cursor": cursor, "ticker": ticker, "limit": limit},
            backoff=10
        )

    def get_transactions(self, cursor=None, time_from=None, limit=None):
        """
        Get a page of transactions to and from the account.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Historical%20Items.md#get-transactions
        :param cursor: Pagination cursor, taken from the 'nextPagePath' of a previous page.
        :param time_from: ISO-8601 timestamp to retrieve transactions from.
        :param limit: Number of items to return. The API caps this at 50.
        :return: A dictionary with an 'items' list and a 'nextPagePath'.
        """
        return self.make_backoff_request(
            self.base_url + "history/transactions",
            params={"cursor": cursor, "time": time_from, "limit": limit},
            backoff=10
        )

    def get_exports(self):
        """
        Get a list of the CSV exports requested for the account.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Historical%20Items.md#get-exports
        :return: A list of exports, each with its status and download link.
        """
        return self.make_backoff_request(
            self.base_url + "history/exports",
            backoff=60
        )

    def request_export(self, time_from, time_to, include_dividends=True, include_interest=True,
                       include_orders=True, include_transactions=True):
        """
        Request a CSV export of the account history. The export is queued, so poll get_exports
        until its status is 'Finished' to pick up the download link.
        https://github.com/clincha/trading212-api-py/blob/main/documentation/Historical%20Items.md#request-export
        :param time_from: ISO-8601 timestamp for the start of the exported period.
        :param time_to: ISO-8601 timestamp for the end of the exported period.
        :param include_dividends: Whether to include dividends in the export.
        :param include_interest: Whether to include interest in the export.
        :param include_orders: Whether to include orders in the export.
        :param include_transactions: Whether to include transactions in the export.
        :return: A dictionary containing the 'reportId' of the queued export.
        """
        return self.make_backoff_request(
            self.base_url + "history/exports",
            method='POST',
            data={
                "timeFrom": time_from,
                "timeTo": time_to,
                "dataIncluded": {
                    "includeDividends": include_dividends,
                    "includeInterest": include_interest,
                    "includeOrders": include_orders,
                    "includeTransactions": include_transactions
                }
            },
            backoff=30
        )
