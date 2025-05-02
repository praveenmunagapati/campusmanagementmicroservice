class StudentException(Exception):
    """Base exception for student microservice"""
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class StudentNotFoundError(StudentException):
    """Raised when a student is not found"""
    def __init__(self, student_id):
        super().__init__(f"Student with ID {student_id} not found", 404)

class StudentProfileNotFoundError(StudentException):
    """Raised when a student profile is not found"""
    def __init__(self, student_id):
        super().__init__(f"Profile for student {student_id} not found", 404)

class StudentAcademicNotFoundError(StudentException):
    """Raised when student academic records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Academic records for student {student_id} not found", 404)

class StudentFinancialNotFoundError(StudentException):
    """Raised when student financial records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Financial records for student {student_id} not found", 404)

class StudentDocumentNotFoundError(StudentException):
    """Raised when a student document is not found"""
    def __init__(self, document_id):
        super().__init__(f"Document with ID {document_id} not found", 404)

class StudentEnrollmentNotFoundError(StudentException):
    """Raised when student enrollment records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Enrollment records for student {student_id} not found", 404)

class StudentAttendanceNotFoundError(StudentException):
    """Raised when student attendance records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Attendance records for student {student_id} not found", 404)

class StudentGradeNotFoundError(StudentException):
    """Raised when student grades are not found"""
    def __init__(self, student_id):
        super().__init__(f"Grades for student {student_id} not found", 404)

class StudentAdvisingNotFoundError(StudentException):
    """Raised when student advising records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Advising records for student {student_id} not found", 404)

class StudentServiceNotFoundError(StudentException):
    """Raised when student service records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Service records for student {student_id} not found", 404)

class StudentComplaintNotFoundError(StudentException):
    """Raised when a student complaint is not found"""
    def __init__(self, complaint_id):
        super().__init__(f"Complaint with ID {complaint_id} not found", 404)

class StudentFeedbackNotFoundError(StudentException):
    """Raised when student feedback is not found"""
    def __init__(self, student_id):
        super().__init__(f"Feedback for student {student_id} not found", 404)

class StudentSurveyNotFoundError(StudentException):
    """Raised when a student survey is not found"""
    def __init__(self, survey_id):
        super().__init__(f"Survey with ID {survey_id} not found", 404)

class StudentLocationNotFoundError(StudentException):
    """Raised when student location records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Location records for student {student_id} not found", 404)

class StudentContactNotFoundError(StudentException):
    """Raised when student contact records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Contact records for student {student_id} not found", 404)

class StudentEmergencyNotFoundError(StudentException):
    """Raised when student emergency records are not found"""
    def __init__(self, student_id):
        super().__init__(f"Emergency records for student {student_id} not found", 404)

class StudentValidationError(StudentException):
    """Raised when student data validation fails"""
    def __init__(self, message):
        super().__init__(f"Validation error: {message}", 400)

class StudentDuplicateError(StudentException):
    """Raised when attempting to create a duplicate student record"""
    def __init__(self, field, value):
        super().__init__(f"Student with {field} '{value}' already exists", 409)

class StudentPermissionError(StudentException):
    """Raised when user doesn't have permission to perform an action"""
    def __init__(self, action):
        super().__init__(f"Permission denied for {action}", 403)

class StudentServiceError(StudentException):
    """Raised when a service operation fails"""
    def __init__(self, service, message):
        super().__init__(f"{service} service error: {message}", 500) 