from flask import Flask
from flask_restful import Resource
import requests
import os
from api.security.verify_token import verify_token

class SearchFood(Resource):
    method_decorators = [verify_token]
    def get(self, food_name):
        url = f"https://api.edamam.com/api/food-database/v2/parser?app_id={os.getenv('EDAMAM_APP_ID')}&app_key={os.getenv('EDAMAM_APP_KEY')}&ingr={food_name}"
        response = requests.get(url)

        data = response.json()

        return data

