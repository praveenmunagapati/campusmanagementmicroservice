import os
import hashlib
import logging
from datetime import datetime
from functools import wraps
from flask import jsonify, request
import werkzeug

def allowed_file(filename, allowed_extensions):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def secure_filename_with_timestamp(filename):
    """Generate a secure filename with timestamp."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    secure_name = werkzeug.utils.secure_filename(filename)
    name, ext = os.path.splitext(secure_name)
    return f"{name}_{timestamp}{ext}"

def hash_password(password, salt, iterations=100000):
    """Hash a password using PBKDF2."""
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        iterations
    ).hex()

def format_response(data=None, message='Success', status_code=200):
    """Format API responses."""
    response = {
        'status': 'success' if 200 <= status_code < 300 else 'error',
        'message': message,
        'data': data
    }
    return jsonify(response), status_code

def handle_exception(e):
    """Handle exceptions and return a formatted response."""
    logging.error(f"Error: {str(e)}")
    return format_response(
        message=str(e),
        status_code=500
    )

def validate_request(schema):
    """Decorator to validate request data against a schema."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                data = request.get_json()
                schema.validate(data)
                return f(*args, **kwargs)
            except Exception as e:
                return format_response(
                    message=f"Invalid request data: {str(e)}",
                    status_code=400
                )
        return wrapper
    return decorator

def paginate_query(query, page, per_page):
    """Paginate a SQLAlchemy query."""
    return query.paginate(page=page, per_page=per_page, error_out=False)

def format_paginated_response(pagination):
    """Format a paginated response."""
    return {
        'items': [item.to_dict() for item in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': pagination.per_page
    }

def log_activity(user_id, action, details=None):
    """Log user activity."""
    logging.info(f"User {user_id} performed {action}")
    if details:
        logging.debug(f"Details: {details}")

def validate_date_range(start_date, end_date):
    """Validate a date range."""
    if start_date and end_date and start_date > end_date:
        raise ValueError("Start date must be before end date")
    return True 