# -*- coding: utf-8 -*-
from flask_restful import Resource


class TypeAheadRequest(Resource):
    def get(self):
        return {'get': 'response'}

    def post(self):
        return {'post': 'response'}
