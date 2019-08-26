import logging
import typing as T
import urllib.parse

import aiohttp.client
import aiohttp.client_exceptions
import aiohttp.web
from aioelasticsearch import Elasticsearch
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
            expanded = jsonld.expand(result)
            datasets = expanded[0]['http://www.w3.org/ns/dcat#dataset'][0]['@list']
            if len(datasets) > 0:
                total_results = expanded[0]['http://rdfs.org/ns/void#documents'][0]['@value']
                result_dict = {
                    "label": "Datasets",
                    "content": [
                        {
                            '_display': d['http://purl.org/dc/terms/title'][0]['@value'],
                            'uri': urllib.parse.urlparse(d['@id']).path[1:]
                        }
                        for d in datasets],
                    "total_results": total_results
                }
                return [result_dict]

        return []


class Typeahead(SearchEndpoint):

    async def search(self, q: str, authorization_header: T.Optional[str]) -> T.List[dict]:
        headers = (authorization_header is not None and {'Authorization': authorization_header}) or {}
        req = self.session.get(self.url, timeout=self.read_timeout, params={'q': q, 'limit': self.max_results},
                          headers=headers)
        results = []
        async with req as response:
            result = await response.json()
            if len(result) > 0:
                for r in result:
                    if 'content' in r:
                        l = len(r['content'])
                        if l > 0:
                            if 'total_results' not in r: # Monumenten endpoint should include its own total_results
                                r['total_results'] = l
                            if l > self.max_results:
                                r['content'] = r['content'][:self.max_results]
                            results.append(r)
        return results


class DrupalElasticSearch(SearchEndpoint):

    async def initialize(self, app):
        self.session = Elasticsearch(
            sniff_timeout = self.read_timeout   # default 0.1
        )

    async def deinitialize(self, app):
        await self.session.close()

    async def search(self, q: str, authorization_header: T.Optional[str]) -> T.List[dict]:

        # Default localhost 9200. Index is last part of path
        index = self.url.split('/')[-1]
        base_url = ''.join(self.url.split('/')[0:-1])
        drupal_selector = '/jsonapi/node/article/?filter[drupal_internal__nid]='
        query = q + '*'
        response = await self.session.search(index=index, analyze_wildcard=True, q=query, size=self.max_results)
        if 'hits' in response and len(response['hits']['hits']) > 0:
            result_dict = {
                "label": "Articles",
                "content": [
                    {
                        '_display': hit['_source']['field_short_title'][0],
                        'uri': f"{base_url}{drupal_selector}{hit['_source']['nid'][0]}",
                    }
                    for hit in response['hits']['hits']],
                "total_results": response['hits']['total']
            }
            return [result_dict]
        else:
            return []
