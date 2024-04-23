import datetime
from flask import request
from flask_restful import Resource
from api.db.diary import verify_diarytable, get_diary, create_entry
from api.security.verify_token import verify_token

class Diary(Resource):
    method_decorators = [verify_token]
    def get(self, **kwargs):
        verify_diarytable()
        uid = kwargs.get('user_id')
        date = datetime.date.today()
        date_str = date.strftime('%Y-%m-%d') # should maybe do some verification here with the frontend to account for timezones and what not
        entries = get_diary(uid, date_str)

        if entries is None:
            return {'message': 'Diary not found'}, 404
        
        # Initialize an empty list to store diary entries
        diary_entries = []

        # Iterate over each row and unpack the tuple into a dictionary
        for entry in entries:
            diary_entry = {
                "uid": entry[0],
                "date": entry[1],
                "calories": entry[2],
                "protein": entry[3],
                "fat": entry[4],
                "carbs": entry[5],
                "food": entry[6]
            }
            # Append the dictionary to the list
            diary_entries.append(diary_entry)

        # Flask-Restful automatically jsonify your list of dictionaries.
        return diary_entries, 200


    def post(self, **kwargs):
        data = request.get_json()
        user_id = kwargs.get('user_id')
        date = datetime.date.today()
        date_str = date.strftime('%Y-%m-%d')

        # Create a diary entry
        create_entry(user_id, date_str, data['calories'], data['protein'], data['fat'], data['carbs'], data['food'])
        
        return {"message": 'OK'}, 200
