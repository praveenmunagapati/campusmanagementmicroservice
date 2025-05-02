class ServiceException(Exception):
    """Base exception for all service-specific exceptions."""
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ValidationError(ServiceException):
    """Exception raised when validation fails."""
    def __init__(self, message, errors=None):
        super().__init__(message, status_code=400)
        self.errors = errors or {}

class NotFoundError(ServiceException):
    """Exception raised when a resource is not found."""
    def __init__(self, message="Resource not found"):
        super().__init__(message, status_code=404)

class UnauthorizedError(ServiceException):
    """Exception raised when authentication fails."""
    def __init__(self, message="Unauthorized"):
        super().__init__(message, status_code=401)

class ForbiddenError(ServiceException):
    """Exception raised when access is forbidden."""
    def __init__(self, message="Forbidden"):
        super().__init__(message, status_code=403)

class ConflictError(ServiceException):
    """Exception raised when there is a conflict with existing data."""
    def __init__(self, message="Conflict with existing data"):
        super().__init__(message, status_code=409)

class DatabaseError(ServiceException):
    """Exception raised when there is a database error."""
    def __init__(self, message="Database error occurred"):
        super().__init__(message, status_code=500)

class ExternalServiceError(ServiceException):
    """Exception raised when an external service call fails."""
    def __init__(self, message="External service error"):
        super().__init__(message, status_code=502)

class RateLimitError(ServiceException):
    """Exception raised when rate limit is exceeded."""
    def __init__(self, message="Rate limit exceeded"):
        super().__init__(message, status_code=429)

class FileUploadError(ServiceException):
    """Exception raised when file upload fails."""
    def __init__(self, message="File upload failed"):
        super().__init__(message, status_code=400)

class ConfigurationError(ServiceException):
    """Exception raised when there is a configuration error."""
    def __init__(self, message="Configuration error"):
        super().__init__(message, status_code=500) 