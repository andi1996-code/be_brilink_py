import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from models.user import TokenBlacklist

SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

def generate_token(user_id, user_email, expires_in_hours=24):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'email': user_email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=expires_in_hours)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    """Verify JWT token"""
    try:
        # Check if token is blacklisted
        blacklisted = TokenBlacklist.query.filter_by(token=token).first()
        if blacklisted:
            raise ValueError('Token sudah logout')
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token sudah expired')
    except jwt.InvalidTokenError:
        raise ValueError('Token tidak valid')

def token_required(f):
    """Decorator untuk protect endpoints"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({
                    'success': False,
                    'message': 'Format Authorization header salah (Bearer <token>)',
                    'error': 'INVALID_HEADER_FORMAT'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token diperlukan',
                'error': 'MISSING_TOKEN'
            }), 401
        
        try:
            payload = verify_token(token)
            request.user_id = payload['user_id']
            request.user_email = payload['email']
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e),
                'error': 'INVALID_TOKEN'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated
