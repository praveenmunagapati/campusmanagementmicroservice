from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum, Text, JSON
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base
import re
from .. import db

Base = declarative_base()

class Student(db.Model):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    student_id = Column(String(20), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    student_type = Column(Enum('undergraduate', 'graduate', 'phd', name='student_type'), nullable=False)
    program = Column(String(100), nullable=False)
    enrollment_date = Column(DateTime, nullable=False)
    status = Column(Enum('active', 'inactive', 'graduated', 'withdrawn', name='student_status'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship('StudentProfile', back_populates='student', uselist=False)
    academic_records = relationship('StudentAcademic', back_populates='student')
    financial_records = relationship('StudentFinancial', back_populates='student')
    documents = relationship('StudentDocument', back_populates='student')
    enrollments = relationship('StudentEnrollment', back_populates='student')
    attendance_records = relationship('StudentAttendance', back_populates='student')
    grades = relationship('StudentGrade', back_populates='student')
    advising_records = relationship('StudentAdvising', back_populates='student')
    services = relationship('StudentService', back_populates='student')
    complaints = relationship('StudentComplaint', back_populates='student')
    feedback = relationship('StudentFeedback', back_populates='student')
    surveys = relationship('StudentSurvey', back_populates='student')
    locations = relationship('StudentLocation', back_populates='student')
    contacts = relationship('StudentContact', back_populates='student')
    emergencies = relationship('StudentEmergency', back_populates='student')

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError('Invalid email format')
        return email

    @validates('phone')
    def validate_phone(self, key, phone):
        if not re.match(r'^\+?1?\d{9,15}$', phone):
            raise ValueError('Invalid phone number format')
        return phone

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'student_type': self.student_type,
            'program': self.program,
            'enrollment_date': self.enrollment_date.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    nationality = Column(String(50), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    gender = Column(Enum('male', 'female', 'other', name='gender'), nullable=False)
    address = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    zip_code = Column(String(20))
    country = Column(String(100), nullable=False)
    status = Column(Enum('active', 'inactive', name='profile_status'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='profile')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'nationality': self.nationality,
            'date_of_birth': self.date_of_birth.isoformat(),
            'gender': self.gender,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'country': self.country,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentAcademic(db.Model):
    __tablename__ = 'student_academic_records'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    program = Column(String(100), nullable=False)
    major = Column(String(100))
    minor = Column(String(100))
    start_date = Column(DateTime, nullable=False)
    expected_graduation = Column(DateTime)
    gpa = Column(Float)
    status = Column(Enum('active', 'completed', 'transferred', name='academic_status'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='academic_records')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'program': self.program,
            'major': self.major,
            'minor': self.minor,
            'start_date': self.start_date.isoformat(),
            'expected_graduation': self.expected_graduation.isoformat() if self.expected_graduation else None,
            'gpa': self.gpa,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentFinancial(db.Model):
    __tablename__ = 'student_financial_records'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    payment_type = Column(Enum('tuition', 'fees', 'housing', 'meal_plan', 'other', name='payment_type'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    status = Column(Enum('paid', 'pending', 'overdue', 'cancelled', name='payment_status'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='financial_records')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'payment_type': self.payment_type,
            'amount': self.amount,
            'payment_date': self.payment_date.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentDocument(db.Model):
    __tablename__ = 'student_documents'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    document_type = Column(Enum('transcript', 'certificate', 'id_card', 'other', name='document_type'), nullable=False)
    file_name = Column(String(200), nullable=False)
    file_path = Column(String(500), nullable=False)
    upload_date = Column(DateTime, nullable=False)
    status = Column(Enum('verified', 'pending', 'rejected', name='document_status'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='documents')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'document_type': self.document_type,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'upload_date': self.upload_date.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentEnrollment(db.Model):
    __tablename__ = 'student_enrollments'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course = Column(String(50), nullable=False)
    section = Column(String(10), nullable=False)
    semester = Column(String(20), nullable=False)
    enrollment_date = Column(DateTime, nullable=False)
    status = Column(Enum('enrolled', 'dropped', 'completed', 'withdrawn', name='enrollment_status'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='enrollments')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course': self.course,
            'section': self.section,
            'semester': self.semester,
            'enrollment_date': self.enrollment_date.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentAttendance(db.Model):
    __tablename__ = 'student_attendance'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course = Column(String(50), nullable=False)
    attendance_date = Column(DateTime, nullable=False)
    status = Column(Enum('present', 'absent', 'late', 'excused', name='attendance_status'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='attendance_records')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course': self.course,
            'attendance_date': self.attendance_date.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentGrade(db.Model):
    __tablename__ = 'student_grades'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course = Column(String(50), nullable=False)
    grade = Column(String(2), nullable=False)
    grade_points = Column(Float, nullable=False)
    grade_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='grades')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course': self.course,
            'grade': self.grade,
            'grade_points': self.grade_points,
            'grade_date': self.grade_date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentAdvising(db.Model):
    __tablename__ = 'student_advising'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    advisor_id = Column(String(20), nullable=False)
    advising_date = Column(DateTime, nullable=False)
    notes = Column(Text)
    status = Column(Enum('scheduled', 'completed', 'cancelled', name='advising_status'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='advising_records')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'advisor_id': self.advisor_id,
            'advising_date': self.advising_date.isoformat(),
            'notes': self.notes,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentService(db.Model):
    __tablename__ = 'student_services'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    service_type = Column(Enum('counseling', 'tutoring', 'career', 'health', 'other', name='service_type'), nullable=False)
    service_date = Column(DateTime, nullable=False)
    notes = Column(Text)
    status = Column(Enum('scheduled', 'completed', 'cancelled', name='service_status'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='services')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'service_type': self.service_type,
            'service_date': self.service_date.isoformat(),
            'notes': self.notes,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentComplaint(db.Model):
    __tablename__ = 'student_complaints'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    complaint_type = Column(Enum('academic', 'administrative', 'facility', 'other', name='complaint_type'), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum('pending', 'in_progress', 'resolved', 'rejected', name='complaint_status'), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='complaints')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'complaint_type': self.complaint_type,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'status': self.status,
            'updated_at': self.updated_at.isoformat()
        }

class StudentFeedback(db.Model):
    __tablename__ = 'student_feedback'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    feedback_type = Column(Enum('course', 'faculty', 'facility', 'service', 'other', name='feedback_type'), nullable=False)
    rating = Column(Integer, nullable=False)
    comments = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='feedback')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'feedback_type': self.feedback_type,
            'rating': self.rating,
            'comments': self.comments,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentSurvey(db.Model):
    __tablename__ = 'student_surveys'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    survey_type = Column(Enum('course_evaluation', 'faculty_evaluation', 'service_evaluation', 'other', name='survey_type'), nullable=False)
    responses = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='surveys')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'survey_type': self.survey_type,
            'responses': self.responses,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentLocation(db.Model):
    __tablename__ = 'student_locations'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    location_type = Column(Enum('residence', 'classroom', 'library', 'other', name='location_type'), nullable=False)
    building = Column(String(100), nullable=False)
    room = Column(String(20))
    status = Column(Enum('active', 'inactive', name='location_status'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='locations')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'location_type': self.location_type,
            'building': self.building,
            'room': self.room,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentContact(db.Model):
    __tablename__ = 'student_contacts'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    contact_type = Column(Enum('emergency', 'parent', 'guardian', 'other', name='contact_type'), nullable=False)
    name = Column(String(100), nullable=False)
    relationship = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='contacts')

    @validates('email')
    def validate_email(self, key, email):
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError('Invalid email format')
        return email

    @validates('phone')
    def validate_phone(self, key, phone):
        if not re.match(r'^\+?1?\d{9,15}$', phone):
            raise ValueError('Invalid phone number format')
        return phone

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'contact_type': self.contact_type,
            'name': self.name,
            'relationship': self.relationship,
            'phone': self.phone,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentEmergency(db.Model):
    __tablename__ = 'student_emergencies'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    emergency_type = Column(Enum('medical', 'security', 'other', name='emergency_type'), nullable=False)
    description = Column(Text, nullable=False)
    occurred_at = Column(DateTime, nullable=False)
    status = Column(Enum('active', 'resolved', name='emergency_status'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship('Student', back_populates='emergencies')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'emergency_type': self.emergency_type,
            'description': self.description,
            'occurred_at': self.occurred_at.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 