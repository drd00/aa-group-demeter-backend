from flask import Flask
from flask_restful import Resource, Api
import sqlite3

app = Flask(__name__)
api = Api(app)

# super simple endpoint for the sake of example,
# do not use something this specific
class Age(Resource):
    def get(self, id):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute("SELECT age FROM user_info WHERE id=?", (id,))
        return {'age': c.fetchall()}
