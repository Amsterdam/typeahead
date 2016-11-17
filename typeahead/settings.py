import socket

LOCAL_CONSUL_PORT = 8501

SERVICE_PORT = 8080

SERVICE_BINDING = '0.0.0.0'

SERVICE_NAME = 'typeahead'

INFERRED_IP = socket.gethostbyname(socket.gethostname())

HEALTH_CHECK_ENDPOINT = 'http://{host}:{port}/health'.format(host=INFERRED_IP,
                                                             port=SERVICE_PORT)

HEALTH_CHECK_INTERVAL = '10s'

DEBUG = True

DEFAULT_UPSTREAM_TIMEOUT = 0.5

UPSTREAM_CONFIG = {
    'hr': {
        'endpoint': 'http://hr.endpoint.internal',
        'external': 'http://datapunt.external/hr',
        'maxresults': 5,
        'weight': 10,
        'timeout': DEFAULT_UPSTREAM_TIMEOUT

    },
    'nap': {
        'endpoint': 'http://nap.endpoint.internal',
        'external': 'http://datapunt.external/nap',
        'maxresults': 5,
        'weight': 6,
        'timeout': DEFAULT_UPSTREAM_TIMEOUT
    }
}
