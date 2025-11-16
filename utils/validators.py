import re
from werkzeug.security import generate_password_hash, check_password_hash

class ValidationError(Exception):
    """Custom validation error"""
    pass

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError('Email format tidak valid')
    return True

def validate_password(password):
    """
    Validate password requirements:
    - Minimum 8 characters
    """
    if len(password) < 8:
        raise ValidationError('Password minimal 8 karakter')
    return True

def validate_name(name):
    """Validate name"""
    if not name or len(name.strip()) < 3:
        raise ValidationError('Nama minimal 3 karakter')
    return True

def hash_password(password):
    """Hash password using werkzeug"""
    return generate_password_hash(password, method='pbkdf2:sha256')

def check_password(password_hash, password):
    """Check password against hash"""
    return check_password_hash(password_hash, password)
