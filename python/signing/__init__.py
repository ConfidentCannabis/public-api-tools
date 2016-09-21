"""
Generate signatures for the CC external api endpoints.
"""
import hashlib
import hmac
import logging
import urllib

logging.basicConfig(level=logging.DEBUG)


def generate_signature(
        method, route, headers, data, api_key, api_secret, version=0):
    """
    Generate an api request signature for the given method, endpoint,
    headers, data dict, api_key, and api_secret.

    Parameters:

    - method (string): uppercase http method for endpoint - GET/POST/PUT/DELETE
    - route (string): url after the hostname (without any querystring)
        eg: /api/v0/signingtest
    - headers (dict): dictionary of headers being sent in the
        request must include X-ConfidentCannabis-Timestamp and
        anything else you wish to sign
        X-ConfidentCannabis-Timestamp should be a unix timestamp
        (seconds since epoch)
    - data (dict): dictionary of data fields being sent in the request
    - api_key (string): api key used for signing
    - api_secret (string): api secret used for signing

    Steps to generate a signature:

    1. create base string by combining method and route - eg: GET/api/v0/test
    2. create ascii-sorted (ascending), lowercased list of (key,
        value) pairs from headers dictionary (must include
        X-ConfidentCannabis-Timestamp but not
        X-ConfidentCannabis-APIKey or
        X-ConfidentCannabis-Signature)
    3. create url encoded string '{{key}}={{value}}&...'
        for ascii-ordered header fields, lowercased
    4. create semi-colon separated list of lowercase
        header keys eg: x-confidentcannabis-timestamp;host
    5. create ascii-sorted list of (key, value) pairs from data
    6. add ('api_key', {{api_key}}) to the END of the list
    7. create url encoded param string '{{key}}={{value}}&...'
        for ordered data fields
    8. percent-encode (see notes below about URI Encoding) the base string
        from step 1
    9. combine percent encoded base string, url encoded header string, and url
        encoded parameter string with & between them
    10. create sha256 hmac signature from string using api_secret
    11. prefix with signing algorithm and header list string:
        'CC0-HMAC-SHA256:host;x-confidentcannabis-timestamp:'

    URI Encoding:
    - rfc: http://tools.ietf.org/html/rfc3986#section-2.1
    - python: https://docs.python.org/2/library/urllib.html#urllib.urlencode

    NOTE! The encoding used by each language (and often from library to
    library and even function to function) always ends up having
    different quirks. The Confident Cannabis API uses url escaping
    for every printable ascii character except -, _, and . are left
    alone and spaces are encoded as + signs (NOT %20).

    There is a full list of encoded characters in the readme to help
    debug signing issues related to encoding.

    Example:
    ```
    method = 'GET'
    route = '/api/v0/signingtest/'
    headers = {'X-ConfidentCannabis-Timestamp': '1474507118.77095'}
    data = {'foo': 1, 'bar': 2}
    api_key = '88b750a8-d414-4aee-b26c-2cc7e85434dd'
    api_secret = '043bca27-c4d1-4d39-86d6-e5f0c3b4bb4f'

    signature = generate_signature(
        method, route, headers, data, api_key, api_secret)
    print(signature)

    >>> CC0-HMAC-SHA256:x-confidentcannabis-timestamp:1fdc8a407c5d1c31df2334fbc49984062a4071077a9dc7cfff4de934902c01b8  # NOQA
    ```
    """

    logging.debug(
        'Creating Confident Cannabis V0 HMAC-SHA256 request signature')
    # 1. create base string by combining method and route
    base_string = '{}{}'.format(method.upper(), route)

    # 2. create sorted, lowercased list of (key, value) pairs from headers
    # dictionary (must include X-ConfidentCannabis-Timestamp but not
    # X-ConfidentCannabis-APIKey or X-ConfidentCannabis-Signature)
    sorted_headers = sorted([
        (key.lower(), value)
        for key, value in headers.items()
    ])

    # 3. create url encoded param string '{{key}}={{value]}}&...'
    #     for ordered header fields, lowercased
    header_string = unicode_safe_urlencode(sorted_headers)

    # 4. create semi-colon separated list of lowercase
    #     header keys that will be signed eg: host;x-cc-timestamp
    header_list = ';'.join(k for k, v in sorted_headers)

    # 5. create sorted list of (key, value) pairs from data
    params = sorted((key, value) for key, value in data.items())

    # 6. add api_key={{api_key}} to the END of the list
    params.append(('api_key', api_key))

    # 7. create url encoded param string '{{key}}={{value}}&...'
    #     for ordered data fields
    param_string = unicode_safe_urlencode(params)
    print param_string

    # 8. percent-encode (see notes below about URI Encoding) the base string
    #     from step 1
    encoded_base_string = urllib.quote_plus(base_string)

    # 9. combine percent encoded base string, url
    #     encoded header string, header list, and url
    #     encoded parameter string with & between them
    logging.debug('Base String: {}'.format(encoded_base_string))
    logging.debug('Header String: {}'.format(header_string))
    logging.debug('Params String: {}'.format(param_string))
    signing_string = '&'.join([
        encoded_base_string,
        header_string,
        param_string
    ])
    logging.debug('String: {}'.format(signing_string))
    logging.debug('length: {}'.format(len(signing_string)))

    # 10. create sha256 hmac signature from string using api_secret
    raw_signature = hmac.new(
        api_secret,
        msg=signing_string,
        digestmod=hashlib.sha256
    ).hexdigest()

    # 11. prefix with signing algorithm and header list string:
    #     'CC0-HMAC-SHA256:host;x-confidentcannabis-timestamp:'
    signature = 'CC0-HMAC-SHA256:{}:{}'.format(header_list, raw_signature)
    logging.debug('Final Signature: {}'.format(signature))

    return signature


def unicode_safe_urlencode(sequence):
    return urllib.urlencode(encoded_sequence(sequence))


def encoded_sequence(sequence):
    return [
        (value_to_bytes(key), value_to_bytes(value))
        for key, value in sequence
    ]


def value_to_bytes(value):
    if isinstance(value, unicode):
        safe_value = value.encode('utf8')
    else:
        safe_value = str(value)
    return safe_value


def export_signing_for_debug():
    import string  # NOQA
    sequence = [('1', char) for char in string.printable]
    encoded = unicode_safe_urlencode(sequence)

    stripped = [
        encoded_pair[len('1='):]
        for encoded_pair in encoded.split('&')
    ]

    print stripped
