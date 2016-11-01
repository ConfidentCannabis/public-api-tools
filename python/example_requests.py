from confidentcannabis import ConfidentCannabis

if __name__ == '__main__':
    api_key = 'PUT-YOUR-API-KEY-HERE'
    api_secret = 'PUT-YOUR-API-SECRET-HERE'

    cc = ConfidentCannabis(api_key, api_secret, api_stage='sandbox')

    client_id = 1
    order_id = '1610LAB0001'
    sample_id = '1610LAB0001.0001'
    upload_file_path = 'path/to/a/file'
    sample_coa_path = 'path/to/a/pdf'
    sample_image_path = 'path/to/an/image'
    set_sample_cover = True

    test_results = {
        'categories': {
            'cannabinoids': {
                'info_fields': {
                    'input_units': '%',
                    'report_units': '%',
                    'footnote': 'Only the highest quality methods',
                    'signatory_name': 'John Hancock',
                    'signatory_title': 'Lab Director',
                    'unit_description': 'Flower'
                },
                'compounds': [
                    {
                        'name': 'd9_thc',
                        'value': '0.19',
                        'loq': '0.01'
                    },
                    {
                        'name': 'thca',
                        'value': '0.03',
                        'loq': '0.01'
                    },
                    {
                        'name': 'cbd',
                        'value': '0.02',
                        'loq': '0.01'
                    }
                ]
            },
            'pesticides': {
                'info_fields': {
                    'input_units': 'ppm',
                    'report_units': 'ppb',
                    'footnote': 'Checked for pesticides',
                    'signatory_name': 'John Hancock',
                    'signatory_title': 'Lab Director'
                },
                'compounds': [
                    {
                        'name': 'avermectin',
                        'value': '20',
                        'loq': '10',
                        'limit': '50'
                    },
                    {
                        'name': 'ddvp',
                        'value': '20',
                        'loq': '10',
                        'limit': '50'
                    },
                    {
                        'name': 'gamma_bhc',
                        'value': '20',
                        'loq': '10',
                        'limit': '50'
                    }
                ]
            }
        }
    }

    # ------
    # CLIENTS
    # ------

    # print "List Clients"
    # print cc.get_clients()

    # print "Client Details"
    # print cc.get_client(client_id)

    # ------
    # ORDERS
    # ------

    # print "List Orders"
    # orders = cc.get_orders()
    # print orders

    # print "Paged Orders"
    # paged_orders = cc.get_orders(start=len(orders)-2, limit=1)
    # print paged_orders
    # assert(len(paged_orders), 1)

    # print "Only In Progress Orders"
    # in_progress_orders = cc.get_orders(status_id=2)
    # print in_progress_orders

    # print "Order Details"
    # print cc.get_order(order_id)

    # print "Upload Order Document"
    # cc.upload_order_document(order_id, upload_file_path)

    # ------
    # SAMPLES
    # ------

    # print "List Samples"
    # samples = cc.get_samples()
    # print samples

    # print "Paged Samples"
    # paged_samples = cc.get_samples(start=len(samples)-2, limit=1)
    # print paged_samples
    # assert(len(paged_samples), 1)

    # print "Only In Progress Samples"
    # in_progress_samples = cc.get_samples(order_status_id=2)
    # print in_progress_samples

    # print "Sample Details"
    # print cc.get_sample(sample_id)

    # print "Submit Sample Test Results"
    # cc.submit_test_results(sample_id, test_results)

    # print "Upload Sample COA"
    # cc.upload_sample_coa(
    #     sample_id,
    #     sample_coa_path,
    # )

    # print "Upload Sample Image"
    # cc.upload_sample_image(
    #     sample_id,
    #     sample_image_path,
    #     set_as_cover=set_sample_cover
    # )

    # ------
    # INFO
    # ------

    # print "COMPOUNDS"
    # print cc.get_compounds()

    # print "ORDER STATUSES"
    # print cc.get_order_statuses()

    # print "SAMPLE CATEGORIES"
    # print cc.get_sample_categories()

    # print "SAMPLE TYPES"
    # print cc.get_sample_types()

    # print "TEST TYPES"
    # print cc.get_test_types()
