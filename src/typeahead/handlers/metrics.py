from aiohttp import web
from prometheus_client import core, exposition


async def get(request):
    # language=rst
    """Display service metrics as json.
    """
    registry = core.REGISTRY
    if 'name' in request.query:
        registry = registry.restricted_registry(request.query['name'])
    output = exposition.generate_latest(registry)
    return web.Response(body=output, content_type='text/plain; version=0.0.4', charset='utf-8')
