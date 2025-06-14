# trading212-api-py

Python client for Trading212 API.

Creating a client:

```python
from trading212 import client

t212 = client.Client("TOKEN", demo=True)
```

Once a client is created, you can use it to interact with the Trading212 API using the methods below. See the tests package for more examples. Omit the
`demo` parameter (or set it to `False`) to use a live account.

See the [documentation](https://github.com/clincha/trading212-api-py/tree/main/documentation) folder for details on the API methods and their parameters. Included in the folder are sample responses for each method, which can be used to understand the expected structure of the data returned by the API.

## Implementation status

| API                  | Status             | Notes            |
|----------------------|--------------------|------------------|
| Instruments Metadata | :white_check_mark: | Completed v0.0.4 |
| Pies                 | :white_check_mark: | Completed v0.0.4 |
| Equity Orders        | :x:                | Estimated v1.0.0 |
| Account Data         | :white_check_mark: | Completed v0.0.4 |
| Personal Portfolio   | :x:                | Estimated v0.1.0 |
| Historical items     | :x:                | Estimated v0.2.0 |
