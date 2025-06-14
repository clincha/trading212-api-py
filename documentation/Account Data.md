# Account Data

## Get Account Cash

```python
from trading212 import client

t212 = client.Client("TOKEN")

cash = t212.get_account_cash()
```

### Returns

An object containing the cash balances of the account.

**Example:**

```json
{
  "free": 2567.57,
  "total": 223998.31,
  "ppl": 173484.92,
  "result": 524.35,
  "invested": 47945.82,
  "pieCash": 0.0,
  "blocked": null
}
```

## Get Account Metadata

```python
from trading212 import client

t212 = client.Client("TOKEN")

metadata = t212.get_account_metadata()
```

### Returns

An object containing the id and currency of the account.

**Example:**

```json
{
  "id": 1234567,
  "currencyCode": "EUR"
}
```