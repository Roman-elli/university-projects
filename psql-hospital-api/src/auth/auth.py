import jwt

from functools import wraps
from flask import request, jsonify
from config import Config

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            token = token.split(" ")[1]  # Assuming the token is sent as "Bearer <token>"
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            kwargs['current_user'] = data['username']
            kwargs['user_type'] = data['user_type']
            kwargs['user_id'] = data['user_id']
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated_function
