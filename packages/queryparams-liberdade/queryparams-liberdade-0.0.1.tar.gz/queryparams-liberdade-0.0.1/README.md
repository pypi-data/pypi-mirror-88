# Query Params

This package provides a couple of functions to turn a dictionary like
this:

``` python
d = {
    'filters[1][field]': ['year'],
    'filters[1][operator]': ['btw'],
    'filters[1][value][0]': ['2020'],
    'filters[1][value][1]': ['2021'],
    'filters[0][field]': ['month'],
    'filters[0][operator]': ['btw'],
    'filters[0][value][0]': ['8'],
    'filters[0][value][1]': ['9'],
    'orders[date]': ['asc'],
}
```

into an object like this:

``` python
d = {
    "filters": [
        {
            "field": "year"
            "operator": "btw",
            "value"; [
                "2020",
                "2021",
            ]
        }, {
            "field": "month"
            "operator": "btw",
            "value"; [
                "8",
                "9",
            ]
        }
    ],
    "orders": {
        "date": "asc",
    }
}
```

That's great to send objects as query parameters in URLs (hence the project
name).
