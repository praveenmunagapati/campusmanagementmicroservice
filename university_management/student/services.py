from .base_services import BaseService
from .models import *
from datetime import datetime
from typing import List, Dict, Any, Optional
from . import db, cache
from .schemas import (
    StudentSchema, StudentProfileSchema, StudentAcademicSchema,
    StudentFinancialSchema, StudentDocumentSchema, StudentEnrollmentSchema,
    StudentAttendanceSchema, StudentGradeSchema, StudentAdvisingSchema,
    StudentServiceSchema, StudentComplaintSchema, StudentFeedbackSchema,
    StudentSurveySchema, StudentLocationSchema, StudentContactSchema,
    StudentEmergencySchema
)
from .exceptions import (
    ValidationError, NotFoundError, UnauthorizedError,
    ForbiddenError, ConflictError
)
from .utils import format_response, paginate_query


class StudentService(BaseService):
    """Service for Student operations."""
    
    def __init__(self):
        super().__init__(Student)
    
    # Add service-specific methods here
    pass

class StudentProfileService(BaseService):
    """Service for StudentProfile operations."""
    
    def __init__(self):
        super().__init__(StudentProfile)
    
    # Add service-specific methods here
    pass

class StudentAcademicService(BaseService):
    """Service for StudentAcademic operations."""
    
    def __init__(self):
        super().__init__(StudentAcademic)
    
    # Add service-specific methods here
    pass

class StudentFinancialService(BaseService):
    """Service for StudentFinancial operations."""
    
    def __init__(self):
        super().__init__(StudentFinancial)
    
    # Add service-specific methods here
    pass

class StudentDocumentService(BaseService):
    """Service for StudentDocument operations."""
    
    def __init__(self):
        super().__init__(StudentDocument)
    
    # Add service-specific methods here
    pass

class StudentEnrollmentService(BaseService):
    """Service for StudentEnrollment operations."""
    
    def __init__(self):
        super().__init__(StudentEnrollment)
    
    # Add service-specific methods here
    pass

class StudentAttendanceService(BaseService):
    """Service for StudentAttendance operations."""
    
    def __init__(self):
        super().__init__(StudentAttendance)
    
    # Add service-specific methods here
    pass

class StudentGradeService(BaseService):
    """Service for StudentGrade operations."""
    
    def __init__(self):
        super().__init__(StudentGrade)
    
    # Add service-specific methods here
    pass

class StudentAdvisingService(BaseService):
    """Service for StudentAdvising operations."""
    
    def __init__(self):
        super().__init__(StudentAdvising)
    
    # Add service-specific methods here
    pass

class StudentServiceService(BaseService):
    """Service for StudentService operations."""
    
    def __init__(self):
        super().__init__(StudentService)
    
    # Add service-specific methods here
    pass

class StudentComplaintService(BaseService):
    """Service for StudentComplaint operations."""
    
    def __init__(self):
        super().__init__(StudentComplaint)
    
    # Add service-specific methods here
    pass

class StudentFeedbackService(BaseService):
    """Service for StudentFeedback operations."""
    
    def __init__(self):
        super().__init__(StudentFeedback)
    
    # Add service-specific methods here
    pass

class StudentSurveyService(BaseService):
    """Service for StudentSurvey operations."""
    
    def __init__(self):
        super().__init__(StudentSurvey)
    
    # Add service-specific methods here
    pass

class StudentLocationService(BaseService):
    """Service for StudentLocation operations."""
    
    def __init__(self):
        super().__init__(StudentLocation)
    
    # Add service-specific methods here
    pass

class StudentContactService(BaseService):
    """Service for StudentContact operations."""
    
    def __init__(self):
        super().__init__(StudentContact)
    
    # Add service-specific methods here
    pass

class StudentEmergencyService(BaseService):
    """Service for StudentEmergency operations."""
    
    def __init__(self):
        super().__init__(StudentEmergency)
    
    # Add service-specific methods here
    pass

class StudentService:
    """Service for student operations."""
    
    def __init__(self):
        self.model_class = Student
        self.schema = StudentSchema()
    
    def get_by_id(self, id: int) -> Student:
        """Get student by ID."""
        student = self.model_class.get_by_id(id)
        if not student:
            raise NotFoundError(f"Student with ID {id} not found")
        return student
    
    def get_all(self, page: int = 1, per_page: int = 10) -> Dict:
        """Get all students with pagination."""
        query = self.model_class.query
        return paginate_query(query, page, per_page)
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> Student:
        """Create a new student."""
        try:
            # Validate data
            validated_data = self.schema.load(data)
            
            # Check if student_id already exists
            if self.model_class.query.filter_by(student_id=validated_data['student_id']).first():
                raise ConflictError(f"Student with ID {validated_data['student_id']} already exists")
            
            # Create student
            student = self.model_class(**validated_data)
            student.save()
            
            return student
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> Student:
        """Update a student."""
        student = self.get_by_id(id)
        
        try:
            # Validate data
            validated_data = self.schema.load(data, partial=True)
            
            # Update student
            for key, value in validated_data.items():
                setattr(student, key, value)
            
            student.save()
            return student
        except Exception as e:
            raise ValidationError(str(e))
    
    def delete(self, id: int, user_id: Optional[int] = None) -> None:
        """Delete a student."""
        student = self.get_by_id(id)
        student.delete()

class StudentProfileService:
    """Service for student profile operations."""
    
    def __init__(self):
        self.model_class = StudentProfile
        self.schema = StudentProfileSchema()
    
    def get_by_student_id(self, student_id: int) -> StudentProfile:
        """Get student profile by student ID."""
        profile = self.model_class.query.filter_by(student_id=student_id).first()
        if not profile:
            raise NotFoundError(f"Profile for student {student_id} not found")
        return profile
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentProfile:
        """Create a new student profile."""
        try:
            validated_data = self.schema.load(data)
            profile = self.model_class(**validated_data)
            profile.save()
            return profile
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, student_id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentProfile:
        """Update a student profile."""
        profile = self.get_by_student_id(student_id)
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(profile, key, value)
            profile.save()
            return profile
        except Exception as e:
            raise ValidationError(str(e))

class StudentAcademicService:
    """Service for student academic operations."""
    
    def __init__(self):
        self.model_class = StudentAcademic
        self.schema = StudentAcademicSchema()
    
    def get_by_student_id(self, student_id: int) -> StudentAcademic:
        """Get student academic record by student ID."""
        academic = self.model_class.query.filter_by(student_id=student_id).first()
        if not academic:
            raise NotFoundError(f"Academic record for student {student_id} not found")
        return academic
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentAcademic:
        """Create a new student academic record."""
        try:
            validated_data = self.schema.load(data)
            academic = self.model_class(**validated_data)
            academic.save()
            return academic
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, student_id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentAcademic:
        """Update a student academic record."""
        academic = self.get_by_student_id(student_id)
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(academic, key, value)
            academic.save()
            return academic
        except Exception as e:
            raise ValidationError(str(e))

class StudentFinancialService:
    """Service for student financial operations."""
    
    def __init__(self):
        self.model_class = StudentFinancial
        self.schema = StudentFinancialSchema()
    
    def get_by_student_id(self, student_id: int) -> StudentFinancial:
        """Get student financial record by student ID."""
        financial = self.model_class.query.filter_by(student_id=student_id).first()
        if not financial:
            raise NotFoundError(f"Financial record for student {student_id} not found")
        return financial
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentFinancial:
        """Create a new student financial record."""
        try:
            validated_data = self.schema.load(data)
            financial = self.model_class(**validated_data)
            financial.save()
            return financial
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, student_id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentFinancial:
        """Update a student financial record."""
        financial = self.get_by_student_id(student_id)
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(financial, key, value)
            financial.save()
            return financial
        except Exception as e:
            raise ValidationError(str(e))

class StudentDocumentService:
    """Service for student document operations."""
    
    def __init__(self):
        self.model_class = StudentDocument
        self.schema = StudentDocumentSchema()
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student documents by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentDocument:
        """Create a new student document."""
        try:
            validated_data = self.schema.load(data)
            document = self.model_class(**validated_data)
            document.save()
            return document
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentDocument:
        """Update a student document."""
        document = self.model_class.get_by_id(id)
        if not document:
            raise NotFoundError(f"Document with ID {id} not found")
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(document, key, value)
            document.save()
            return document
        except Exception as e:
            raise ValidationError(str(e))
    
    def delete(self, id: int, user_id: Optional[int] = None) -> None:
        """Delete a student document."""
        document = self.model_class.get_by_id(id)
        if not document:
            raise NotFoundError(f"Document with ID {id} not found")
        document.delete()

class StudentEnrollmentService:
    """Service for student enrollment operations."""
    
    def __init__(self):
        self.model_class = StudentEnrollment
        self.schema = StudentEnrollmentSchema()
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student enrollments by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentEnrollment:
        """Create a new student enrollment."""
        try:
            validated_data = self.schema.load(data)
            enrollment = self.model_class(**validated_data)
            enrollment.save()
            return enrollment
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentEnrollment:
        """Update a student enrollment."""
        enrollment = self.model_class.get_by_id(id)
        if not enrollment:
            raise NotFoundError(f"Enrollment with ID {id} not found")
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(enrollment, key, value)
            enrollment.save()
            return enrollment
        except Exception as e:
            raise ValidationError(str(e))
    
    def delete(self, id: int, user_id: Optional[int] = None) -> None:
        """Delete a student enrollment."""
        enrollment = self.model_class.get_by_id(id)
        if not enrollment:
            raise NotFoundError(f"Enrollment with ID {id} not found")
        enrollment.delete()

class StudentAttendanceService:
    """Service for student attendance operations."""
    
    def __init__(self):
        self.model_class = StudentAttendance
        self.schema = StudentAttendanceSchema()
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student attendance records by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentAttendance:
        """Create a new student attendance record."""
        try:
            validated_data = self.schema.load(data)
            attendance = self.model_class(**validated_data)
            attendance.save()
            return attendance
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentAttendance:
        """Update a student attendance record."""
        attendance = self.model_class.get_by_id(id)
        if not attendance:
            raise NotFoundError(f"Attendance record with ID {id} not found")
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(attendance, key, value)
            attendance.save()
            return attendance
        except Exception as e:
            raise ValidationError(str(e))

class StudentGradeService:
    """Service for student grade operations."""
    
    def __init__(self):
        self.model_class = StudentGrade
        self.schema = StudentGradeSchema()
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student grades by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentGrade:
        """Create a new student grade."""
        try:
            validated_data = self.schema.load(data)
            grade = self.model_class(**validated_data)
            grade.save()
            return grade
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentGrade:
        """Update a student grade."""
        grade = self.model_class.get_by_id(id)
        if not grade:
            raise NotFoundError(f"Grade with ID {id} not found")
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(grade, key, value)
            grade.save()
            return grade
        except Exception as e:
            raise ValidationError(str(e))

class StudentAdvisingService:
    """Service for student advising operations."""
    
    def __init__(self):
        self.model_class = StudentAdvising
        self.schema = StudentAdvisingSchema()
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student advising records by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentAdvising:
        """Create a new student advising record."""
        try:
            validated_data = self.schema.load(data)
            advising = self.model_class(**validated_data)
            advising.save()
            return advising
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentAdvising:
        """Update a student advising record."""
        advising = self.model_class.get_by_id(id)
        if not advising:
            raise NotFoundError(f"Advising record with ID {id} not found")
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(advising, key, value)
            advising.save()
            return advising
        except Exception as e:
            raise ValidationError(str(e))

class StudentServiceService:
    """Service for student service operations."""
    
    def __init__(self):
        self.model_class = StudentService
        self.schema = StudentServiceSchema()
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student services by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentService:
        """Create a new student service record."""
        try:
            validated_data = self.schema.load(data)
            service = self.model_class(**validated_data)
            service.save()
            return service
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentService:
        """Update a student service record."""
        service = self.model_class.get_by_id(id)
        if not service:
            raise NotFoundError(f"Service record with ID {id} not found")
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(service, key, value)
            service.save()
            return service
        except Exception as e:
            raise ValidationError(str(e))

class StudentComplaintService:
    """Service for student complaint operations."""
    
    def __init__(self):
        self.model_class = StudentComplaint
        self.schema = StudentComplaintSchema()
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student complaints by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentComplaint:
        """Create a new student complaint."""
        try:
            validated_data = self.schema.load(data)
            complaint = self.model_class(**validated_data)
            complaint.save()
            return complaint
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentComplaint:
        """Update a student complaint."""
        complaint = self.model_class.get_by_id(id)
        if not complaint:
            raise NotFoundError(f"Complaint with ID {id} not found")
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(complaint, key, value)
            complaint.save()
            return complaint
        except Exception as e:
            raise ValidationError(str(e))

class StudentFeedbackService:
    """Service for student feedback operations."""
    
    def __init__(self):
        self.model_class = StudentFeedback
        self.schema = StudentFeedbackSchema()
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student feedback by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentFeedback:
        """Create a new student feedback."""
        try:
            validated_data = self.schema.load(data)
            feedback = self.model_class(**validated_data)
            feedback.save()
            return feedback
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentFeedback:
        """Update a student feedback."""
        feedback = self.model_class.get_by_id(id)
        if not feedback:
            raise NotFoundError(f"Feedback with ID {id} not found")
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(feedback, key, value)
            feedback.save()
            return feedback
        except Exception as e:
            raise ValidationError(str(e))

class StudentSurveyService:
    """Service for student survey operations."""
    
    def __init__(self):
        self.model_class = StudentSurvey
        self.schema = StudentSurveySchema()
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student surveys by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentSurvey:
        """Create a new student survey response."""
        try:
            validated_data = self.schema.load(data)
            survey = self.model_class(**validated_data)
            survey.save()
            return survey
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentSurvey:
        """Update a student survey response."""
        survey = self.model_class.get_by_id(id)
        if not survey:
            raise NotFoundError(f"Survey response with ID {id} not found")
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(survey, key, value)
            survey.save()
            return survey
        except Exception as e:
            raise ValidationError(str(e))

class StudentLocationService:
    """Service for student location operations."""
    
    def __init__(self):
        self.model_class = StudentLocation
        self.schema = StudentLocationSchema()
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student locations by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentLocation:
        """Create a new student location record."""
        try:
            validated_data = self.schema.load(data)
            location = self.model_class(**validated_data)
            location.save()
            return location
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentLocation:
        """Update a student location record."""
        location = self.model_class.get_by_id(id)
        if not location:
            raise NotFoundError(f"Location record with ID {id} not found")
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(location, key, value)
            location.save()
            return location
        except Exception as e:
            raise ValidationError(str(e))

class StudentContactService:
    """Service for student contact operations."""
    
    def __init__(self):
        self.model_class = StudentContact
        self.schema = StudentContactSchema()
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student contacts by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentContact:
        """Create a new student contact."""
        try:
            validated_data = self.schema.load(data)
            contact = self.model_class(**validated_data)
            contact.save()
            return contact
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentContact:
        """Update a student contact."""
        contact = self.model_class.get_by_id(id)
        if not contact:
            raise NotFoundError(f"Contact with ID {id} not found")
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(contact, key, value)
            contact.save()
            return contact
        except Exception as e:
            raise ValidationError(str(e))
    
    def delete(self, id: int, user_id: Optional[int] = None) -> None:
        """Delete a student contact."""
        contact = self.model_class.get_by_id(id)
        if not contact:
            raise NotFoundError(f"Contact with ID {id} not found")
        contact.delete()

class StudentEmergencyService:
    """Service for student emergency contact operations."""
    
    def __init__(self):
        self.model_class = StudentEmergency
        self.schema = StudentEmergencySchema()
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student emergency contacts by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentEmergency:
        """Create a new student emergency contact."""
        try:
            validated_data = self.schema.load(data)
            emergency = self.model_class(**validated_data)
            emergency.save()
            return emergency
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> StudentEmergency:
        """Update a student emergency contact."""
        emergency = self.model_class.get_by_id(id)
        if not emergency:
            raise NotFoundError(f"Emergency contact with ID {id} not found")
        
        try:
            validated_data = self.schema.load(data, partial=True)
            for key, value in validated_data.items():
                setattr(emergency, key, value)
            emergency.save()
            return emergency
        except Exception as e:
            raise ValidationError(str(e))
    
    def delete(self, id: int, user_id: Optional[int] = None) -> None:
        """Delete a student emergency contact."""
        emergency = self.model_class.get_by_id(id)
        if not emergency:
            raise NotFoundError(f"Emergency contact with ID {id} not found")
        emergency.delete()
