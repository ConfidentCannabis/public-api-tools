cc_urls = {
    'compounds': 'compounds',
    'order_statuses': 'orderstatuses',
    'sample_categories': 'samplecategories',
    'sample_types': 'sampletypes',
    'test_types': 'testtypes',

    'clients': 'clients',
    'client_details': 'client/{client_id}',

    'orders': 'orders',
    'order_details': 'order/{order_id}',
    'order_document': 'order/{order_id}/document',

    'samples': 'samples',
    'sample_details': 'sample/{sample_id}',
    'sample_test_results': 'sample/{sample_id}/test_results',
    'sample_coa': 'sample/{sample_id}/coa',
    'sample_image': 'sample/{sample_id}/image',
}

cc_stages = {
    'sandbox': 'https://sandbox-api.confidentcannabis.com/',
    'production': 'https://api.confidentcannabis.com/'
}


def get_cc_backend_url(stage, route):
    assert stage in cc_stages.keys()
    return cc_stages[stage] + route
