from flask import jsonify
from typing import Any, Dict, Optional

def success_response(
    data: Optional[Any] = None,
    message: str = 'Success',
    status_code: int = 200
) -> tuple:
    """
    Return a success response
    
    Args:
        data: Response data
        message: Response message
        status_code: HTTP status code
    
    Returns:
        Tuple of (response dict, status code)
    """
    response = {
        'success': True,
        'message': message,
        'data': data
    }
    return jsonify(response), status_code

def error_response(
    message: str = 'Error',
    error: str = 'ERROR',
    status_code: int = 400,
    details: Optional[Dict] = None
) -> tuple:
    """
    Return an error response
    
    Args:
        message: Error message
        error: Error code/type
        status_code: HTTP status code
        details: Additional error details
    
    Returns:
        Tuple of (response dict, status code)
    """
    response = {
        'success': False,
        'message': message,
        'error': error
    }
    if details:
        response['details'] = details
    
    return jsonify(response), status_code
