import logging
import typing as T
import urllib.parse

import aiohttp.client
import aiohttp.client_exceptions
import aiohttp.web
from pyld import jsonld

from typeahead import metrics

_logger = logging.getLogger(__name__)


class SearchEndpoint:

    def __init__(self, app: aiohttp.web.Application, connect_timeout: int,
                 max_results: int, url: str, read_timeout: T.Optional[float]):
        self.connect_timeout = connect_timeout
        self.max_results = max_results
        self.url = url
        self.read_timeout = read_timeout
        # placeholder (each endpoint gets an own connection pool)
        self.session: aiohttp.client.ClientSession = None
        # make sure everything is initialized and cleaned up
        app.on_startup.append(self.initialize)
        app.on_cleanup.append(self.deinitialize)

    async def initialize(self, app):
        self.session = aiohttp.client.ClientSession(
            conn_timeout=self.connect_timeout, raise_for_status=True
        )

    async def deinitialize(self, app):
        await self.session.close()

    async def wrappedsearch(self, *args, **kwargs):
        u = self.url
        try:
            with metrics.ENDPOINT_SEARCHTIME.labels(endpoint=u).time():
                return await self.search(*args, **kwargs)
        except aiohttp.client_exceptions.ClientResponseError as e:
            metrics.SEARCH_RESP_COUNTER.labels(status=e.status, endpoint=u).inc()
            raise
        except Exception as e:
            metrics.SEARCH_EXC_COUNTER.labels(exc_type=repr(e), endpoint=u).inc()
            _logger.exception('Error querying {}'.format(u))
            raise

    async def search(self, q: str, authorization_header: T.Optional[str]) -> T.List[dict]:
        raise NotImplementedError()


class DCATAms(SearchEndpoint):

    async def search(self, q: str, authorization_header: T.Optional[str]) -> T.List[dict]:
        headers = (authorization_header is not None and {'Authorization': authorization_header}) or {}
        req = self.session.get(
            self.url, timeout=self.read_timeout, headers=headers,
            params={'q': q, 'limit': self.max_results}
        )
        async with req as response:
            result = await response.json()
#            expanded = jsonld.expand(result)
#            datasets = expanded[0]['http://www.w3.org/ns/dcat#dataset'][0]['@list']
            datasets = result['dcat:dataset']
            if len(datasets) > 0:
                return [{
                    "label": "Datasets",
                    "content": [
                        {
#                            '_display': d['http://purl.org/dc/terms/title'][0]['@value'],
                            '_display': d['dct:title'],
                            'uri': urllib.parse.urlparse(d['@id']).path[1:]
                        }
                        for d in datasets]
                }]
        return []


class Typeahead(SearchEndpoint):

    async def search(self, q: str, authorization_header: T.Optional[str]) -> T.List[dict]:
        headers = (authorization_header is not None and {'Authorization': authorization_header}) or {}
        req = self.session.get(self.url, timeout=self.read_timeout, params={'q': q},
                          headers=headers)
        results = []
        async with req as response:
            result = await response.json()
            if len(result) > 0:
                for r in result:
                    if 'content' in r:
                        if len(r['content']) > 0:
                            if len(r['content']) > self.max_results:
                                r['content'] = r['content'][:self.max_results]
                            results.append(r)
        return results
