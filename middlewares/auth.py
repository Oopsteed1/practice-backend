# middlewares/auth.py
from functools import wraps
from flask import request, jsonify, current_app
from jose import jwt
from app.models import User
from flask import g

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            print(decoded_token)
            g.current_user = User.query.filter_by(userName=decoded_token['sub']).first()
            if not g.current_user:
                return jsonify({'error': 'User not found!'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.JWTError as e:
            print(f'JWT decoding error: {e}')
            return jsonify({'error': 'Invalid token'}), 401

        return func(*args, **kwargs)

    return wrapper
