from flask import request, jsonify
from flask_restful import Resource
from db.profile import verify_profiletable, get_profile, create_profile
from api.security.verify_token import verify_token

class Profile(Resource):
    method_decorators = [verify_token]
    def get(self):
        verify_profiletable()
        uid = request.decoded_token['uid']
        profile = get_profile(uid)

        if profile is None:
            return jsonify({"status": 404, "message": "Profile not found"})
        
        return jsonify({
            "uid": profile[0],
            "firstname": profile[1],
            "lastname": profile[2],
            "age": profile[3],
            "weight": profile[4],
            "goalweight": profile[5],
            "height": profile[6],
            "primarygoal": profile[7],
            "activitylevel": profile[8]
        })
    
    def post(self):
        data = request.get_json()
        uid = create_profile(data['firstname'], data['lastname'], data['age'], data['weight'], data['goalweight'], data['height'], data['primarygoal'], data['activitylevel'])

        if uid == None:
            return jsonify({"status": 400, "message": "Profile already exists"})
        
        return jsonify({"status": 200})
