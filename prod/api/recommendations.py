from flask_restful import Resource
from api.security.verify_token import verify_token
from api.db.search_history import verify_searchtable, probabilistic_sample_recommender

class Recommendations(Resource):
    method_decorators = [verify_token]

    def get(self, **kwargs):
        uid = kwargs.get('uid')

        verify_searchtable()

        # Sample from the table 10 times.
        recommendations = []
        n_samples = 10
        recommendations = probabilistic_sample_recommender(uid, n_samples)  # Python list

        if len(recommendations) == 0:
            return {'message': 'No recommendations found.'}, 404
        else:
            return {'recommendations': recommendations}, 200

