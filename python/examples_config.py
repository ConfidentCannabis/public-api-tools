api_key = 'PUT_YOUR_API_KEY_HERE'
api_secret = 'PUT_YOUR_API_SECRET_HERE'

client_id = 1
order_id = 'ORDER_NUMBER_HERE'
sample_id = '{}.SAMPLE_NUMBER_HERE'.format(order_id)
upload_file_path = 'path-to-file'
sample_coa_path = 'path-to-coa-file.pdf'
sample_image_path = 'path-to-image.png'
set_sample_cover = True


bad_test_results = {
    'missing_required_field': {
        'categories': {
            'cannabinoids': {
                'info_fields': {
                    'input_units': '%',
                    'report_units': 'mg/ml',
                },
                'compounds': [
                    {
                        'name': 'thca',
                        'value': '0.19',
                        'loq': '0.01'
                    },
                ]
            },
        }
    },
    'unit_not_allowed': {
        'categories': {
            'cannabinoids': {
                'info_fields': {
                    'input_units': '%',
                    'report_units': 'cq',
                },
                'compounds': [
                    {
                        'name': 'thca',
                        'value': '0.19',
                        'loq': '0.01'
                    },
                ]
            },
        }
    },
    'invalid_units': {
        'categories': {
            'cannabinoids': {
                'info_fields': {
                    'input_units': '%',
                    'report_units': 'notaunit',
                },
                'compounds': [
                    {
                        'name': 'thca',
                        'value': '0.19',
                        'loq': '0.01'
                    },
                ]
            },
        }
    },
    'unknown_compound': {
        'categories': {
            'cannabinoids': {
                'info_fields': {
                    'input_units': '%',
                    'report_units': '%',
                },
                'compounds': [
                    {
                        'name': 'notathing',
                        'value': '0.19',
                        'loq': '0.01'
                    },
                ]
            },
        }
    },
    'suspicious_date': {
        'categories': {
            'cannabinoids': {
                'info_fields': {
                    'input_units': '%',
                    'report_units': '%',
                    'date_tested': '2010-01-01'
                },
                'compounds': [
                    {
                        'name': 'thca',
                        'value': '0.01',
                        'loq': '0.01'
                    }
                ]
            }
        }
    },
    'invalid_date': {
        'categories': {
            'cannabinoids': {
                'info_fields': {
                    'input_units': '%',
                    'report_units': '%',
                    'date_tested': '20161021'
                },
                'compounds': [
                    {
                        'name': 'thca',
                        'value': '0.01',
                        'loq': '0.01'
                    }
                ]
            }
        }
    },


    'invalid_status': {
        'categories': {
            'pesticides': {
                'info_fields': {
                    'input_units': '%',
                    'report_units': '%',
                    'status': 3
                },
                'compounds': [
                    {
                        'name': 'abamectin',
                        'value': '0.1',
                        'loq': '0.01'
                    }
                ]
            },
        }
    },
    'duplicate_compound': {
        'categories': {
            'cannabinoids': {
                'info_fields': {
                    'input_units': '%',
                    'report_units': '%',
                },
                'compounds': [
                    {
                        'name': 'thca',
                        'value': '0.19',
                        'loq': '0.01'
                    },
                    {
                        'name': 'thca',
                        'value': '0.01',
                        'loq': '0.01'
                    },
                ]
            },
        }
    },
    'impossible_value': {
        'categories': {
            'cannabinoids': {
                'info_fields': {
                    'input_units': 'mg/g',
                    'report_units': 'mg/g',
                },
                'compounds': [
                    {
                        'name': 'thca',
                        'value': '1001',
                        'loq': '0.01'
                    }
                ]
            },
        }
    }
}
