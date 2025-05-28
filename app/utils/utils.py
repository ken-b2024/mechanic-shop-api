from datetime import datetime, timedelta, timezone
from jose.exceptions import ExpiredSignatureError, JWTError
from jose import jwt
from functools import wraps
from flask import request, jsonify
import os


SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretloginkey'

def encode_token(user_id, role):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(user_id),
        'role': role
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization'in request.headers:
            print("Authorization Header:", request.headers['Authorization'])

            token = request.headers['Authorization'].split()
            if len(token) != 2 or token[0].lower() != 'bearer':
                return jsonify({"message": "Invalid Authorization header format"}), 400

            token = token[1]

            if not token:
                return jsonify({"message": "missing token"}), 400
            
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                print("Decoded token:", data)
                user_id = data['sub']
                role = data['role']
            except ExpiredSignatureError as e:
                return jsonify({"message": "token expired"}), 400
            except JWTError as e:
                print("JWTError:", str(e))
                return jsonify({"message": "Invalid token"}), 400

            return f(*args, user_id=user_id, role=role, **kwargs)
        else:
            return jsonify({"message": "You must be logged in to access this resource."}), 400
    
    return decorated