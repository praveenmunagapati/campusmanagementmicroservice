from datetime import datetime
from . import db
from .base_models import BaseModel


class Student(BaseModel):
    """Model for student information."""
    __tablename__ = 'students'
    
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    nationality = db.Column(db.String(50))
    status = db.Column(db.String(20), default='active')
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    advisor_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))

class StudentProfile(BaseModel):
    """Model for student profile information."""
    __tablename__ = 'student_profiles'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(20))
    blood_group = db.Column(db.String(5))
    medical_conditions = db.Column(db.Text)
    photo_url = db.Column(db.String(255))

class StudentAcademic(BaseModel):
    """Model for student academic information."""
    __tablename__ = 'student_academics'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
    semester = db.Column(db.String(20))
    year = db.Column(db.Integer)
    gpa = db.Column(db.Float)
    credits_earned = db.Column(db.Integer)
    credits_remaining = db.Column(db.Integer)
    academic_status = db.Column(db.String(20))
    graduation_date = db.Column(db.Date)
    honors = db.Column(db.String(100))

class StudentFinancial(BaseModel):
    """Model for student financial information."""
    __tablename__ = 'student_financials'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    tuition_fee = db.Column(db.Float)
    scholarship_amount = db.Column(db.Float)
    financial_aid_amount = db.Column(db.Float)
    payment_status = db.Column(db.String(20))
    payment_due_date = db.Column(db.Date)
    payment_history = db.Column(db.JSON)

class StudentDocument(BaseModel):
    """Model for student documents."""
    __tablename__ = 'student_documents'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    document_name = db.Column(db.String(255), nullable=False)
    document_url = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')
    verified_by = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    verification_date = db.Column(db.DateTime)

class StudentEnrollment(BaseModel):
    """Model for student course enrollment."""
    __tablename__ = 'student_enrollments'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('course_sections.id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')
    grade = db.Column(db.String(2))
    credits = db.Column(db.Integer)

class StudentAttendance(BaseModel):
    """Model for student attendance records."""
    __tablename__ = 'student_attendance'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('course_sections.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # present, absent, late
    reason = db.Column(db.String(255))
    verified_by = db.Column(db.Integer, db.ForeignKey('faculty.id'))

class StudentGrade(BaseModel):
    """Model for student grades."""
    __tablename__ = 'student_grades'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('course_sections.id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(2), nullable=False)
    grade_points = db.Column(db.Float)
    credits = db.Column(db.Integer)
    remarks = db.Column(db.Text)
    posted_by = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)

class StudentAdvising(BaseModel):
    """Model for student advising records."""
    __tablename__ = 'student_advising'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    advisor_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    meeting_date = db.Column(db.DateTime, nullable=False)
    meeting_type = db.Column(db.String(50))  # academic, career, personal
    notes = db.Column(db.Text)
    follow_up_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='scheduled')

class StudentService(BaseModel):
    """Model for student services."""
    __tablename__ = 'student_services'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)  # counseling, career, health
    service_date = db.Column(db.DateTime, nullable=False)
    provider = db.Column(db.String(100))
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    follow_up_date = db.Column(db.DateTime)

class StudentComplaint(BaseModel):
    """Model for student complaints."""
    __tablename__ = 'student_complaints'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    complaint_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')
    priority = db.Column(db.String(20), default='medium')
    assigned_to = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    resolution = db.Column(db.Text)
    resolution_date = db.Column(db.DateTime)

class StudentFeedback(BaseModel):
    """Model for student feedback."""
    __tablename__ = 'student_feedback'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    feedback_type = db.Column(db.String(50), nullable=False)  # course, faculty, service
    target_id = db.Column(db.Integer, nullable=False)  # course_id, faculty_id, service_id
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='submitted')

class StudentSurvey(BaseModel):
    """Model for student surveys."""
    __tablename__ = 'student_surveys'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    responses = db.Column(db.JSON, nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')

class StudentLocation(BaseModel):
    """Model for student location tracking."""
    __tablename__ = 'student_locations'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    building = db.Column(db.String(100))
    room = db.Column(db.String(50))
    check_in_time = db.Column(db.DateTime, default=datetime.utcnow)
    check_out_time = db.Column(db.DateTime)
    purpose = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')

class StudentContact(BaseModel):
    """Model for student contact information."""
    __tablename__ = 'student_contacts'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    contact_type = db.Column(db.String(50), nullable=False)  # phone, email, address
    value = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_date = db.Column(db.DateTime)

class StudentEmergency(BaseModel):
    """Model for student emergency contacts."""
    __tablename__ = 'student_emergency_contacts'
    
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))
    is_primary = db.Column(db.Boolean, default=False)
