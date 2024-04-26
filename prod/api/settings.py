from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from db import settings
from api.db.default_settings import DEFAULT_SETTINGS

app = Flask(__name__)
api = Api(app)

# Endpoint to get user settings by user ID
class UserSettings(Resource):
    def get(self, uid):
        settings_data = settings.get_settings(uid)
        if settings_data:
            settings_dict = {
                'uid': settings_data[0],
                'calorie_compensation': settings_data[1],
                'protein_goal': settings_data[2],
                'display_calories': settings_data[3],
                'display_protein': settings_data[4],
                'display_fat': settings_data[5],
                'display_carbs': settings_data[6]
            }
            return jsonify(settings_dict)
        else:
            # Modify default settings here
            DEFAULT_SETTINGS['uid'] = uid
            return jsonify(DEFAULT_SETTINGS)

# Endpoint to update user settings
class UpdateUserSettings(Resource):
    def put(self, uid):
        # Get the updated settings from the request body
        updated_settings = request.json
        # Update the settings in the database
        settings.update_settings(uid, **updated_settings)
        return jsonify({'message': 'User settings updated successfully'})

api.add_resource(UserSettings, '/api/settings/<int:uid>')
api.add_resource(UpdateUserSettings, '/api/settings/<int:uid>')

if __name__ == '__main__':
    app.run(debug=True)
