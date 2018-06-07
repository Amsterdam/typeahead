from prometheus_client import Counter, Summary

REQUEST_TIME = Summary('typeahead_request_processing_seconds', 'Time spent processing request.')
ENDPOINT_SEARCHTIME = Summary('typeahead_endpoint_searchtime_seconds', 'Time spent searching an endpoint.', ['endpoint'])
SEARCH_EXC_COUNTER = Counter('typeahead_search_exceptions_total', 'Counter of all exceptions that occur during search.', ['exc_type', 'endpoint'])
SEARCH_RESP_COUNTER = Counter('typeahead_search_responses_total', 'Counter of all exceptions that occur during search.', ['status', 'endpoint'])
