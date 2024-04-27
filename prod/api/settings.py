from flask import request, jsonify
from flask_restful import Resource
from api.db.settings import get_settings, update_settings
from api.db.default_settings import DEFAULT_SETTINGS
from api.security.verify_token import verify_token
import json

# Endpoint to get user settings by user ID
class Settings(Resource):
    method_decorators = [verify_token]
    def get(self, **kwargs):
        uid = kwargs.get('user_id')
        settings_data = get_settings(uid)

        if settings_data:
            settings_dict = {
                'uid': settings_data["uid"],
                'calorie_compensation': settings_data["calorie_compensation"],
                'protein_goal': settings_data["protein_goal"],
                'display_calories': settings_data["display_calories"],
                'display_protein': settings_data["display_protein"],
                'display_fat': settings_data["display_fat"],
                'display_carbs': settings_data["display_carbs"]
            }
            return settings_dict, 200
        else:
            default_set = DEFAULT_SETTINGS
            default_set['uid'] = uid
            return default_set, 200
    
    def post(self, **kwargs):
        uid = kwargs.get('user_id')
        updated_settings = request.get_json()
        json_settings = json.loads(updated_settings)
        update = update_settings(uid, calorie_compensation=json_settings['calorie_compensation'], protein_goal=json_settings['protein_goal'], display_calories=json_settings['display_calories'], display_protein=json_settings['display_protein'], display_fat=json_settings['display_fat'], display_carbs=json_settings['display_carbs'])

        if update is not None:
            return {"message": 'OK'}, 200
        else:
            return {"message": "Initial settings not found"}, 404
