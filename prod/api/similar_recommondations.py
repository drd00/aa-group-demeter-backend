from flask import Flask,jsonify, request
from flask_restful import Resource
import numpy as np
from api.security.verify_token import verify_token

existing_data = [
    {'uid': 97577, 'age': 30, 'bmi': 22, 'food_list': [{'food': 'Salmon Fillet', 'calories': 205, 'protein': 11.8, 'fat': 4.4, 'carbs': 3.3}]},
    {'uid': 23146, 'age': 23, 'bmi': 17, 'food_list': [{'food': 'Peanut butter', 'calories': 232, 'protein': 6.0, 'fat': 7.1, 'carbs': 19.9}]},
    {'uid': 14590, 'age': 50, 'bmi': 20, 'food_list': [{'food': 'Oatmeal', 'calories': 68, 'protein': 5.3, 'fat': 2.6, 'carbs': 27}]},
    {'uid': 52273, 'age': 40, 'bmi': 26, 'food_list': [{'food': 'Apple', 'calories': 122, 'protein': 14.9, 'fat': 2.8, 'carbs': 37.3}]},
    {'uid': 95805, 'age': 28, 'bmi': 23, 'food_list': [{'food': 'Banana', 'calories': 121, 'protein': 1.1, 'fat': 0.3, 'carbs': 23.0}]}
]

class FoodPreference(Resource):
    method_decorators = [verify_token]  # Apply the token verification decorator to all methods

    def get(self,**kwargs):
        print("called this funct")
        uid = kwargs.get('user_id')
        print(uid)

        # age = request.args.get('age', type=int)
        # height = request.args.get('height', type=float)  # Height in feet
        # weight = request.args.get('weight', type=float)
        age = 10
        height = 7
        weight = 20        
        
        if not all([age, height, weight]):
            return {'error': 'Missing required parameters'}, 400

        # Convert height from feet to meters and calculate BMI
        height_meters = height * 0.3048  # 1 foot = 0.3048 meters
        bmi = weight / (height_meters ** 2)

        # Fetch the user's food preference based on their profile
        food_preference = self.get_food_preference( age, bmi)
        food_preference_serializable = {
            'food_list': [{
                'food': item['food'],
                'calories': item['calories'],
                'protein': item['protein'],
                'fat': item['fat'],
                'carbs': item['carbs']
            } for item in food_preference]
        }
        return food_preference_serializable


    def get_food_preference(self, age, bmi):
        # existing_data_dict = {data['uid']: data for data in existing_data}
        age_bmi_data = np.array([(data['age'], data['bmi']) for data in existing_data])
        new_data = np.array([age, bmi])
        distances = np.linalg.norm(age_bmi_data - new_data, axis=1)
        closest_index = np.argmin(distances)
        closest_array = existing_data[closest_index]
        return closest_array['food_list']