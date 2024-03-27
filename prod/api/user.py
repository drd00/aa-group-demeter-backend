from flask import request
from flask_restful import Resource
import sqlite3
from api.security.verify_token import verify_token

class User(Resource):
    method_decorators = [verify_token]
    def get(self):
        uid = request.decoded_token['uid']
        return {
            "uid": uid
        }

