import argparse
import asyncio

from aiohttp import web
import uvloop

from typeahead import application


def run():
    parser = argparse.ArgumentParser(description='Typeahead service')
    parser.add_argument(
        '--config', '-c', action='store', metavar='path_to_configfile', required=True,
        help='Specify the path to your configuration file.')
    args = parser.parse_args()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    aio_app = application.Application(args.config)
    web.run_app(aio_app, port=aio_app.config['web']['port'])
    return 0


if __name__ == '__main__':
    run()
