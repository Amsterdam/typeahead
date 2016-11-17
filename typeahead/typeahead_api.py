# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask_restful import reqparse
from gevent import monkey
import sys

from TypeAheadQueryTask import TypeAheadQueryTask

monkey.patch_all(thread=False, select=False)


class TypeAheadRequest(Resource):
    """
    Query for typeahead
    in: q=da
    terug:[{label: 'type', content: [{uri: '', _display: ''}, ..]}, ...]
    ---
    tags:
          - typeahead
        definitions:
          - schema:
              id: keystrokes
              properties:
                name:
                 type: string
                 description: the text entered by the user
        parameters:
          - in: body
            name: body
            schema:
              id: keystrokes
              required:
                - q
              properties:
                q:
                  type: string
                  description: The characters the user typed sofar
        responses:
          200:
            description: Typing suggestions

    """

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q', type=str, help='the characters typed')
        args = parser.parse_args()

        try:
            return TypeAheadQueryTask(
                query=args['q'],
                overall_timeout=1
            ).work().json_serializable(), 200
        except():
            print("Unexpected error:", sys.exc_info()[0])
            return {}, 500

    def post(self):
        return self.get()
