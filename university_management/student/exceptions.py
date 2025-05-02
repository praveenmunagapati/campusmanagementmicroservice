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

class StudentNotFoundError(NotFoundError):
    """Exception raised when a student is not found."""
    def __init__(self, student_id):
        super().__init__(f"Student with ID {student_id} not found")

class StudentAlreadyExistsError(ConflictError):
    """Exception raised when a student already exists."""
    def __init__(self, student_id):
        super().__init__(f"Student with ID {student_id} already exists")

class InvalidStudentDataError(ValidationError):
    """Exception raised when student data is invalid."""
    def __init__(self, message, errors=None):
        super().__init__(f"Invalid student data: {message}", errors)

class StudentEnrollmentError(ServiceException):
    """Exception raised when there is an error with student enrollment."""
    def __init__(self, message):
        super().__init__(message, status_code=400)

class StudentAcademicError(ServiceException):
    """Exception raised when there is an error with student academic records."""
    def __init__(self, message):
        super().__init__(message, status_code=400)

class StudentFinancialError(ServiceException):
    """Exception raised when there is an error with student financial records."""
    def __init__(self, message):
        super().__init__(message, status_code=400)

class StudentProfileNotFoundError(ServiceException):
    """Raised when a student profile is not found"""
    def __init__(self, student_id):
        super().__init__(f"Profile for student {student_id} not found", 404)

class StudentAcademicNotFoundError(ServiceException):
    """Raised when student academic records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Academic records for student {student_id} not found", 404)

class StudentFinancialNotFoundError(ServiceException):
    """Raised when student financial records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Financial records for student {student_id} not found", 404)

class StudentDocumentNotFoundError(ServiceException):
    """Raised when a student document is not found"""
    def __init__(self, document_id):
        super().__init__(f"Document with ID {document_id} not found", 404)

class StudentEnrollmentNotFoundError(ServiceException):
    """Raised when student enrollment records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Enrollment records for student {student_id} not found", 404)

class StudentAttendanceNotFoundError(ServiceException):
    """Raised when student attendance records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Attendance records for student {student_id} not found", 404)

class StudentGradeNotFoundError(ServiceException):
    """Raised when student grades are not found"""
    def __init__(self, student_id):
        super().__init__(f"Grades for student {student_id} not found", 404)

class StudentAdvisingNotFoundError(ServiceException):
    """Raised when student advising records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Advising records for student {student_id} not found", 404)

class StudentServiceNotFoundError(ServiceException):
    """Raised when student service records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Service records for student {student_id} not found", 404)

class StudentComplaintNotFoundError(ServiceException):
    """Raised when a student complaint is not found"""
    def __init__(self, complaint_id):
        super().__init__(f"Complaint with ID {complaint_id} not found", 404)

class StudentFeedbackNotFoundError(ServiceException):
    """Raised when student feedback is not found"""
    def __init__(self, student_id):
        super().__init__(f"Feedback for student {student_id} not found", 404)

class StudentSurveyNotFoundError(ServiceException):
    """Raised when a student survey is not found"""
    def __init__(self, survey_id):
        super().__init__(f"Survey with ID {survey_id} not found", 404)

class StudentLocationNotFoundError(ServiceException):
    """Raised when student location records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Location records for student {student_id} not found", 404)

class StudentContactNotFoundError(ServiceException):
    """Raised when student contact records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Contact records for student {student_id} not found", 404)

class StudentEmergencyNotFoundError(ServiceException):
    """Raised when student emergency records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Emergency records for student {student_id} not found", 404)

class StudentDuplicateError(ServiceException):
    """Raised when attempting to create a duplicate student record"""
    def __init__(self, field, value):
        super().__init__(f"Student with {field} '{value}' already exists", 409)

class StudentPermissionError(ServiceException):
    """Raised when user doesn't have permission to perform an action"""
    def __init__(self, action):
        super().__init__(f"Permission denied for {action}", 403)

class StudentServiceError(ServiceException):
    """Raised when a service operation fails"""
    def __init__(self, service, message):
        super().__init__(f"{service} service error: {message}", 500) 