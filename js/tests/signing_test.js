var assert = require('assert');
var generateSignature = require('../signing').generateSignature;
var specialEncodeComponent = require('../signing').specialEncodeComponent;

var method = 'GET';
var route = '/api/v0/signingtest/';
var headers = {'X-ConfidentCannabis-Timestamp': '1474507118.77095'}
var data = {foo: 1, bar: 2};
var apiKey = '88b750a8-d414-4aee-b26c-2cc7e85434dd';
var apiSecret = '043bca27-c4d1-4d39-86d6-e5f0c3b4bb4f';
var expectedSignature = 'CC0-HMAC-SHA256:x-confidentcannabis-timestamp:1fdc8a407c5d1c31df2334fbc49984062a4071077a9dc7cfff4de934902c01b8';

var escapeData = {'escapeme': "!'()*+~ "};
var escapedEncoded = '%21%27%28%29%2A%2B%7E+';
var expectedEscapeSignature = 'CC0-HMAC-SHA256:x-confidentcannabis-timestamp:7983502f22d3b7a378f5f706184854b0aa554988419672bfea1cfd28bb3f9ffa';

var unicodeData = {'foo': 1, '☃': '☃'};
var expectedUnicodeSignature = 'CC0-HMAC-SHA256:x-confidentcannabis-timestamp:e289a22b9315d8652f6b92f26057f2f018f76414348844a41043d1dbd64def47';


describe('signing', function() {
  describe('generateSignature', function() {
    it('should generate a signature', function() {
      var signature = generateSignature(method, route, headers, data, apiKey, apiSecret);
      assert.equal(signature, expectedSignature);
    });

    it('should escape things to match the requirements', function() {
      var signature = generateSignature(method, route, headers, escapeData, apiKey, apiSecret);
      assert.equal(signature, expectedEscapeSignature);
    });

    it('should consider the request method', function() {
      var signature = generateSignature('POST', route, headers, data, apiKey, apiSecret);
      assert.notEqual(signature, expectedSignature);
    });

    it('should consider the request route', function() {
      var signature = generateSignature(method, route + '/other', headers, data, apiKey, apiSecret);
      assert.notEqual(signature, expectedSignature);
    });

    it('should consider the request headers', function() {
      var newHeaders = Object.assign({}, {'X-Other-Header': 'stuff'}, headers);
      var signature = generateSignature(method, route, newHeaders, data, apiKey, apiSecret);
      assert.notEqual(signature, expectedSignature);
    });

    it('should consider the request data', function() {
      var newData = Object.assign({}, {other: 'data'}, data);
      var signature = generateSignature(method, route, headers, newData, apiKey, apiSecret);
      assert.notEqual(signature, expectedSignature);
    });

    it('should consider the api credentials', function() {
      var badSignature = generateSignature(method, route, headers, data, apiKey, 'foo');
      assert.notEqual(badSignature, expectedSignature);

      var badSignature2 = generateSignature(method, route, headers, data, 'foo', apiSecret);
      assert.notEqual(badSignature2, expectedSignature);

      assert.notEqual(badSignature, badSignature2);
    });

    it('should handle unicode data', function() {
      var signature = generateSignature(method, route, headers, unicodeData, apiKey, apiSecret);
      assert.equal(signature, expectedUnicodeSignature);
    });
  });

  describe('specialEncodeComponent', function() {
    it('should handle special cases to match requirements', function() {
      assert.equal(
        specialEncodeComponent(escapeData.escapeme),
        escapedEncoded
      );
    });
  });

});
