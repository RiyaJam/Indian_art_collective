import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app


def hash_password(password):
    return generate_password_hash(password)


def check_password(password, hashed):
    try:
        return check_password_hash(hashed, password)
    except Exception:
        return False


def generate_token(user_id, role, name=''):
    payload = {
        'user_id': user_id,
        'role': role,
        'name': name,
        'exp': datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRY_HOURS'])
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def decode_token(token):
    try:
        return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        data = decode_token(token)
        if not data:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        request.user = data
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                parts = request.headers['Authorization'].split()
                if len(parts) == 2 and parts[0] == 'Bearer':
                    token = parts[1]
            if not token:
                return jsonify({'error': 'Token is missing'}), 401
            data = decode_token(token)
            if not data:
                return jsonify({'error': 'Token is invalid or expired'}), 401
            if data.get('role') not in roles:
                return jsonify({'error': 'Access forbidden: insufficient permissions'}), 403
            request.user = data
            return f(*args, **kwargs)
        return decorated
    return decorator
