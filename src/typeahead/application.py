import logging.config
from pkg_resources import resource_filename, resource_stream
import urllib.parse

from aiohttp import web
import aiohttp_cors
import config_loader
import yaml

from . import downstream, handlers

logger = logging.getLogger(__name__)

_OPENAPI_SCHEMA_RESOURCE = 'openapi.yml'
_CONFIG_SCHEMA_RESOURCE = 'config_schema.yml'


class Application(web.Application):
    # language=rst
    """The Application.
    """

    def __init__(self, config_path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize config
        schema_filename = resource_filename(__name__, _CONFIG_SCHEMA_RESOURCE)
        self._config = config_loader.load(config_path, schema_filename)

        # logging config
        logging.config.dictConfig(self._config['logging'])

        # set base path on app
        path = urllib.parse.urlparse(self._config['web']['baseurl']).path
        if len(path) == 0 or path[-1] != '/':
            path += '/'
        self['path'] = path

        # set openapi spec on app
        with resource_stream(__name__, _OPENAPI_SCHEMA_RESOURCE) as s:
            self['openapi'] = yaml.load(s)

        # set search endpoints on app
        self['search_endpoints'] = self._search_endpoints()

        # CORS
        cors = aiohttp_cors.setup(self, defaults={
            '*': aiohttp_cors.ResourceOptions(
                expose_headers="*", allow_headers="*"
            ),
        })

        # set routes
        cors.add(self.router.add_get(path, handlers.search.get))
        cors.add(self.router.add_get(path[:-1], handlers.search.get))
        cors.add(self.router.add_get(path + 'openapi', handlers.openapi.get))
        self.router.add_get('/metrics', handlers.metrics.get)

    @property
    def config(self) -> dict:
        return self._config

    def _search_endpoints(self):
        # language=rst
        """ Get the search endpoints from the configuration.
        """

        endpoints = []
        # read default conf
        search_conf = self.config['global_search_config']
        connect_timeout = search_conf['connect_timeout']

        # grab all configured endpoints
        for endpointconf in self.config['search_endpoints']:
            endpoint_clz = getattr(downstream, endpointconf['type'])
            read_timeout = endpointconf.get('read_timeout', search_conf['default_read_timeout'])
            max_results = endpointconf.get('max_results', search_conf['max_results_per_endpoint'])
            url = endpointconf['url']
            endpoints.append(
                endpoint_clz(self, connect_timeout, max_results, url, read_timeout)
            )
        return endpoints
