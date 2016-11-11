# -*- coding: utf-8 -*-
import logging as level
import sys
from consul.aio import Consul
from logging import Logger, StreamHandler

from flask import Flask
from flask.json import jsonify
from flask_restful import Api
from flask_swagger import swagger

import settings
import typeahead_api
import util

log = Logger(__name__)
log.addHandler(StreamHandler(stream=sys.stdout))
log.setLevel(level.INFO)

consul_host = util.get_consul_host()

log.info('Connecting to Consul')
consul_client = Consul(host=consul_host['host'],
                       port=consul_host['port'])
consul_service = consul_client.agent.service
service_id = util.register(consul_client, consul_service)

log.info("Spawning awesomeness: Typeahead API")

app = Flask(__name__)
api = Api(app)


@app.route("/health", methods=['GET'])
def health():
    return "OK"


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Typeahead API"
    return jsonify(swag)


@app.route('/', methods=['GET'])
def index():
    return "up and running"


# Mount API endpoints
api.add_resource(typeahead_api.TypeAheadRequest, '/tr')

# And Run
if __name__ == '__main__':
    try:
        app.run(debug=settings.DEBUG,
                host=settings.SERVICE_BINDING,
                port=settings.SERVICE_PORT)
    finally:
        consul_service.deregister(service_id=service_id)
