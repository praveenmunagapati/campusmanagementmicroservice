import os
from datetime import timedelta

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('STUDENT_DATABASE_URI', 'sqlite:///student.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'student-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # File upload configuration
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads/student')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}

    # Pagination configuration
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100

    # Cache configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes

    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Security configuration
    PASSWORD_SALT = os.getenv('PASSWORD_SALT', 'student-salt')
    PASSWORD_HASH_ALGORITHM = 'sha256'
    PASSWORD_ITERATIONS = 100000

    # API configuration
    API_VERSION = '1.0'
    API_PREFIX = '/api/v1/student' 