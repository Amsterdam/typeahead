import socket
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

DEBUG = True

DEFAULT_UPSTREAM_TIMEOUT = 0.5

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
                    '/handelsregister/typeahead',
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
        'endpoint': 'http://catalogus-api.service.consul:8104/api/3/action/package_search',
        'maxresults': 3,
        'weight': 16,
        'timeout': DEFAULT_UPSTREAM_TIMEOUT,
        'typeahead_response': get_catalogus_typeahead_response,
    },
}
