import json
import logging
import time

import requests

from signing import generate_signature
from cc_config import get_cc_backend_url
from cc_exceptions import InvalidAuthError
from cc_exceptions import InvalidRequestError


def get_version_route(route, version=0):
    return '/v{}/{}'.format(
        str(version),
        route.lstrip('/')
    )


def get_url(api_stage, route, version=0):
    return get_cc_backend_url(
        api_stage,
        get_version_route(route, version)
    )


def submit_test_data():
    pass


def cc_request(
        stage, method, route, data=None, files=None,
        headers=None, api_key=None, api_secret=None):
    data = data or {}
    headers = headers or {}
    headers['X-ConfidentCannabis-Timestamp'] = '{}'.format(time.time())

    signature = generate_signature(
        method,
        get_version_route(route),
        headers,
        data,
        api_key,
        api_secret
    )

    headers['X-ConfidentCannabis-APIKey'] = api_key
    headers['X-ConfidentCannabis-Signature'] = signature

    if method == 'POST':
        request_method = requests.post
    elif method == 'GET':
        request_method = requests.get
    elif method == 'PUT':
        request_method = requests.put
    elif method == 'DELETE':
        request_method = requests.delete

    url = get_url(stage, route)
    logging.info('Sending {} Request to {}'.format(method, url))
    response = request_method(
        url,
        data,
        files=files,
        headers=headers
    )

    if response.status_code == 401:
        raise InvalidAuthError(response.content)

    elif response.status_code == 400:
        # try to parse content out
        try:
            parsed = json.loads(response.content)
        except (ValueError, TypeError):
            raise InvalidRequestError(response.content)

        logging.error('Request failed: {}'.format(response.content))
        raise InvalidRequestError(
            parsed.get('error_message', 'unknown error'),
            error_code=parsed.get('error_code', None),
            error_field=parsed.get('error_field', None),
            error_category=parsed.get('error_category', None)
        )

    elif response.status_code != 200:
        raise Exception(response.content)

    return json.loads(response.content)
