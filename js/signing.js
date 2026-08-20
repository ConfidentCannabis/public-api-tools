// hmac sha256 from https://github.com/brix/crypto-js
var CryptoJS = require('crypto-js');

module.exports = {
  generateSignature: generateSignature,
  specialEncodeComponent: specialEncodeComponent,
  exportSigningForDebug: exportSigningForDebug
};

// hmac sha256 from https://github.com/brix/crypto-js
function generateSignature(method, route, headers, data, apiKey, apiSecret) {
    // 1. create base string by combining method and route - eg: GET/api/v0/test
    var baseString = method.toUpperCase() + route
    // console.log('baseString:', baseString);
    // > baseString: GET/api/v0/signingtest/

    // 2. create sorted, lowercased list of (key, value) pairs from headers
    //     dictionary (must include X-CC-Timestamp but not X-CC-APIKey or
    //     X-CC-Signature)
    var sortedHeaderKeys = Object.keys(headers).sort();
    var sortedHeaders = sortedHeaderKeys.map(function(headerKey) {
      return [headerKey.toLowerCase(), ('' + headers[headerKey]).toLowerCase()];
    }).sort();
    // console.log('sortedHeaders:', sortedHeaders);
    // > sortedHeaders: [ [ 'x-confidentcannabis-timestamp', '1474507118.77095' ] ]

    // 3. create url encoded param string '{{key}}={{value}}&...'
    //     for ordered header fields, lowercased
    var headerString = sortedHeaders.reduce(function(prev, curr) {
      var component = encodeURIComponent(curr[0]) + '=' + encodeURIComponent(curr[1]);
      prev.push(component);
      return prev;
    }, []).join('&');
    // console.log('headerString:', headerString);
    // > headerString: x-confidentcannabis-timestamp=1474507118.77095

    // 4. create semi-colon separated list of lowercase
    //     header keys that have been signed eg: x-cc-timestamp;host
    var headerList = sortedHeaderKeys.map(function(headerKey) {
      return headerKey.toLowerCase();
    }).join(';');
    // console.log('headerListString:', headerListString);
    // > headerListString: x-confidentcannabis-timestamp

    // 5. create sorted list of (key, value) pairs from data
    var sortedKeys = Object.keys(data).sort();
    var sortedParamsList = sortedKeys.map(function(key) {
      return [key, data[key]];
    });
    // console.log('sortedParamsList:', sortedParamsList);
    // > sortedParamsList: [ [ 'bar', 2 ], [ 'foo', 1 ] ]

    // 6. add (api_key, {{api_key}}) to the END of the list
    sortedParamsList.push(['api_key', apiKey]);
    // console.log('sortedParamsList:', sortedParamsList);
    // > sortedParamsList: [ [ 'bar', 2 ],
    // > [ 'foo', 1 ],
    // > [ 'api_key', '88b750a8-d414-4aee-b26c-2cc7e85434dd' ] ]

    // 7. create url encoded param string '{{key}}={{value}}&...'
    //     for ordered data fields
    var paramString = sortedParamsList.reduce(function(prev, curr) {
      var component = specialEncodeComponent(curr[0]) + '=' + specialEncodeComponent(curr[1]);
      prev.push(component);
      return prev;
    }, []).join('&');
    // console.log('paramString:', paramString);
    // > paramString: bar=2&foo=1&api_key=88b750a8-d414-4aee-b26c-2cc7e85434dd

    // 8. percent-encode (see notes below about URI Encoding) the base string
    //     from step 1
    var encodedBaseString = encodeURIComponent(baseString);
    // console.log('encodedBaseString:', encodedBaseString);
    // > encodedBaseString: GET%2Fapi%2Fv0%2Fsigningtest%2F

    // 9. combine percent encoded base string, url encoded header string, and
    //     url encoded parameter string with & between them
    // console.log('Base String: ' + encodedBaseString);
    // console.log('Header String: ' + headerString);
    // console.log('Params String: ' + paramString);
    var signingString = [
      encodedBaseString,
      headerString,
      paramString
    ].join('&');
    // console.log('signingString: ' + signingString);
    // > signingString: GET%2Fapi%2Fv0%2Fsigningtest%2F&x-confidentcannabis-timestamp=1474507118.77095&bar=2&foo=1&api_key=88b750a8-d414-4aee-b26c-2cc7e85434dd

    // 10. create sha256 hmac signature from string using apiSecret
    var rawSignature = '' + CryptoJS.HmacSHA256(signingString, apiSecret).valueOf();
    // console.log('raw signature: ', rawSignature);
    // > raw signature: 1fdc8a407c5d1c31df2334fbc49984062a4071077a9dc7cfff4de934902c01b8

    // 11. prefix with signing algorithm ('CC0-HMAC-SHA256:') and header list
    // with colons in between
    var signature = 'CC0-HMAC-SHA256:' + headerList + ':' + rawSignature;
    // console.log('final signature:', signature);
    // final signature: CC0-HMAC-SHA256:x-confidentcannabis-timestamp:1fdc8a407c5d1c31df2334fbc49984062a4071077a9dc7cfff4de934902c01b8

    return signature;
}

function specialEncodeComponent(component) {
  // special cases! encodeURIComponent does NOT escape everything
  // required to match how the expected encoding works
  var specialCases = [
    [/!/g, '%21'],
    [/'/g, '%27'],
    [/\(/g, '%28'],
    [/\)/g, '%29'],
    [/\*/g, '%2A'],
    [/~/g, '%7E'],
    [/%20/g, '+'] // turn spaces back from %20 into +
  ];

  var component = encodeURIComponent(component);
  for (var i = 0, n = specialCases.length; i < n; i++) {
    component = component.replace(
      specialCases[i][0], specialCases[i][1]);
  }
  return component;
}

function exportSigningForDebug() {
  var source = (
    '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' +
    '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
  ).split('');

  console.log(source.map(function (character) {
    return specialEncodeComponent(character);
  }));
}
