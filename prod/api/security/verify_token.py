from flask import request, jsonify
import firebase_admin.auth as firebase_auth
from functools import wraps

def verify_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": 'No token provided.'}), 403
        try:
            token = token.split(" ")[1]
            decoded_token = firebase_auth.verify_id_token(token)
            request.decoded_token = decoded_token
        except Exception as e:
            return jsonify({"message": 'Invalid token provided.', 'error': str(e)}), 403
        return f(*args, **kwargs)
    return wrapper

