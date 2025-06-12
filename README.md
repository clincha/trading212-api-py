# trading212-api-py

Python client for Trading212 API.

Creating a client:

```python
from trading212 import client

t212 = client.Client("TOKEN")
```

Once a client is created, you can use it to interact with the Trading212 API.

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

## Create a Pie

Create a JSON object to pass into the create_pie method.

`dividendCashAction` can be one of: REINVEST, TO_ACCOUNT_CASH
`endDate` should be in the format 2019-08-24T14:15:22Z.
`goal` is a string representing the goal amount in the account currency, e.g. "1000".
`icon` is a string representing the icon URL.
`instrumentShares` is a dictionary where keys are instrument IDs and values are the number of shares for each instrument. Instrument IDs can be found in the Trading212 app or website.

```json
{
  "dividendCashAction": "REINVEST",
  "endDate": "2024-12-31",
  "goal": "1000",
  "icon": "string",
  "instrumentShares": {
    "APPL_US_EQ": 10,
    "MSFT_US_EQ": 5
  },
  "name": "Test Pie"
}
```