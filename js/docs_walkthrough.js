/**
 * This file is the result of combining all the steps from the
 * signing documentation (with CryptoJS imported).
*/

var CryptoJS = require('crypto-js');

var method = 'GET';
var route = '/api/v0/signingtest/';
var headers = {'X-ConfidentCannabis-Timestamp': '1474507118.77095'};
var data = {'foo': 1, 'bar': 2};
var apiKey = '88b750a8-d414-4aee-b26c-2cc7e85434dd';
var apiSecret = '043bca27-c4d1-4d39-86d6-e5f0c3b4bb4f';

// 1
var baseString = method.toUpperCase() + route;
console.log('baseString:', baseString);

// 2
var headers = {'X-ConfidentCannabis-Timestamp': '1474507118.77095'};
var sortedHeaderKeys = Object.keys(headers).sort();
var sortedHeaders = sortedHeaderKeys.map(function(headerKey) {
  return [headerKey.toLowerCase(), ('' + headers[headerKey]).toLowerCase()];
}).sort();
console.log('sortedHeaders:', sortedHeaders);

// 3
var headerString = sortedHeaders.reduce(function(prev, curr) {
  var component = encodeURIComponent(curr[0]) + '=' + encodeURIComponent(curr[1]);
  prev.push(component);
  return prev;
}, []).join('&');
console.log('headerString:', headerString);

// 4
var headerListString = sortedHeaderKeys.map(function(headerKey) {
  return headerKey.toLowerCase();
}).join(';');
console.log('headerListString:', headerListString);

// 5
var sortedKeys = Object.keys(data).sort();
var sortedParamsList = sortedKeys.map(function(key) {
  return [key, data[key]];
});
console.log('sortedParamsList:', sortedParamsList);

// 6
sortedParamsList.push(['api_key', apiKey]);
console.log('sortedParamsList:', sortedParamsList);

// 7
// handle special cases not done by encodeURIComponent
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

var paramString = sortedParamsList.reduce(function(prev, curr) {
  var component = specialEncodeComponent(curr[0]) + '=' + specialEncodeComponent(curr[1]);
  prev.push(component);
  return prev;
}, []).join('&');
console.log('paramString:', paramString);

// 8
var encodedBaseString = encodeURIComponent(baseString);
console.log('encodedBaseString:', encodedBaseString);

// 9
var signingString = [
  encodedBaseString,
  headerString,
  paramString
].join('&');
console.log('signingString: ' + signingString);

// 10
var rawSignature = '' + CryptoJS.HmacSHA256(signingString, apiSecret).valueOf();
console.log('raw signature: ', rawSignature);

// 11
var signature = 'CC0-HMAC-SHA256:' + headerListString + ':' + rawSignature;
console.log('final signature:', signature);



// confirm it matches the expected signature from the docs
var expected = 'CC0-HMAC-SHA256:x-confidentcannabis-timestamp:1fdc8a407c5d1c31df2334fbc49984062a4071077a9dc7cfff4de934902c01b8';
if (expected === signature) {
  console.log('Yay! Signatures Match!');
} else {
  console.log("Oh no! Something didn't work!");
}
