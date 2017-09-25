import sys

from flask import request
from flask.json import jsonify
from flask.views import MethodView
from flask_restful import reqparse
from gevent import monkey

from TypeAheadQueryTask import TypeAheadQueryTask

monkey.patch_all(thread=False, select=False)


class TypeAheadRequest(MethodView):

    def get(self):
        """
        Query for typeahead results in underlying endpoints
        ---
        description:
            - "Look for possible objects in upstream apis"
        tags:
            - "typeahead"
        produces:
            - "application/json"
        parameters:
            -
                name: "q"
                in: "query"
                description: "The user input to search for"
                required: true
                type: "string"
        responses:
            200:
                description: "Typing suggestions"
            default:
                description: "Unexpected error"

        """
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument(
            'q',
            type=str,
            required=True,
            help='Please provide a query using the \'q\' '
                 'request parameter (eg: ?q=dam)')

        args = parser.parse_args(strict=True)

        try:
            auth = {}
            if 'Authorization' in request.headers:
                auth = {'Authorization': request.headers['Authorization']}

            response_value = TypeAheadQueryTask(
                query=args['q'],
                auth=auth,
                overall_timeout=1).work().json_serializable()
            return jsonify(response_value), 200, {
                'Content-Type': 'application/json; charset=utf-8'}
        except():
            print("Unexpected error:", sys.exc_info()[0])
            return jsonify([]), 500, {'you': 'fool'}

    def post(self):
        return self.get()
