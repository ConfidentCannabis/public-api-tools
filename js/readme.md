# Confident Cannabis API Tools - Javascript

Javascript tools for working with the Confident Cannabis API

## Getting Started
```
npm install
npm test
```

## Running the Tests

Once you have installed the dev dependencies using npm you can run the tests
from the root of the JS directory by calling:

`npm test`


## Request Signing

Javascript:
```js
var generateSignature = require('.signing').generateSignature;

method = 'GET'
route = '/api/v0/signingtest/'
headers = {'X-CC-Timestamp': '1474507118.77095'}
data = {'foo': 1, 'bar': 2}
api_key = '88b750a8-d414-4aee-b26c-2cc7e85434dd'
api_secret = '043bca27-c4d1-4d39-86d6-e5f0c3b4bb4f'

var signature = generateSignature(method, route, headers, data, apiKey, apiSecret);
console.log(signature);

> 'CC0-HMAC-SHA256:x-cc-timestamp:f4f830ac634dee9a9c98bfe71427d4b7e78ffd0356ee305958bc3687d40ffa43'
```
