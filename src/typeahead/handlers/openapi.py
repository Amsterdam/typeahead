import copy
import json

from aiohttp import web


_OPENAPI_SCHEMA = None
"""Cache"""


async def get(request: web.Request):
    # language=rst
    """Produce the OpenAPI3 definition of this service."""
    global _OPENAPI_SCHEMA
    if _OPENAPI_SCHEMA is None:
        openapi_schema = copy.deepcopy(request.app['openapi'])
        _OPENAPI_SCHEMA = openapi_schema
    else:
        openapi_schema = _OPENAPI_SCHEMA
    c = request.app.config
    # add base url to servers
    openapi_schema['servers'] = [{'url': c['web']['baseurl']}]
    text = json.dumps(openapi_schema, indent='  ', sort_keys=True)
    return web.Response(
        text=text,
        content_type='application/json'
    )
