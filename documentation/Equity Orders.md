# Equity Orders

Orders are placed against the account the token belongs to. Only market orders are supported on live
accounts while the API is in beta — the other order types work on demo accounts.

Quantity is signed: a positive quantity buys, a negative quantity sells.

`time_validity` controls how long a resting order stays live and accepts `DAY` or `GOOD_TILL_CANCEL`.
It defaults to `DAY`.

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
    "id": 3428956871,
    "ticker": "AAPL_US_EQ",
    "type": "LIMIT",
    "status": "NEW",
    "strategy": "QUANTITY",
    "quantity": 1.0,
    "filledQuantity": 0.0,
    "value": null,
    "filledValue": null,
    "limitPrice": 100.23,
    "stopPrice": null,
    "creationTime": "2026-08-08T10:15:30.000+03:00"
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
  "id": 3428956871,
  "ticker": "AAPL_US_EQ",
  "type": "LIMIT",
  "status": "NEW",
  "strategy": "QUANTITY",
  "quantity": 1.0,
  "filledQuantity": 0.0,
  "value": null,
  "filledValue": null,
  "limitPrice": 100.23,
  "stopPrice": null,
  "creationTime": "2026-08-08T10:15:30.000+03:00"
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
  "id": 3428957004,
  "ticker": "AAPL_US_EQ",
  "type": "MARKET",
  "status": "FILLED",
  "strategy": "QUANTITY",
  "quantity": 1.0,
  "filledQuantity": 1.0,
  "value": null,
  "filledValue": 213.47,
  "limitPrice": null,
  "stopPrice": null,
  "creationTime": "2026-08-08T10:17:02.000+03:00"
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
  "id": 3428957192,
  "ticker": "AAPL_US_EQ",
  "type": "STOP",
  "status": "NEW",
  "strategy": "QUANTITY",
  "quantity": -1.0,
  "filledQuantity": 0.0,
  "value": null,
  "filledValue": null,
  "limitPrice": null,
  "stopPrice": 190.0,
  "creationTime": "2026-08-08T10:19:44.000+03:00"
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
  "id": 3428957338,
  "ticker": "AAPL_US_EQ",
  "type": "STOP_LIMIT",
  "status": "NEW",
  "strategy": "QUANTITY",
  "quantity": -1.0,
  "filledQuantity": 0.0,
  "value": null,
  "filledValue": null,
  "limitPrice": 188.5,
  "stopPrice": 190.0,
  "creationTime": "2026-08-08T10:21:09.000+03:00"
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
  "id": 3428956871,
  "ticker": "AAPL_US_EQ",
  "type": "LIMIT",
  "status": "NEW",
  "strategy": "QUANTITY",
  "quantity": 1.0,
  "filledQuantity": 0.0,
  "value": null,
  "filledValue": null,
  "limitPrice": 100.23,
  "stopPrice": null,
  "creationTime": "2026-08-08T10:15:30.000+03:00"
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
