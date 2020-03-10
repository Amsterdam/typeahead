import argparse
import asyncio
import os

from aiohttp import web
from aiohttp.web import normalize_path_middleware
import uvloop
import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration


from typeahead import application


def run():
    parser = argparse.ArgumentParser(description='Typeahead service')
    parser.add_argument(
        '--config', '-c', action='store', metavar='path_to_configfile', required=True,
        help='Specify the path to your configuration file.')
    args = parser.parse_args()

    sentry_dsn = os.getenv('SENTRY_DSN')
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            environment='typeahead',
            integrations=[AioHttpIntegration()]
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    aio_app = application.Application(
        args.config, middlewares=[normalize_path_middleware()])
    web.run_app(aio_app, port=aio_app.config['web']['port'])
    return 0


if __name__ == '__main__':
    run()
