import asyncio
from aiohttp import web

from typeahead import metrics


async def get(request):
    # language=rst
    """Run search.
    """
    with metrics.REQUEST_TIME.time():
        q = request.query.get('q', '').strip()
        min_query_length = request.app.config['global_search_config']['min_query_length']
        authz = request.headers.get('Authorization', None)
        # only perform search for queries longer than min_query_length
        if len(q) < min_query_length:
            return web.json_response([])
        # perform searches
        searches = [e.wrappedsearch(q, authz) for e in request.app['search_endpoints']]
        # gather responses
        results = []
        for result in await asyncio.gather(*searches, return_exceptions=True):
            if isinstance(result, list):
                results.extend(result)
        return web.json_response(results)
