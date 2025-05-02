import re
import logging
import structlog
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

def setup_logging(log_level: str = 'INFO') -> None:
    """Configure structured logging for the application."""
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, log_level.upper())
    )

def validate_email_format(email: str) -> bool:
    """Validate email format using email-validator."""
    try:
        validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False

def validate_phone_format(phone: str, country_code: str = 'US') -> bool:
    """Validate phone number format using phonenumbers."""
    try:
        parsed_number = phonenumbers.parse(phone, country_code)
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        return False

def format_phone_number(phone: str, country_code: str = 'US') -> Optional[str]:
    """Format phone number to international format."""
    try:
        parsed_number = phonenumbers.parse(phone, country_code)
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        return None
    except NumberParseException:
        return None

def generate_unique_id(prefix: str = '') -> str:
    """Generate a unique identifier with optional prefix."""
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}{timestamp}{random_str}"

def sanitize_input(data: Union[str, Dict, List]) -> Union[str, Dict, List]:
    """Sanitize input data to prevent XSS and SQL injection."""
    if isinstance(data, str):
        return re.sub(r'[<>"\']', '', data)
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    return data

def format_response(data: Any, message: str = 'Success', status_code: int = 200) -> Dict:
    """Format API response in a consistent structure."""
    return {
        'status': 'success' if 200 <= status_code < 300 else 'error',
        'message': message,
        'data': data,
        'timestamp': datetime.utcnow().isoformat()
    }

def paginate_query(query, page: int = 1, per_page: int = 10) -> Dict:
    """Paginate SQLAlchemy query results."""
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        'items': paginated.items,
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': paginated.page,
        'has_next': paginated.has_next,
        'has_prev': paginated.has_prev
    }

def cache_key_generator(*args, **kwargs) -> str:
    """Generate cache key from function arguments."""
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
    return ":".join(key_parts)

def validate_date_format(date_str: str, format: str = '%Y-%m-%d') -> bool:
    """Validate date string format."""
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False

def format_date(date: Union[str, datetime], format: str = '%Y-%m-%d') -> str:
    """Format date to specified format."""
    if isinstance(date, str):
        date = datetime.strptime(date, format)
    return date.strftime(format) 