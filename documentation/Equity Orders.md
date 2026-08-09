# Equity Orders

Orders are placed against the account the token belongs to. Only market orders are supported on live
accounts while the API is in beta — the other order types work on demo accounts.

Quantity is signed: a positive quantity buys, a negative quantity sells.

`time_validity` controls how long a resting order stays live and accepts `DAY` or `GOOD_TILL_CANCEL`.
It defaults to `DAY`.

A placed order is not immediately readable. `get_order` and `cancel_order` both return 404 for
roughly a second after the placing call has returned the new order's id, so code that places an
order and then acts on it needs to retry rather than assume the id is usable straight away.

The API rejects orders below a minimum value with `min-quantity-exceeded` — the floor is around
1.16 EUR and moves with exchange rates, so `quantity * price` needs headroom above it. Stop prices
more than roughly 30% away from the market price are rejected as `price too far`.

## Get Orders

```python
from trading212 import client

t212 = client.Client("TOKEN")

orders = t212.get_orders()
```

### Returns

A list of the pending orders on the account, each represented as a dictionary. Filled and cancelled
orders are not included — those come from `get_historical_orders`.

**Example:**

```json
[
  {
    "id": 53150556575,
    "strategy": "QUANTITY",
    "type": "LIMIT",
    "ticker": "AAPL_US_EQ",
    "quantity": 1,
    "filledQuantity": 0,
    "limitPrice": 10.0,
    "status": "NEW",
    "currency": "EUR",
    "extendedHours": false,
    "initiatedFrom": "API",
    "side": "BUY",
    "timeInForce": "GOOD_TILL_CANCEL",
    "createdAt": "2026-08-09T08:48:48.878+03:00",
    "instrument": {
      "ticker": "AAPL_US_EQ",
      "name": "Apple",
      "isin": "US0378331005",
      "currency": "USD"
    }
  }
]
```

## Place Limit Order

```python
from trading212 import client

t212 = client.Client("TOKEN")

order = t212.place_limit_order("AAPL_US_EQ", 1, 100.23, "GOOD_TILL_CANCEL")
```

### Input

The ticker of the instrument, the quantity to trade, the limit price the order should fill at or
better than, and optionally the time validity.

### Returns

A dictionary representing the placed order.

**Example:**

```json
{
  "id": 53150556575,
  "strategy": "QUANTITY",
  "type": "LIMIT",
  "ticker": "AAPL_US_EQ",
  "quantity": 1,
  "filledQuantity": 0,
  "limitPrice": 10.0,
  "status": "NEW",
  "currency": "EUR",
  "extendedHours": false,
  "initiatedFrom": "API",
  "side": "BUY",
  "timeInForce": "GOOD_TILL_CANCEL",
  "createdAt": "2026-08-09T08:48:48.878+03:00",
  "instrument": {
    "ticker": "AAPL_US_EQ",
    "name": "Apple",
    "isin": "US0378331005",
    "currency": "USD"
  }
}
```

## Place Market Order

```python
from trading212 import client

t212 = client.Client("TOKEN")

order = t212.place_market_order("AAPL_US_EQ", 1)
```

### Input

The ticker of the instrument and the quantity to trade. Market orders fill immediately while the
market is open, so this method is the one to be careful with on a live account.

### Returns

A dictionary representing the placed order.

**Example:**

```json
{
  "id": 53150556577,
  "strategy": "QUANTITY",
  "type": "MARKET",
  "ticker": "AAPL_US_EQ",
  "quantity": 1,
  "filledQuantity": 0,
  "status": "NEW",
  "currency": "EUR",
  "extendedHours": false,
  "initiatedFrom": "API",
  "side": "BUY",
  "createdAt": "2026-08-09T08:48:51.933+03:00",
  "instrument": {
    "ticker": "AAPL_US_EQ",
    "name": "Apple",
    "isin": "US0378331005",
    "currency": "USD"
  }
}
```

## Place Stop Order

```python
from trading212 import client

t212 = client.Client("TOKEN")

order = t212.place_stop_order("AAPL_US_EQ", -1, 190.0, "GOOD_TILL_CANCEL")
```

### Input

The ticker of the instrument, the quantity to trade, the stop price at which the order is released
to the market, and optionally the time validity.

### Returns

A dictionary representing the placed order.

**Example:**

```json
{
  "id": 53150556579,
  "strategy": "QUANTITY",
  "type": "STOP",
  "ticker": "AAPL_US_EQ",
  "quantity": 1,
  "filledQuantity": 0,
  "stopPrice": 260.0,
  "status": "NEW",
  "currency": "EUR",
  "extendedHours": false,
  "initiatedFrom": "API",
  "side": "BUY",
  "timeInForce": "DAY",
  "createdAt": "2026-08-09T08:48:54.991+03:00",
  "instrument": {
    "ticker": "AAPL_US_EQ",
    "name": "Apple",
    "isin": "US0378331005",
    "currency": "USD"
  }
}
```

## Place Stop Limit Order

```python
from trading212 import client

t212 = client.Client("TOKEN")

order = t212.place_stop_limit_order("AAPL_US_EQ", -1, 188.5, 190.0, "GOOD_TILL_CANCEL")
```

### Input

The ticker of the instrument, the quantity to trade, the limit price, the stop price at which the
order is released to the market, and optionally the time validity.

### Returns

A dictionary representing the placed order.

**Example:**

```json
{
  "id": 53150556581,
  "strategy": "QUANTITY",
  "type": "STOP_LIMIT",
  "ticker": "AAPL_US_EQ",
  "quantity": 1,
  "filledQuantity": 0,
  "limitPrice": 265.0,
  "stopPrice": 260.0,
  "status": "NEW",
  "currency": "EUR",
  "extendedHours": false,
  "initiatedFrom": "API",
  "side": "BUY",
  "timeInForce": "DAY",
  "createdAt": "2026-08-09T08:48:58.052+03:00",
  "instrument": {
    "ticker": "AAPL_US_EQ",
    "name": "Apple",
    "isin": "US0378331005",
    "currency": "USD"
  }
}
```

## Get Order

```python
from trading212 import client

t212 = client.Client("TOKEN")

order = t212.get_order(3428956871)
```

### Input

The ID of a pending order, as returned by `get_orders` or by one of the `place_*_order` methods.

### Returns

A dictionary representing the order. An order that has already filled or been cancelled is no longer
pending and returns a 404.

**Example:**

```json
{
  "id": 53150556575,
  "strategy": "QUANTITY",
  "type": "LIMIT",
  "ticker": "AAPL_US_EQ",
  "quantity": 1,
  "filledQuantity": 0,
  "limitPrice": 10.0,
  "status": "NEW",
  "currency": "EUR",
  "extendedHours": false,
  "initiatedFrom": "API",
  "side": "BUY",
  "timeInForce": "GOOD_TILL_CANCEL",
  "createdAt": "2026-08-09T08:48:48.878+03:00",
  "instrument": {
    "ticker": "AAPL_US_EQ",
    "name": "Apple",
    "isin": "US0378331005",
    "currency": "USD"
  }
}
```

## Cancel Order

```python
from trading212 import client

t212 = client.Client("TOKEN")

t212.cancel_order(3428956871)
```

### Input

The ID of the pending order to cancel.

### Returns

`None`. An unsuccessful cancellation raises an `HTTPError` — 404 if the order is not pending and 400
on a live account, where cancellation is not available during the beta.
