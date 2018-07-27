import json

import attr

from cc_utils import cc_request
from cc_config import cc_urls


@attr.s
class ConfidentCannabis(object):
    """
    Simple interface to the Confident Cannabis Lab API. Please see
    the full API documentation for details.

    Quick Summary:
    - everything is signed using an api_key and api_secret
    - endpoints that return lists are paged, generally are ordered with the
    most recent items first, and accept start and limit fields
    - all requests can raise InvalidAuthError or InvalidRequestError
    - InvalidRequestError generally has `error_code` and `error_message`
    - basic examples are at the bottom of this file

    Example:
        cc = ConfidentCannabis(
            api_key='FILLTHISOUT',
            api_secret='FILLTHISOUT',
            api_stage='production'
        )
        print cc.get_clients()
    """

    api_key = attr.ib()
    api_secret = attr.ib()
    api_version = attr.ib(default=0)
    api_stage = attr.ib(default='sandbox')

    def request(self, method, *args, **kwargs):
        kwargs['api_key'] = self.api_key
        kwargs['api_secret'] = self.api_secret
        return cc_request(self.api_stage, method, *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.request('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request('POST', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.request('PUT', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request('DELETE', *args, **kwargs)

    def get_compounds(self):
        """Return the list of possible test compounds."""
        # TODO: cache these results since they change very rarely
        result = self.get(cc_urls['compounds'])
        return result['compounds']

    def get_order_statuses(self):
        """Return the list of possible order statuses."""
        # TODO: cache these results since they change very rarely
        result = self.get(cc_urls['order_statuses'])
        return result['order_statuses']

    def get_sample_categories(self):
        """Return the list of possible sample categories."""
        # TODO: cache these results since they change very rarely
        result = self.get(cc_urls['sample_categories'])
        return result['sample_categories']

    def get_sample_types(self):
        """Return the list of possible sample types."""
        # TODO: cache these results since they change very rarely
        result = self.get(cc_urls['sample_types'])
        return result['sample_types']

    def get_test_types(self):
        """Return the list of possible test types."""
        # TODO: cache these results since they change very rarely
        result = self.get(cc_urls['test_types'])
        return result['test_types']

    def get_clients(self):
        result = self.get(cc_urls['clients'])
        return result['clients']

    def get_client(self, client_id):
        result = self.get(
            cc_urls['client_details'].format(client_id=client_id)
        )
        return result['client']

    def get_orders(self, status_id=None, start=None, limit=None):
        """
        Return a paged list of orders, sorted by most recent first.
        Can be limited to a particular order status using the status_id param
        """
        payload = {}
        if status_id is not None:
            payload['status_id'] = status_id
        if start is not None:
            payload['start'] = start
        if limit is not None:
            payload['limit'] = limit
        result = self.get(cc_urls['orders'], payload)
        return result['orders']

    def get_order(self, order_id):
        """Return details about the given order."""
        result = self.get(
            cc_urls['order_details'].format(order_id=order_id)
        )
        return result['order']

    def upload_order_document(self, order_id, filepath):
        """Upload a document and attach it to the given order.
        Returns True if successful, False otherwise.
        """
        with open(filepath, 'rb') as f:
            result = self.post(
                cc_urls['order_document'].format(order_id=order_id),
                files={'document': f}
            )
            return result.get('success', False)

    def get_samples(self, order_status_id=None, start=None, limit=None):
        """
        Return a paged list of samples, sorted by most recent first.
        Results can be limited to a particular order status using the
        order_status_id param.
        """
        payload = {}
        if order_status_id is not None:
            payload['order_status_id'] = order_status_id
        if start is not None:
            payload['start'] = start
        if limit is not None:
            payload['limit'] = limit

        result = self.get(cc_urls['samples'], payload)
        return result['samples']

    def get_sample(self, sample_id):
        """Return details about the given sample."""
        result = self.get(
            cc_urls['sample_details'].format(
                sample_id=sample_id
            )
        )
        return result['sample']

    def submit_test_results(self, sample_id, results_dict):
        """
        Submit test results for the given sample.
        Requires a results_dict in the format matching the api - please
        check the documentation to ensure this is up to date.
        """
        return self.post(
            cc_urls['sample_test_results'].format(sample_id=sample_id),
            {'test_results': json.dumps(results_dict)}
        )

    def create_order(self, order):
        """
        Create a new order.
        Requires an 'order' in the format matching the api. This payload can be
        large and has many fields -- please check the documentation to
        ensure this is up to date.

        # TODO: validate fields in a helpful way - either optionally here or
        # as a helper
        """
        return self.post(cc_urls['order'], {'order': json.dumps(order)})

    def upload_sample_coa(self, sample_id, filepath):
        """
        Upload a pdf and attach it to the given sample as the
        Certificate of Analysis.
        Returns True if successful, False otherwise.
        """
        with open(filepath, 'rb') as f:
            result = self.post(
                cc_urls['sample_coa'].format(sample_id=sample_id),
                files={'coa': f}
            )
            return result.get('success', False)

    def upload_sample_image(self, sample_id, filepath, set_as_cover=True):
        """
        Upload an image and attach it to the given sample. Sets the
        image as the sample's cover unless set_as_cover is False.
        Returns True if successful, False otherwise.
        """
        with open(filepath, 'rb') as f:
            data = {}
            if set_as_cover:
                data['set_cover_image'] = bool(set_as_cover)

            result = self.post(
                cc_urls['sample_image'].format(sample_id=sample_id),
                files={'image': f},
                data=data
            )
            return result.get('success', False)
