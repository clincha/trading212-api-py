# Historical Items

The three history listings are paginated. Each returns a dictionary with an `items` list and a
`nextPagePath`, which is either `None` on the last page or a path carrying the cursor for the next
one. The cursor can be pulled out of that path and passed back in as the `cursor` argument.

The API caps `limit` at 50 items per page and rate limits these endpoints to 6 requests per minute,
so a full history walk is slow by design.

The two CSV export calls are **live accounts only**. On a demo account both return 403
`not-available-in-demo-account`, so the tests covering them are skipped and their examples below
come from the API specification rather than a captured response.

## Get Historical Orders

```python
from trading212 import client

t212 = client.Client("TOKEN")

history = t212.get_historical_orders(ticker="AAPL_US_EQ", limit=50)
```

### Input

All arguments are optional: a pagination cursor, a ticker to filter by, and a page size.

### Returns

A page of historical orders. Unlike `get_orders`, this covers orders that have already filled or
been cancelled, and includes fill details and the taxes charged.

Each entry in `items` is a wrapper, not an order: the order itself sits under an `order` key, and an
entry for an order that filled carries a second `fill` key holding the execution price, the trading
method and the taxes charged. Entries for orders that never filled have no `fill` key at all.

**Example:**

```json
{
  "items": [
    {
      "order": {
        "id": 32500210180,
        "strategy": "VALUE",
        "type": "MARKET",
        "ticker": "RPIl_EQ",
        "status": "FILLED",
        "value": 200.0,
        "filledValue": 200.0,
        "currency": "EUR",
        "extendedHours": false,
        "initiatedFrom": "WEB",
        "side": "BUY",
        "createdAt": "2025-06-14T16:22:55.000Z",
        "instrument": {
          "ticker": "RPIl_EQ",
          "name": "Raspberry PI",
          "isin": "GB00BS3DYQ52",
          "currency": "GBX"
        }
      },
      "fill": {
        "id": 32650200365,
        "quantity": 33.4188685,
        "price": 506.5,
        "type": "TRADE",
        "tradingMethod": "OTC",
        "filledAt": "2025-06-16T07:15:03.000Z",
        "walletImpact": {
          "currency": "EUR",
          "netValue": 200.0,
          "fxRate": 85.18699997,
          "taxes": [
            {
              "name": "STAMP_DUTY_RESERVE_TAX",
              "quantity": -1.0,
              "currency": "EUR",
              "chargedAt": "2025-06-16T07:15:03.151Z"
            },
            {
              "name": "CURRENCY_CONVERSION_FEE",
              "quantity": -0.3,
              "currency": "EUR",
              "chargedAt": "2025-06-16T07:15:03.137Z"
            }
          ]
        }
      }
    },
    {
      "order": {
        "id": 53150556569,
        "strategy": "QUANTITY",
        "type": "STOP",
        "ticker": "AAPL_US_EQ",
        "quantity": 1.0,
        "filledQuantity": 0,
        "stopPrice": 260.0,
        "status": "CANCELLED",
        "currency": "EUR",
        "extendedHours": false,
        "initiatedFrom": "API",
        "side": "BUY",
        "createdAt": "2026-08-09T05:43:00.000Z",
        "instrument": {
          "ticker": "AAPL_US_EQ",
          "name": "Apple",
          "isin": "US0378331005",
          "currency": "USD"
        }
      }
    }
  ],
  "nextPagePath": "/api/v0/equity/history/orders?cursor=32500210180&limit=50"
}
```

## Get Dividends

```python
from trading212 import client

t212 = client.Client("TOKEN")

dividends = t212.get_dividends(ticker="AAPL_US_EQ")
```

### Input

All arguments are optional: a pagination cursor, a ticker to filter by, and a page size.

### Returns

A page of dividends paid out to the account. `amount` is in the account currency and
`grossAmountPerShare` is in the instrument currency.

The example below comes from the API specification rather than a captured response — the demo
account this was verified against has never been paid a dividend, so the endpoint returns an
empty `items` list there.

**Example:**

```json
{
  "items": [
    {
      "ticker": "AAPL_US_EQ",
      "reference": "DIV-19238471",
      "type": "ORDINARY",
      "quantity": 12.0,
      "grossAmountPerShare": 0.25,
      "amount": 2.31,
      "amountInEuro": 2.68,
      "paidOn": "2026-08-01T09:00:00.000+03:00"
    }
  ],
  "nextPagePath": null
}
```

## Get Transactions

```python
from trading212 import client

t212 = client.Client("TOKEN")

transactions = t212.get_transactions(time_from="2026-01-01T00:00:00Z")
```

### Input

All arguments are optional: a pagination cursor, an ISO-8601 timestamp to start from, and a page
size. The timestamp argument is named `time_from` here and `time` on the API.

### Returns

A page of money movements into and out of the account — deposits, withdrawals, fees and transfers.
Trades are not transactions; those come from `get_historical_orders`.

**Example:**

```json
{
  "items": [
    {
      "type": "DEPOSIT",
      "amount": 50000.0,
      "currency": "EUR",
      "reference": "920b1a43-b03c-4249-b022-6e160688c532",
      "dateTime": "2019-06-03T18:52:50.000Z"
    }
  ],
  "nextPagePath": null
}
```

## Get Exports

```python
from trading212 import client

t212 = client.Client("TOKEN")

exports = t212.get_exports()
```

### Returns

A list of the CSV exports requested for the account. `downloadLink` is `null` until `status` reaches
`Finished`; the other statuses are `Queued`, `Processing`, `Running`, `Canceled` and `Failed`.

**Example:**

```json
[
  {
    "reportId": 1284471,
    "status": "Finished",
    "downloadLink": "https://trading212equities.s3.eu-central-1.amazonaws.com/report-1284471.csv",
    "timeFrom": "2026-01-01T00:00:00.000Z",
    "timeTo": "2026-08-08T00:00:00.000Z",
    "dataIncluded": {
      "includeDividends": true,
      "includeInterest": true,
      "includeOrders": true,
      "includeTransactions": true
    }
  }
]
```

## Request Export

```python
from trading212 import client

t212 = client.Client("TOKEN")

export = t212.request_export("2026-01-01T00:00:00Z", "2026-08-08T00:00:00Z")
```

### Input

The start and end of the period to export, plus four optional flags choosing what the CSV contains.
All four default to `True`.

### Returns

A dictionary containing the ID of the queued export. Poll `get_exports` until that ID reports
`Finished` to get its download link.

**Example:**

```json
{
  "reportId": 1284471
}
```
