from flask import request
from flask_restful import Resource
from api.db.diary import verify_diarytable, get_diary


class Diary(Resource):
    def get(self):
        verify_diarytable()
        rows = get_diary()

        if not rows:
            return {'message': 'Diary not found'}, 404

        # Initialize an empty list to store diary entries
        diary_entries = []

        # Iterate over each row and unpack the tuple into a dictionary
        for row in rows:
            diary_entry = {
                "uid": row[0],
                "date": row[1],
                "calories": row[2],
                "protein": row[3],
                "fat": row[4],
                "carbs": row[5],
                "food": row[6]
            }
            # Append the dictionary to the list
            diary_entries.append(diary_entry)

        # Flask-Restful automatically jsonify your list of dictionaries.
        return diary_entries, 200
