from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
import os

from api.security.firebase import initialise_firebase
from api.profile import Profile 
from api.searchfood import SearchFood
from api.diary import Diary
from api.settings import UserSettings, UpdateUserSettings
from api.default_settings import default_settings  # Import default settings

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path, override=True)

# Initialise Firebase authentication
initialise_firebase()

app = Flask(__name__)
api = Api(app)

# Enable CORS
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE"])

# Add resource endpoints
api.add_resource(SearchFood, '/searchfood/<string:food_name>')
api.add_resource(Profile, '/profile')
api.add_resource(Diary, '/diary')
api.add_resource(UserSettings, '/settings')
# Endpoint to get default settings
@app.route('/api/default-settings')
def get_default_settings():
    return jsonify(default_settings)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
