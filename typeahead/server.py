import logging as level
import sys
import graypy

from logging import Logger, StreamHandler

from flask import Flask
from flask.json import jsonify
from flask_restful import Api
from flask_swagger import swagger

import conf
from typeahead_api import TypeAheadRequest

app = Flask(__name__)
api = Api(app)

app.url_map.strict_slashes = False

service_id = -1
consul_service = None
consul_client = None


@app.route("/health", methods=['GET'])
def health():
    """
    No database so all request reaching this endpoint mean the service is ok
    :return: the string OK
    """
    if conf.DEBUG:
        return 'running in debug mode..', 500
    return 'api status: OK'


@app.route("/typeahead/spec.json")
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
    handler = graypy.GELFHandler(conf.LOGSTASH_HOST, conf.LOGSTASH_PORT)
    handler.setLevel(level.ERROR)
    log.addHandler(StreamHandler(stream=sys.stdout))
    log.addHandler(handler)
    log.setLevel(level.INFO)
    log.info("Spawning awesomeness: Typeahead API")

# Mount API endpoints
typahead_view = TypeAheadRequest.as_view('typeahead')
app.add_url_rule('/typeahead/', methods=['GET'], view_func=typahead_view)

# And Run
if __name__ == '__main__':
    app.run(debug=conf.DEBUG,
            host=conf.SERVICE_BINDING,
            port=conf.SERVICE_PORT)
