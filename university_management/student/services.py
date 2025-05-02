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
    
    def get_by_student_id(self, student_id: str) -> Student:
        """Get student by student ID."""
        student = self.model_class.query.filter_by(student_id=student_id).first()
        if not student:
            raise NotFoundError(f"Student with ID {student_id} not found")
        return student
    
    def get_by_email(self, email: str) -> Student:
        """Get student by email."""
        student = self.model_class.query.filter_by(email=email).first()
        if not student:
            raise NotFoundError(f"Student with email {email} not found")
        return student
    
    def get_by_program(self, program_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get students by program ID."""
        query = self.model_class.query.filter_by(program_id=program_id)
        return paginate_query(query, page, per_page)
    
    def get_by_department(self, department_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get students by department ID."""
        query = self.model_class.query.filter_by(department_id=department_id)
        return paginate_query(query, page, per_page)
    
    def get_by_advisor(self, advisor_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get students by advisor ID."""
        query = self.model_class.query.filter_by(advisor_id=advisor_id)
        return paginate_query(query, page, per_page)
    
    def get_by_status(self, status: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get students by status."""
        query = self.model_class.query.filter_by(status=status)
        return paginate_query(query, page, per_page)
    
    def search(self, query: str, page: int = 1, per_page: int = 10) -> Dict:
        """Search students by name, email, or student ID."""
        search_query = f"%{query}%"
        query = self.model_class.query.filter(
            (self.model_class.first_name.ilike(search_query)) |
            (self.model_class.last_name.ilike(search_query)) |
            (self.model_class.email.ilike(search_query)) |
            (self.model_class.student_id.ilike(search_query))
        )
        return paginate_query(query, page, per_page)


class StudentProfileService(BaseService):
    """Service for StudentProfile operations."""
    
    def __init__(self):
        super().__init__(StudentProfile)
    
    def get_by_student_id(self, student_id: int) -> StudentProfile:
        """Get student profile by student ID."""
        profile = self.model_class.query.filter_by(student_id=student_id).first()
        if not profile:
            raise NotFoundError(f"Profile for student {student_id} not found")
        return profile


class StudentAcademicService(BaseService):
    """Service for StudentAcademic operations."""
    
    def __init__(self):
        super().__init__(StudentAcademic)
    
    def get_by_student_id(self, student_id: int) -> StudentAcademic:
        """Get student academic record by student ID."""
        academic = self.model_class.query.filter_by(student_id=student_id).first()
        if not academic:
            raise NotFoundError(f"Academic record for student {student_id} not found")
        return academic
    
    def get_by_program(self, program_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get academic records by program ID."""
        query = self.model_class.query.filter_by(program_id=program_id)
        return paginate_query(query, page, per_page)
    
    def get_by_semester(self, semester: str, year: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get academic records by semester and year."""
        query = self.model_class.query.filter_by(semester=semester, year=year)
        return paginate_query(query, page, per_page)
    
    def get_by_status(self, status: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get academic records by status."""
        query = self.model_class.query.filter_by(academic_status=status)
        return paginate_query(query, page, per_page)


class StudentFinancialService(BaseService):
    """Service for StudentFinancial operations."""
    
    def __init__(self):
        super().__init__(StudentFinancial)
    
    def get_by_student_id(self, student_id: int) -> StudentFinancial:
        """Get student financial record by student ID."""
        financial = self.model_class.query.filter_by(student_id=student_id).first()
        if not financial:
            raise NotFoundError(f"Financial record for student {student_id} not found")
        return financial
    
    def get_by_status(self, status: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get financial records by payment status."""
        query = self.model_class.query.filter_by(payment_status=status)
        return paginate_query(query, page, per_page)
    
    def get_overdue_payments(self, page: int = 1, per_page: int = 10) -> Dict:
        """Get overdue payments."""
        today = datetime.utcnow().date()
        query = self.model_class.query.filter(
            self.model_class.payment_status == 'unpaid',
            self.model_class.payment_due_date < today
        )
        return paginate_query(query, page, per_page)


class StudentDocumentService(BaseService):
    """Service for StudentDocument operations."""
    
    def __init__(self):
        super().__init__(StudentDocument)
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student documents by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def get_by_type(self, document_type: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get documents by type."""
        query = self.model_class.query.filter_by(document_type=document_type)
        return paginate_query(query, page, per_page)
    
    def get_by_status(self, status: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get documents by status."""
        query = self.model_class.query.filter_by(status=status)
        return paginate_query(query, page, per_page)


class StudentEnrollmentService(BaseService):
    """Service for StudentEnrollment operations."""
    
    def __init__(self):
        super().__init__(StudentEnrollment)
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student enrollments by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def get_by_course(self, course_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get enrollments by course ID."""
        query = self.model_class.query.filter_by(course_id=course_id)
        return paginate_query(query, page, per_page)
    
    def get_by_section(self, section_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get enrollments by section ID."""
        query = self.model_class.query.filter_by(section_id=section_id)
        return paginate_query(query, page, per_page)
    
    def get_by_semester(self, semester: str, year: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get enrollments by semester and year."""
        query = self.model_class.query.filter_by(semester=semester, year=year)
        return paginate_query(query, page, per_page)
    
    def get_by_status(self, status: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get enrollments by status."""
        query = self.model_class.query.filter_by(status=status)
        return paginate_query(query, page, per_page)


class StudentAttendanceService(BaseService):
    """Service for StudentAttendance operations."""
    
    def __init__(self):
        super().__init__(StudentAttendance)
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student attendance records by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def get_by_course(self, course_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get attendance records by course ID."""
        query = self.model_class.query.filter_by(course_id=course_id)
        return paginate_query(query, page, per_page)
    
    def get_by_section(self, section_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get attendance records by section ID."""
        query = self.model_class.query.filter_by(section_id=section_id)
        return paginate_query(query, page, per_page)
    
    def get_by_date(self, date: datetime, page: int = 1, per_page: int = 10) -> Dict:
        """Get attendance records by date."""
        query = self.model_class.query.filter_by(date=date)
        return paginate_query(query, page, per_page)
    
    def get_by_status(self, status: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get attendance records by status."""
        query = self.model_class.query.filter_by(status=status)
        return paginate_query(query, page, per_page)


class StudentGradeService(BaseService):
    """Service for StudentGrade operations."""
    
    def __init__(self):
        super().__init__(StudentGrade)
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student grades by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def get_by_course(self, course_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get grades by course ID."""
        query = self.model_class.query.filter_by(course_id=course_id)
        return paginate_query(query, page, per_page)
    
    def get_by_section(self, section_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get grades by section ID."""
        query = self.model_class.query.filter_by(section_id=section_id)
        return paginate_query(query, page, per_page)
    
    def get_by_semester(self, semester: str, year: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get grades by semester and year."""
        query = self.model_class.query.filter_by(semester=semester, year=year)
        return paginate_query(query, page, per_page)
    
    def get_by_grade(self, grade: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get grades by grade value."""
        query = self.model_class.query.filter_by(grade=grade)
        return paginate_query(query, page, per_page)


class StudentAdvisingService(BaseService):
    """Service for StudentAdvising operations."""
    
    def __init__(self):
        super().__init__(StudentAdvising)
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student advising records by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def get_by_advisor(self, advisor_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get advising records by advisor ID."""
        query = self.model_class.query.filter_by(advisor_id=advisor_id)
        return paginate_query(query, page, per_page)
    
    def get_by_type(self, meeting_type: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get advising records by meeting type."""
        query = self.model_class.query.filter_by(meeting_type=meeting_type)
        return paginate_query(query, page, per_page)
    
    def get_by_status(self, status: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get advising records by status."""
        query = self.model_class.query.filter_by(status=status)
        return paginate_query(query, page, per_page)


class StudentServiceService(BaseService):
    """Service for StudentService operations."""
    
    def __init__(self):
        super().__init__(StudentService)
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student services by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def get_by_type(self, service_type: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get services by type."""
        query = self.model_class.query.filter_by(service_type=service_type)
        return paginate_query(query, page, per_page)
    
    def get_by_status(self, status: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get services by status."""
        query = self.model_class.query.filter_by(status=status)
        return paginate_query(query, page, per_page)


class StudentComplaintService(BaseService):
    """Service for StudentComplaint operations."""
    
    def __init__(self):
        super().__init__(StudentComplaint)
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student complaints by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def get_by_type(self, complaint_type: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get complaints by type."""
        query = self.model_class.query.filter_by(complaint_type=complaint_type)
        return paginate_query(query, page, per_page)
    
    def get_by_status(self, status: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get complaints by status."""
        query = self.model_class.query.filter_by(status=status)
        return paginate_query(query, page, per_page)
    
    def get_by_priority(self, priority: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get complaints by priority."""
        query = self.model_class.query.filter_by(priority=priority)
        return paginate_query(query, page, per_page)
    
    def get_by_assigned_to(self, assigned_to: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get complaints assigned to a specific faculty member."""
        query = self.model_class.query.filter_by(assigned_to=assigned_to)
        return paginate_query(query, page, per_page)


class StudentFeedbackService(BaseService):
    """Service for StudentFeedback operations."""
    
    def __init__(self):
        super().__init__(StudentFeedback)
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student feedback by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def get_by_type(self, feedback_type: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get feedback by type."""
        query = self.model_class.query.filter_by(feedback_type=feedback_type)
        return paginate_query(query, page, per_page)
    
    def get_by_target(self, target_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get feedback by target ID."""
        query = self.model_class.query.filter_by(target_id=target_id)
        return paginate_query(query, page, per_page)
    
    def get_by_status(self, status: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get feedback by status."""
        query = self.model_class.query.filter_by(status=status)
        return paginate_query(query, page, per_page)


class StudentSurveyService(BaseService):
    """Service for StudentSurvey operations."""
    
    def __init__(self):
        super().__init__(StudentSurvey)
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student surveys by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def get_by_survey(self, survey_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get survey responses by survey ID."""
        query = self.model_class.query.filter_by(survey_id=survey_id)
        return paginate_query(query, page, per_page)
    
    def get_by_status(self, status: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get survey responses by status."""
        query = self.model_class.query.filter_by(status=status)
        return paginate_query(query, page, per_page)


class StudentLocationService(BaseService):
    """Service for StudentLocation operations."""
    
    def __init__(self):
        super().__init__(StudentLocation)
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student locations by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def get_by_building(self, building: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get locations by building."""
        query = self.model_class.query.filter_by(building=building)
        return paginate_query(query, page, per_page)
    
    def get_by_status(self, status: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get locations by status."""
        query = self.model_class.query.filter_by(status=status)
        return paginate_query(query, page, per_page)


class StudentContactService(BaseService):
    """Service for StudentContact operations."""
    
    def __init__(self):
        super().__init__(StudentContact)
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student contacts by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def get_by_type(self, contact_type: str, page: int = 1, per_page: int = 10) -> Dict:
        """Get contacts by type."""
        query = self.model_class.query.filter_by(contact_type=contact_type)
        return paginate_query(query, page, per_page)
    
    def get_primary_contacts(self, page: int = 1, per_page: int = 10) -> Dict:
        """Get primary contacts."""
        query = self.model_class.query.filter_by(is_primary=True)
        return paginate_query(query, page, per_page)
    
    def get_verified_contacts(self, page: int = 1, per_page: int = 10) -> Dict:
        """Get verified contacts."""
        query = self.model_class.query.filter_by(is_verified=True)
        return paginate_query(query, page, per_page)


class StudentEmergencyService(BaseService):
    """Service for StudentEmergency operations."""
    
    def __init__(self):
        super().__init__(StudentEmergency)
    
    def get_by_student_id(self, student_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get student emergency contacts by student ID."""
        query = self.model_class.query.filter_by(student_id=student_id)
        return paginate_query(query, page, per_page)
    
    def get_primary_contacts(self, page: int = 1, per_page: int = 10) -> Dict:
        """Get primary emergency contacts."""
        query = self.model_class.query.filter_by(is_primary=True)
        return paginate_query(query, page, per_page)
