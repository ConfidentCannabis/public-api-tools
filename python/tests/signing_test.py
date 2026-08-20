# -*- coding: utf-8 -*-
import unittest
from signing import generate_signature, unicode_safe_urlencode


method = 'GET'
route = '/api/v0/signingtest/'
headers = {'X-ConfidentCannabis-Timestamp': '1474507118.77095'}
data = {'foo': 1, 'bar': 2}
api_key = '88b750a8-d414-4aee-b26c-2cc7e85434dd'
api_secret = '043bca27-c4d1-4d39-86d6-e5f0c3b4bb4f'
expected_signature = 'CC0-HMAC-SHA256:x-confidentcannabis-timestamp:1fdc8a407c5d1c31df2334fbc49984062a4071077a9dc7cfff4de934902c01b8'  # NOQA

escape_data = {'escapeme': "!'()*+~ "}
escaped_encoded = '%21%27%28%29%2A%2B%7E+'
expected_escaped_signature = 'CC0-HMAC-SHA256:x-confidentcannabis-timestamp:7983502f22d3b7a378f5f706184854b0aa554988419672bfea1cfd28bb3f9ffa'  # NOQA

unicode_data = {'foo': 1, '☃': '☃'}
expected_unicode_signature = 'CC0-HMAC-SHA256:x-confidentcannabis-timestamp:e289a22b9315d8652f6b92f26057f2f018f76414348844a41043d1dbd64def47'  # NOQA


class SigningTest(unittest.TestCase):
    def generate_signature_test(self):
        signature = generate_signature(
            method, route, headers, data, api_key, api_secret)
        self.assertEqual(signature, expected_signature)

    def escape_test(self):
        escaped = unicode_safe_urlencode([
            ('escapeme', escape_data['escapeme'])
        ])
        self.assertEqual(
            escaped,
            'escapeme={}'.format(
                escaped_encoded
            )
        )

    def escape_signature_test(self):
        signature = generate_signature(
            method, route, headers, escape_data, api_key, api_secret)
        self.assertEqual(signature, expected_escaped_signature)

    def support_unicode_test(self):
        signature = generate_signature(
            method, route, headers, unicode_data, api_key, api_secret)
        self.assertEqual(signature, expected_unicode_signature)


if __name__ == '__main__':
    unittest.main()
