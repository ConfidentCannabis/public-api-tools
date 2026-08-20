# Confident Cannabis API Tools - Python

Python tools for working with the Confident Cannabis API

## Getting Started
```
virtualenv env
. env/bin/activate
pip install -r requirements.txt

nosetest
```

## Running the Tests

Once you have a local environment set up and have installed the requirements
using pip you can run all the tests from the root of the python directory by
calling:

`nosetests`


## Request Signing

```python
from .signing import generate_signature

method = 'GET'
route = '/api/v0/signingtest/'
headers = {'X-CC-Timestamp': '1474507118.77095'}
data = {'foo': 1, 'bar': 2}
api_key = '88b750a8-d414-4aee-b26c-2cc7e85434dd'
api_secret = '043bca27-c4d1-4d39-86d6-e5f0c3b4bb4f'

signature = generate_signature(method, route, headers, data, api_key, api_secret)
print(signature)

>>> 'CC0-HMAC-SHA256:x-cc-timestamp:f4f830ac634dee9a9c98bfe71427d4b7e78ffd0356ee305958bc3687d40ffa43'  # NOQA
```
