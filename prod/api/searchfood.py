from flask import Flask, jsonify, request
from flask_restful import Resource
import requests
import os
from api.security.verify_token import verify_token

class SearchFood(Resource):
    method_decorators = [verify_token]  # Apply the token verification decorator to all methods

    def get(self, food_name):
        # Parameter validation
        if not food_name:
            return jsonify({'error': 'Food name is required'}), 400  # Return an error if no food name is provided

        food_name = food_name.strip()
        if len(food_name) < 2:  # Require at least two characters for the food name
            return jsonify({'error': 'Food name too short'}), 400  # Return an error if the food name is too short

        # Construct the request URL
        url = f"https://api.edamam.com/api/food-database/v2/parser?app_id={os.getenv('EDAMAM_APP_ID')}&app_key={os.getenv('EDAMAM_APP_KEY')}&ingr={food_name}"
        response = requests.get(url)  # Make the API request

        # Error handling
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch data from external API', 'status': response.status_code}), response.status_code  # Return an error if the API call failed

        # Data processing
        data = response.json()  # Parse the JSON response
        filtered_data = {
            'foods': [
                {'name': item['food']['label'], 'nutrients': item['food']['nutrients']}
                for item in data.get('hints', [])  # Extract relevant data from the API response
            ]
        }

        return filtered_data  # Return the filtered data
