# Instrument Metadata

## Exchanges

### Get Exchanges

```python
from trading212 import client

t212 = client.Client("TOKEN")

exchanges = t212.get_exchanges()
```

#### Returns

A list of exchanges, each represented as a dictionary. Each exchange contains a list workingSchedule objects which in turn contain timeEvents. Each timeEvent has a date and a type (OPEN or CLOSE).

**Example:**

```json
[
  {
    "id": 42,
    "name": "London Stock Exchange",
    "workingSchedules": [
      {
        "id": 70,
        "timeEvents": [
          {
            "date": "2025-05-27T07:00:31.000Z",
            "type": "OPEN"
          },
          {
            "date": "2025-05-27T15:30:00.000Z",
            "type": "CLOSE"
          }
        ]
      }
    ]
  }
]
```

## Instruments

### Get Instruments

```python
from trading212 import client

t212 = client.Client("TOKEN")

instruments = t212.get_instruments()
```

#### Returns

A list of instruments, each represented as a dictionary.

**Example:**

```json
[
  {
    "ticker": "RPIl_EQ",
    "type": "STOCK",
    "workingScheduleId": 55,
    "isin": "GB00BS3DYQ52",
    "currencyCode": "GBX",
    "name": "Raspberry PI ",
    "shortName": "RPI",
    "minTradeQuantity": 0.3,
    "maxOpenQuantity": 23660.0,
    "addedOn": "2024-06-11T09:55:40.000+03:00"
  }
]
```

