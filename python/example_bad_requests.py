"""
example_bad_requests.py

Test script that makes it easy to submit test results
that are invalid in various ways as an easy way to
generate the various different error code responses.

Fill out the configuration info in examples_config, then
use keys listed in the bad_test_results dict to

Use keys listed in example_config.bad_test_results to
send the matching block of data as test results.

For Example:

`python example_bad_requests.py missing_required_field` will
trigger an error with the `missing_required_field` error code.

"""

import sys

from examples_config import (
    api_key, api_secret,
    sample_id,
    bad_test_results
)

from confidentcannabis import ConfidentCannabis

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print 'Usage: {} error_code_to_trigger'.format(
            sys.argv[0]
        )
        sys.exit(1)

    error_code = sys.argv[1]
    if error_code not in bad_test_results:
        print 'Error code "{}" not found in config'.format(
            error_code
        )
        sys.exit(1)

    cc = ConfidentCannabis(api_key, api_secret)
    cc.submit_test_results(
        sample_id,
        bad_test_results[error_code]
    )
