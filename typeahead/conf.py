import socket
import os

from typeahead_response_parsers import get_catalogus_typeahead_response


LOCAL_CONSUL_PORT = 8501

SERVICE_PORT = 8080

SERVICE_BINDING = '0.0.0.0'

SERVICE_NAME = 'typeahead'

INFERRED_IP = socket.gethostbyname(socket.gethostname())

HEALTH_CHECK_ENDPOINT = 'http://{host}:{port}/health'.format(host=INFERRED_IP,
                                                             port=SERVICE_PORT)

MIN_CHARACTERS = 3

HEALTH_CHECK_INTERVAL = '10s'

DEBUG = False

# if we run local we can test against public urls
LOCAL = False

DEFAULT_UPSTREAM_TIMEOUT = 0.5

LOGSTASH_HOST = os.getenv('LOGSTASH_HOST', '127.0.0.1')
LOGSTASH_PORT = int(os.getenv('LOGSTASH_GELF_UDP_PORT', '12201'))

UPSTREAM_CONFIG = {
    'bag': {
        'endpoint': 'http://bag-api.service.consul:8096'
                    '/atlas/typeahead/bag/',
        'maxresults': 3,
        'weight': 20,
        'timeout': DEFAULT_UPSTREAM_TIMEOUT,
    },
    'hr': {
        'endpoint': 'http://handelsregister-api.service.consul:8101'
                    '/handelsregister/typeahead/',
        'maxresults': 3,
        'weight': 19,
        'timeout': DEFAULT_UPSTREAM_TIMEOUT
    },

    'brk': {
        'endpoint': 'http://bag-api.service.consul:8096'
                    '/atlas/typeahead/brk/',
        'maxresults': 3,
        'weight': 18,
        'timeout': DEFAULT_UPSTREAM_TIMEOUT
    },
    'gebieden': {
        'endpoint': 'http://bag-api.service.consul:8096'
                    '/atlas/typeahead/gebieden/',
        'maxresults': 3,
        'weight': 17,
        'timeout': DEFAULT_UPSTREAM_TIMEOUT
    },

    'meetbouten': {
        'endpoint': 'http://nap-api.service.consul:8081'
                    '/meetbouten/typeahead/',
        'maxresults': 3,
        'weight': 16,
        'timeout': DEFAULT_UPSTREAM_TIMEOUT
    },

    'catalogus': {
        'endpoint': 'http://catalogus-api.service.consul:8104'
                    '/api/3/action/package_search',
        'maxresults': 3,
        'weight': 16,
        'timeout': DEFAULT_UPSTREAM_TIMEOUT,
        'typeahead_response': get_catalogus_typeahead_response,
    },

    'monumenten': {
        'endpoint': 'http://monumenten-api.service.consul:8099'
                    '/monumenten/typeahead/',
        'maxresults': 6,  # Maximal 3 monuments and 3 complexes . The are returned in one query
        'weight': 15,
        'timeout': DEFAULT_UPSTREAM_TIMEOUT,
    },
}

local_urls = [
    ('catalogus',  'https://api.data.amsterdam.nl/catalogus'
                   '/api/3/action/package_search'),

    ('meetbouten', 'https://api.data.amsterdam.nl'
                   '/meetbouten/typeahead/'),

    ('gebieden',  'https://api.data.amsterdam.nl'
                  '/atlas/typeahead/gebieden/'),

    ('brk', 'https://api.data.amsterdam.nl'
            '/atlas/typeahead/brk/'),

    ('hr',  'https://api.data.amsterdam.nl'
            '/handelsregister/typeahead/'),

    ('bag', 'https://api.data.amsterdam.nl'
            '/atlas/typeahead/bag/'),

    ('monumenten', 'https://api.data.amsterdam.nl'
                   '/monumenten/typeahead/')
]

# make typeahead work localy.
if LOCAL:
    for dataset, url in local_urls:
        UPSTREAM_CONFIG[dataset]['endpoint'] = url
