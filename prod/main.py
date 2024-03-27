from flask import Flask 
from flask_restful import Api
from dotenv import load_dotenv
import os

from api.security.firebase import initialise_firebase
from api.user import User
from api.searchfood import SearchFood

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

api.add_resource(SearchFood, '/searchfood/<string:food_name>')
api.add_resource(User, '/user/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
