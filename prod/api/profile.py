from flask import request, jsonify
from flask_restful import Resource
from api.db.profile import verify_profiletable, get_profile, create_profile
from api.security.verify_token import verify_token

class Profile(Resource):
    method_decorators = [verify_token]
    def get(self):
        verify_profiletable()
        uid = request.decoded_token['uid']
        profile = get_profile(uid)

        if profile is None:
            return {'message': 'Profile not found'}, 404
        
        return jsonify({
            "uid": profile[0],
            "First Name": profile[1],
            "Last Name": profile[2],
            "Age": profile[3],
            "Weight": profile[4],
            "Goal Weight": profile[5],
            "Height": profile[6],
            "Primary Goal": profile[7],
            "Activity Level": profile[8]
        })
    
    def post(self):
        data = request.get_json()
        uid = create_profile(data['firstname'], data['lastname'], data['age'], data['weight'], data['goalweight'], data['height'], data['primarygoal'], data['activitylevel'])

        if uid == None:
            return jsonify({"status": 400, "message": "Profile already exists"})
        
        return jsonify({"status": 200})
