# -*- coding: utf-8 -*-
import logging as level
import sys
from logging import Logger, StreamHandler

from flask import Flask, current_app
from flask.json import jsonify
from flask_restful import Api
from flask_swagger import swagger

import conf
import typeahead_api
import util

app = Flask(__name__)
api = Api(app)

service_id = -1
consul_service = None
consul_client = None


@app.route("/health", methods=['GET'])
def health():
    """
    No database so all request reaching this endpoint mean the service is ok
    :return: the string OK
    """
    return 'api status: OK'


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Typeahead API"
    return jsonify(swag)


@app.route('/', methods=['GET'])
def index():
    return "up and running"


with app.app_context():
    log = Logger(__name__)
    log.addHandler(StreamHandler(stream=sys.stdout))
    log.setLevel(level.INFO)
    log.info("Spawning awesomeness: Typeahead API")

# Mount API endpoints
api.add_resource(typeahead_api.TypeAheadRequest, '/tr')

# And Run
if __name__ == '__main__':
    app.run(debug=conf.DEBUG,
            host=conf.SERVICE_BINDING,
            port=conf.SERVICE_PORT)
