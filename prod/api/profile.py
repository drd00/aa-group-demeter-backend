from flask import request
from flask_restful import Resource
from api.db.profile import verify_profiletable, get_profile, create_profile
from api.security.verify_token import verify_token

class Profile(Resource):
    method_decorators = [verify_token]
    def get(self, **kwargs):
        verify_profiletable()
        uid = kwargs.get('user_id')
        profile = get_profile(uid)

        if profile is None:
            return {'message': 'Profile not found'}, 404
        
        return {
            "uid": profile['uid'],
            "firstName": profile['firstName'],
            "lastName": profile['lastName'],
            "age": profile['age'],
            "weight": profile['weight'],
            "goalWeight": profile['goalWeight'],
            "height": profile['height'],
            "activityLevel": profile['activityLevel']
        }, 200
    
    def post(self, **kwargs):
        data = request.get_json()
        print(f"jsondata: {data}")
        user_id = kwargs.get('user_id')
        print(f"user_id: {user_id}")
        uid = create_profile(user_id, data['firstName'], data['lastName'], data['age'], data['weight'], data['goalWeight'], data['height'], data['activityLevel'])

        if uid == None:
            return {"message": "Profile already exists"}, 400
        
        return {"message": 'OK'}, 200
    

    # def put(self):
    #     data = request.get_json()
    #     uid = request.decoded_token['uid']
    #     profile = get_profile(uid)

    #     if profile is None:
    #         return {'message': 'Profile not found'}, 404
        
    #     create_profile(uid, data['firstname'], data['lastname'], data['age'], data['weight'], data['goalweight'], data['height'], data['activitylevel'])

