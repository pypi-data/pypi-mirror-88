# Horkos

A library for validating data at the edges of data systems.

## Install

```
pip install horkos
```

## Documentation

Detailed documentation can be found on [Read the Docs](https://horkos.readthedocs.io/en/latest/).

## Usage

First define the data schema:

```yaml
# http-requests-schema.yaml
name: "http_requests"
description: >-
  This is the http request event data set, it is all about http requests we
  receive. It's important to include as much information about it
  as is reasonable. The hardest thing about data is understanding it after
  the fact.
fields:
  path:
    type: string
    description: >-
      The path of the url that was hit. This will be everything after the
      host portion of the url.
  params:
    type: string
    nullable: true
    checks:
      - json
    description: >-
      The parameters of the http request. If the method is a `GET` these come
      from the url otherwise they are the JSON from the request body.
  method:
    type: string
    checks:
      - name: choice
        args:
          options:
            - DELETE
            - GET
            - HEAD
            - OPTIONS
            - PATCH
            - POST
            - PUT
    description: >-
      The http method of the request. Must be one of:
      `DELETE`, `GET`, `HEAD`, `OPTIONS`, `PATCH`, `POST`, or `PUT`.
  response_code:
    type: integer
    description: The http response code of the request
  timestamp:
    type: string
    checks:
      - iso_timestamp
    description: The time at which the http request was received.
```

To use this schema to validate records:

```python
import horkos

schema = horkos.load_schema('http-requests-schema.yaml')
schema.process({'path': '/foo/bar'})
# RecordValidationError: Casting errors - params is required, method is required, ...
schema.process({
    'path': '/foo/bar',
    'params': '{"foo": "bar"}',
    'method': 'BAD',
    'response_code': '200',
    'timestamp': '2020-06-15T12:34:56',
})
# RecordValidationError: Check errors - "BAD" in method did not pass choice check, ...
schema.process({
    'path': '/foo/bar',
    'params': '{"foo": "bar"}',
    'method': 'GET',
    'response_code': '200',
    'timestamp': '2020-06-15T12:34:56',
})
# {..., 'response_code': 200, ...}
```

## CLI

It's also possible to use `horkos` via cli to validate `csv` and `json` files.

```csv
path,params,method,response_code,timestamp
/foo/bar,,GET,200,2020-06-15T12:34:56
/fizbuz,{"param":"value"},POST,200,2020-12-15T12:34:56
/fizbuz,,ERROR,500,2020-12-15T12:34:56
/fizbuz,,GET,BAD,2020-12-15T12:34:56
```

To validate the csv run:

```
$ horkos check -s http-requests-schema.yaml data.csv
[Row 2]: Check errors - value of "ERROR" for method did not pass choice check
[Row 3]: Casting errors - value of "BAD" for response_code could not be cast to integer
2 errors found
```
