import asyncio
from aiohttp import web

from typeahead import metrics


async def get(request):
    # language=rst
    """Run search. Swallows all downstream exceptions.
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

        results_type = request.app.config['global_search_config'].get('results_type')
        if results and results_type and results_type == 'equal_until_max':
            # The result is a list of objects where the 'content' exists of embedded lists of results.
            # From each top level entry we will repeatedly take one item to till we have total_max_results items
            # But the original order needs to remain the same
            total_max_results = request.app.config['global_search_config'].get('total_max_results', 15)
            max_content_results = max([len(x['content']) for x in results])
            new_results = [{'label': x['label'], 'content': [], 'total_results': x['total_results']} for x in results]

            total_results = top_level_index = content_index = 0
            while total_results < total_max_results and content_index < max_content_results:
                if content_index < len(results[top_level_index]['content']):
                    new_results[top_level_index]['content'].append(results[top_level_index]['content'][content_index])
                    total_results += 1
                top_level_index += 1
                if top_level_index >= len(results):
                    top_level_index = 0
                    content_index += 1

            results = new_results

        return web.json_response(results)
