from flask import Flask 
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv
import os

from api.security.firebase import initialise_firebase
from api.profile import Profile 
from api.searchfood import SearchFood
from api.diary import Diary
from api.similar_recommondations import FoodPreference

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
print(dotenv_path)
dotenv_loaded = load_dotenv(dotenv_path, override=True)
print(f".env loaded: {dotenv_loaded}")

# get env variables
EDAMAM_APP_ID = os.getenv("EDAMAM_APP_ID")
EDAMAM_APP_KEY = os.getenv("EDAMAM_APP_KEY")

# initialise Firebase authentication
initialise_firebase()

app = Flask(__name__)
api = Api(app)

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE"])

api.add_resource(SearchFood, '/searchfood/<string:food_name>')
api.add_resource(Profile, '/profile')
api.add_resource(FoodPreference, '/get_food_preference')
api.add_resource(Diary, '/diary')

if __name__ == '__main__':
    app.run(port=8000,debug=True)
