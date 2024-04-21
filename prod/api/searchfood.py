from flask_restful import Resource
import requests
import os
import sqlite3
from api.security.verify_token import verify_token
from api.db.profile import get_profile
from api.db.settings import get_settings
from api.db.search_history import decay_weight, verify_searchtable, insert_search_history, clear_low_weight

def gen_recommendations(uid, response_data):
    def generate_bmi_weight(weight, height):
        bmi = float(weight) / (float(height) * float(height))

        if bmi < 18.5:
            return 'underweight'
        elif bmi >= 18.5 and bmi < 25:
            return 'normal'
        elif bmi >= 25 and bmi < 30:
            return 'overweight'
        else:
            return 'obese'

    relevant_response_fields = response_data['hints']

    # Verify a search table exists and create this otherwise.
    verify_searchtable()

    # Decay probabilities of existing recommendations if present.
    decay_weight(uid)

    # Clear entries from the table which have a weight below 1.0
    clear_low_weight(uid)

    # Fetch from profile and settings table for uid.
    profile = get_profile(uid)
    settings = get_settings(uid)
    if profile is not None and settings is not None:
        # Derive a BMI feature.
        bmi_w = generate_bmi_weight(profile['weight'], profile['height'])

        # Generate a dictionary of stochastic weights for each food item.
        weights_dict = {}
        for food in relevant_response_fields:
            food_tuple = (food['food']['foodId'], food['food']['label'])    # (id, name)
            weights_dict[food_tuple] = 0.0
            if bmi_w == 'underweight':
                if 'ENERC_KCAL' in food['food']['nutrients']:
                    # filter by 'higher calorie' foods.
                    if float(food['food']['nutrients']['ENERC_KCAL']) > 500:
                        weights_dict[food_tuple] += 5.0
            elif bmi_w == 'normal':
                if 'ENERC_KCAL' in food['food']['nutrients']:
                    # filter by 'medium calorie' foods.
                    if float(food['food']['nutrients']['ENERC_KCAL']) > 200 and float(food['food']['nutrients']['ENERC_KCAL']) < 500:
                        weights_dict[food_tuple] += 1.0
            elif bmi_w == 'overweight':
                if 'ENERC_KCAL' in food['food']['nutrients']:
                    # filter by 'lower calorie' foods.
                    if float(food['food']['nutrients']['ENERC_KCAL']) < 600:
                        weights_dict[food_tuple] += 5.0
            
            # Good ratio for protein is 10g per 100kcal.
            if 'PROCNT' in food['food']['nutrients']:
                cals = float(food['food']['nutrients']['ENERC_KCAL'])
                protein = float(food['food']['nutrients']['PROCNT'])
                protein_kcal = 4 * protein
                percentage_protein = (protein_kcal / cals) * 100
                if percentage_protein >= 10.0:
                    weights_dict[food_tuple] += 5.0
            
        for food in relevant_response_fields:
            insert_search_history(uid, food['food']['foodId'], food['food']['label'], weights_dict[(food['food']['foodId'], food['food']['label'])])
    else:
        print("Profile or settings not found for user.")
        return None

    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'search_history.db'))

    return None

class SearchFood(Resource):
    method_decorators = [verify_token]
    def get(self, food_name, **kwargs):
        uid = kwargs.get('user_id')
        url = f"https://api.edamam.com/api/food-database/v2/parser?app_id={os.getenv('EDAMAM_APP_ID')}&app_key={os.getenv('EDAMAM_APP_KEY')}&ingr={food_name}"
        response = requests.get(url)

        data = response.json()
        gen_recommendations(uid, data)

        return data

