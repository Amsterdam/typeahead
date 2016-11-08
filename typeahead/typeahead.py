# -*- coding: utf-8 -*-
import logging as level
import sys
import consul
import asyncio
import os
from logging import Logger, StreamHandler

from flask import Flask
from flask.json import jsonify
from flask_restful import Api
from flask_swagger import swagger

import typeahead_api, util

log = Logger(__name__)
log.addHandler(StreamHandler(stream=sys.stdout))
log.setLevel(level.INFO)

consul_host = util.get_consul_hosts()[0]

log.info('Connecting to Consul')
consul_client = consul.Consul(host=consul_host['host'],
                              port=int(consul_host['port']))
util.register(consul_client)
# c = consul.Consul(host=os.getenv("CONSUL_IP"), port=int(os.getenv("CONSUL_PORT")))


log.info('Starting consult eventloop')
# consul_client.kv.get('test')[1]['Value'].decode('utf-8')

log.info("Spawning awesomeness: Typeahead API")

app = Flask(__name__)
api = Api(app)


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
        app.run(debug=True)
    finally:
        consul_client.Agent.Service.deregister(service_id=123)
