from pkg_resources import resource_filename

import aiohttp.client
import pytest
from typeahead import application, downstream


def _downstream_get_func(resp):
    async def get(*args, **kwargs):
        class Response:
            async def json(self):
                return resp
        return Response()
    return get


@pytest.fixture(scope='function')
async def server(aiohttp_server):
    config_path = resource_filename(__name__, 'test.config.yml')
    return await aiohttp_server(application.Application(config_path))


async def test_ckan_endpoint(monkeypatch, server):
    endpoints = [e for e in server.app['search_endpoints'] if type(e) if downstream.CKAN]
    for e in endpoints:
        monkeypatch.setattr(e.session, 'get', _downstream_get_func([]))
        #assert (await e.search('q', None)) == []


async def test_dcatd_endpoint(monkeypatch, server):
    endpoints = [e for e in server.app['search_endpoints'] if type(e) if downstream.DCATAms]
    for e in endpoints:
        monkeypatch.setattr(e.session, 'get', _downstream_get_func([]))


async def test_typeahead_endpoint(monkeypatch, server):
    endpoints = [e for e in server.app['search_endpoints'] if type(e) if downstream.Typeahead]
    for e in endpoints:
        monkeypatch.setattr(e.session, 'get', _downstream_get_func([]))
