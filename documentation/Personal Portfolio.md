# Personal Portfolio

## Get Open Positions

```python
from trading212 import client

t212 = client.Client("TOKEN")

positions = t212.get_open_positions()
```

### Returns

A list of open positions, each represented as a dictionary. Each position contains details such as the instrument, quantity, average price, and current price.

**Example:**

```json
[
  {
    "ticker": "TSLA_US_EQ",
    "quantity": 783.0,
    "averagePrice": 68.99666667,
    "currentPrice": 326.92,
    "ppl": 173484.92,
    "fxPpl": -1212.72,
    "initialFillDate": "2019-06-06T17:49:02.000+03:00",
    "frontend": "SYSTEM",
    "maxBuy": 3511623.0,
    "maxSell": 3512406.0,
    "pieQuantity": 0.0
  }
]
```

## Get Position

```python
from trading212 import client

t212 = client.Client("TOKEN")

position = t212.get_position("TSLA_US_EQ")
```

### Input

The ticker of the instrument for which to retrieve the position. This method is similar to `search_position_by_ticker`, but implemented slightly differently.

### Returns

A dictionary representing the position for the specified instrument, including details such as quantity, average price, and current price.

**Example:**

```json
{
  "ticker": "TSLA_US_EQ",
  "quantity": 783.0,
  "averagePrice": 68.99666667,
  "currentPrice": 326.92,
  "ppl": 173484.92,
  "fxPpl": -1212.72,
  "initialFillDate": "2019-06-06T17:49:02.000+03:00",
  "frontend": "SYSTEM",
  "maxBuy": 3511623.0,
  "maxSell": 3512406.0,
  "pieQuantity": 0.0
}
```

## Search Position by Ticker

```python
from trading212 import client

t212 = client.Client("TOKEN")

position = t212.search_position_by_ticker("TSLA_US_EQ")
```

### Input

The ticker of the instrument for which to retrieve the position. This method is similar to `get_position`, but implemented slightly differently.

### Returns

A dictionary representing the position for the specified instrument, including details such as quantity, average price, and current price.

**Example:**

```json
{
  "ticker": "TSLA_US_EQ",
  "quantity": 783.0,
  "averagePrice": 68.99666667,
  "currentPrice": 326.92,
  "ppl": 173484.92,
  "fxPpl": -1212.72,
  "initialFillDate": "2019-06-06T17:49:02.000+03:00",
  "frontend": "SYSTEM",
  "maxBuy": 3511623.0,
  "maxSell": 3512406.0,
  "pieQuantity": 0.0
}
```