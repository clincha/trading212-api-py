# Historical Items

The three history listings are paginated. Each returns a dictionary with an `items` list and a
`nextPagePath`, which is either `None` on the last page or a path carrying the cursor for the next
one. The cursor can be pulled out of that path and passed back in as the `cursor` argument.

The API caps `limit` at 50 items per page and rate limits these endpoints to 6 requests per minute,
so a full history walk is slow by design.

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

**Example:**

```json
{
  "items": [
    {
      "id": 3428956871,
      "parentOrder": 0,
      "ticker": "AAPL_US_EQ",
      "type": "MARKET",
      "status": "FILLED",
      "executor": "API",
      "dateCreated": "2026-08-06T13:42:11.000+03:00",
      "dateModified": "2026-08-06T13:42:12.000+03:00",
      "dateExecuted": "2026-08-06T13:42:12.000+03:00",
      "fillId": 1899234771,
      "fillType": "TOTV",
      "fillPrice": 213.47,
      "fillCost": 213.47,
      "fillResult": 0.0,
      "filledQuantity": 1.0,
      "filledValue": 164.92,
      "orderedQuantity": 1.0,
      "orderedValue": null,
      "limitPrice": null,
      "stopPrice": null,
      "timeValidity": null,
      "taxes": [
        {
          "fillId": "1899234771",
          "name": "CURRENCY_CONVERSION_FEE",
          "quantity": 0.25,
          "timeCharged": "2026-08-06T13:42:12.000+03:00"
        }
      ]
    }
  ],
  "nextPagePath": "/api/v0/equity/history/orders?cursor=3428956871&ticker=AAPL_US_EQ&limit=50"
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
      "reference": "d-19238471",
      "amount": 500.0,
      "dateTime": "2026-07-30T18:24:53.000+03:00"
    }
  ],
  "nextPagePath": "/api/v0/history/transactions?cursor=c3e50994-7d6f-47c0-b3f9-40f8ba1733f6&limit=50"
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
