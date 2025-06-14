# Pies

## Get Pies

```python
from trading212 import client

t212 = client.Client("TOKEN")

pies = t212.get_pies()
```

### Returns

An array of pie objects, each containing details about the pie, such as its ID, cash balance, dividend details, and investment results.

**Example:**

```json
[
  {
    "id": 4617385,
    "cash": 0.0,
    "dividendDetails": {
      "gained": 0.0,
      "reinvested": 0.0,
      "inCash": 0.0
    },
    "result": {
      "priceAvgInvestedValue": 0,
      "priceAvgValue": 0,
      "priceAvgResult": 0,
      "priceAvgResultCoef": 0
    },
    "progress": null,
    "status": null
  }
]
```

## Create Pie

```python
from trading212 import client
import datetime

t212 = client.Client("TOKEN")

time = datetime.datetime.now() + datetime.timedelta(weeks=1)
timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ")

pie = {
    "name": "Test Pie",
    "icon": "string",
    "instrumentShares": {
        "RPIl_EQ": 1
    },
    "goal": "1000",
    "dividendCashAction": "REINVEST",
    "endDate": timestamp,
}

pie = t212.create_pie(pie)
```

### Input

JSON object representing a pie.

| Field              | Type   | Description                                                            | Example                             |
|--------------------|--------|------------------------------------------------------------------------|-------------------------------------|
| name               | string | Name of the pie.                                                       | Test                                |
| dividendCashAction | string | Action to take with dividends, can be "REINVEST" or "TO_ACCOUNT_CASH". | REINVEST                            |
| endDate            | string | End date for the pie in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).        | 2025-06-19F12:05:08Z                |
| goal               | string | Goal amount in the account currency.                                   | 1000                                |
| icon               | string | URL of the icon for the pie.                                           | Unicorn                             |
| instrumentShares   | object | Dictionary of instrument IDs and their corresponding target weight.    | {"RPIl_EQ": 0.5, "NVDA_US_EQ": 0.5} |

### Returns

A dictionary representing the created pie, including its settings and instrument list.

**Example**

```json
{
  "instruments": [
    {
      "ticker": "RPIl_EQ",
      "result": {
        "priceAvgInvestedValue": 0,
        "priceAvgValue": 0,
        "priceAvgResult": 0,
        "priceAvgResultCoef": 0
      },
      "expectedShare": 1.0,
      "currentShare": 0,
      "ownedQuantity": 0.0,
      "issues": []
    }
  ],
  "settings": {
    "id": 1234567,
    "instrumentShares": null,
    "name": "Tester",
    "icon": null,
    "goal": 1000,
    "creationDate": 1749732446.569772,
    "endDate": "2025-07-10T23:59:59.999+03:00",
    "initialInvestment": null,
    "dividendCashAction": "REINVEST",
    "publicUrl": null
  }
}
```

## Get Pie

```python
from trading212 import client

t212 = client.Client("TOKEN")

pie = t212.get_pie(4617385)
```

### Input

The ID of the pie to retrieve.

### Returns

A dictionary representing the pie, including its settings and instrument list.

**Example**

```json
{
  "instruments": [
    {
      "ticker": "RPIl_EQ",
      "result": {
        "priceAvgInvestedValue": 0,
        "priceAvgValue": 0,
        "priceAvgResult": 0,
        "priceAvgResultCoef": 0
      },
      "expectedShare": 1.0,
      "currentShare": 0,
      "ownedQuantity": 0.0,
      "issues": []
    }
  ],
  "settings": {
    "id": 4617385,
    "instrumentShares": null,
    "name": "Test Pie",
    "icon": null,
    "goal": 1000,
    "creationDate": 1749732446.569772,
    "endDate": "2025-07-10T23:59:59.999+03:00",
    "initialInvestment": null,
    "dividendCashAction": "REINVEST",
    "publicUrl": null
  }
}
```

## Update Pie

**Note**: I have found that some fields **must
** be updated, otherwise the API will return an error. For example, I have found issues when I do not update the
`insurmentShares` field, even if I am not changing it. If you encounter issues, try updating all fields with the same values as before.

```python
from trading212 import client

t212 = client.Client("TOKEN")
pie = {
    "name": "Updated Pie",
    "icon": "new_icon_url",
    "instrumentShares": {
        "RPIl_EQ": 0.7,
        "NVDA_US_EQ": 0.3
    },
    "goal": "1500",
    "dividendCashAction": "TO_ACCOUNT_CASH",
}
t212.update_pie(4617385, pie)
```

### Input

The ID of the pie to update and a JSON object representing the changes to make to the pie.

| Field              | Type   | Description                                                            | Example                             |
|--------------------|--------|------------------------------------------------------------------------|-------------------------------------|
| name               | string | Name of the pie.                                                       | Test                                |
| dividendCashAction | string | Action to take with dividends, can be "REINVEST" or "TO_ACCOUNT_CASH". | REINVEST                            |
| endDate            | string | End date for the pie in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).        | 2025-06-19F12:05:08Z                |
| goal               | string | Goal amount in the account currency.                                   | 1000                                |
| icon               | string | URL of the icon for the pie.                                           | Unicorn                             |
| instrumentShares   | object | Dictionary of instrument IDs and their corresponding target weight.    | {"RPIl_EQ": 0.5, "NVDA_US_EQ": 0.5} |

### Returns

A dictionary representing the updated pie, including its settings and instrument list.

```json
{
  "instruments": [
    {
      "ticker": "RPIl_EQ",
      "result": {
        "priceAvgInvestedValue": 0,
        "priceAvgValue": 0,
        "priceAvgResult": 0,
        "priceAvgResultCoef": 0
      },
      "expectedShare": 0.7,
      "currentShare": 0,
      "ownedQuantity": 0.0,
      "issues": []
    },
    {
      "ticker": "AAPL_US_EQ",
      "result": {
        "priceAvgInvestedValue": 0,
        "priceAvgValue": 0,
        "priceAvgResult": 0,
        "priceAvgResultCoef": 0
      },
      "expectedShare": 0.3,
      "currentShare": 0,
      "ownedQuantity": 0.0,
      "issues": []
    }
  ],
  "settings": {
    "id": 715872,
    "instrumentShares": null,
    "name": "Updated Pie",
    "icon": "Unicorn",
    "goal": 2000,
    "creationDate": 1749845179.0,
    "endDate": null,
    "initialInvestment": null,
    "dividendCashAction": "REINVEST",
    "publicUrl": null
  }
}
```

## Duplicate Pie

```python
from trading212 import client

t212 = client.Client("TOKEN")

new_pie = {
    "name": "Duplicated Pie",
    "icon": "Unicorn",
}

pie = t212.duplicate_pie(4617385, new_pie)
```

### Input

The ID of the pie to duplicate and a JSON object representing the new pie's name and optionally, its icon.

| Field | Type   | Description                      | Example        |
|-------|--------|----------------------------------|----------------|
| name  | string | Name of the new pie.             | Duplicated Pie |
| icon  | string | URL of the icon for the new pie. | Unicorn        |

### Returns

A dictionary representing the duplicated pie, including its settings and instrument list.

```json
{
  "instruments": [
    {
      "ticker": "RPIl_EQ",
      "result": {
        "priceAvgInvestedValue": 0,
        "priceAvgValue": 0,
        "priceAvgResult": 0,
        "priceAvgResultCoef": 0
      },
      "expectedShare": 0.7,
      "currentShare": 0,
      "ownedQuantity": 0,
      "issues": []
    },
    {
      "ticker": "AAPL_US_EQ",
      "result": {
        "priceAvgInvestedValue": 0,
        "priceAvgValue": 0,
        "priceAvgResult": 0,
        "priceAvgResultCoef": 0
      },
      "expectedShare": 0.3,
      "currentShare": 0,
      "ownedQuantity": 0,
      "issues": []
    }
  ],
  "settings": {
    "id": 715875,
    "instrumentShares": null,
    "name": "Duplicated Pie",
    "icon": null,
    "goal": 2000.0,
    "creationDate": 1749845599.2010345,
    "endDate": null,
    "initialInvestment": null,
    "dividendCashAction": "REINVEST",
    "publicUrl": null
  }
}
```

## Delete Pie

```python
from trading212 import client

t212 = client.Client("TOKEN")

t212.delete_pie(4617385)
```

### Input

The ID of the pie to delete.

### Returns

`None`. The pie is deleted successfully if no exception is raised.
