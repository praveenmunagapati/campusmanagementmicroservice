from datetime import datetime
from .. import db
from sqlalchemy.dialects.postgresql import JSONB

class Course(db.Model):
    """Model for university courses"""
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # e.g., CS101
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    prerequisites = db.Column(JSONB)  # List of course codes
    corequisites = db.Column(JSONB)  # List of course codes
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = db.Column(JSONB)  # For additional course-specific data

    # Relationships
    offerings = db.relationship('CourseOffering', backref='course', lazy=True)
    department = db.relationship('Department', backref='courses')

    def __repr__(self):
        return f'<Course {self.code}>'

class CourseOffering(db.Model):
    """Model for course offerings (specific instances of courses)"""
    __tablename__ = 'course_offerings'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    section = db.Column(db.String(10))  # e.g., A, B, C
    capacity = db.Column(db.Integer)
    enrolled = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='open')  # open, closed, cancelled
    schedule = db.Column(JSONB)  # Class schedule details
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    enrollments = db.relationship('Enrollment', backref='offering', lazy=True)
    instructor = db.relationship('User', backref='taught_courses')
    semester = db.relationship('Semester', backref='offerings')

    def __repr__(self):
        return f'<CourseOffering {self.course.code}-{self.section}>'

class Enrollment(db.Model):
    """Model for student course enrollments"""
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    offering_id = db.Column(db.Integer, db.ForeignKey('course_offerings.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='enrolled')  # enrolled, dropped, withdrawn
    grade = db.Column(db.String(2))  # A, B, C, D, F, etc.
    grade_points = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = db.relationship('User', backref='enrollments')

    def __repr__(self):
        return f'<Enrollment {self.id}>'

class Department(db.Model):
    """Model for academic departments"""
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)  # e.g., CS, MATH
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    head_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    head = db.relationship('User', backref='department_head')

    def __repr__(self):
        return f'<Department {self.code}>'

class Semester(db.Model):
    """Model for academic semesters"""
    __tablename__ = 'semesters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # e.g., Fall 2024
    code = db.Column(db.String(10), unique=True, nullable=False)  # e.g., F2024
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    registration_start = db.Column(db.Date)
    registration_end = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Semester {self.name}>'

class CourseMaterial(db.Model):
    """Model for course materials"""
    __tablename__ = 'course_materials'

    id = db.Column(db.Integer, primary_key=True)
    offering_id = db.Column(db.Integer, db.ForeignKey('course_offerings.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    file_type = db.Column(db.String(50))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_public = db.Column(db.Boolean, default=True)
    metadata = db.Column(JSONB)  # For additional material-specific data

    # Relationships
    offering = db.relationship('CourseOffering', backref='materials')
    uploader = db.relationship('User', backref='uploaded_materials')

    def __repr__(self):
        return f'<CourseMaterial {self.title}>'

class Section(db.Model):
    __tablename__ = 'sections'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    section_number = db.Column(db.String(10), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    enrolled = db.Column(db.Integer, default=0)
    schedule = db.Column(db.Text)  # JSON string of class schedule
    location = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')  # active, cancelled, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    course = db.relationship('Course', backref=db.backref('sections', lazy=True))
    faculty = db.relationship('Faculty', backref=db.backref('sections', lazy=True))

class Prerequisite(db.Model):
    __tablename__ = 'prerequisites'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    prerequisite_course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    is_corequisite = db.Column(db.Boolean, default=False)
    minimum_grade = db.Column(db.String(2))  # Minimum grade required
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    course = db.relationship('Course', foreign_keys=[course_id], backref=db.backref('prerequisites', lazy=True))
    prerequisite_course = db.relationship('Course', foreign_keys=[prerequisite_course_id])

class Term(db.Model):
    __tablename__ = 'terms'
    
    id = db.Column(db.String(36), primary_key=True)
    term_code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    registration_start = db.Column(db.Date, nullable=False)
    registration_end = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'term_code': self.term_code,
            'name': self.name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'registration_start': self.registration_start.isoformat() if self.registration_start else None,
            'registration_end': self.registration_end.isoformat() if self.registration_end else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class CourseSchedule(db.Model):
    __tablename__ = 'course_schedules'
    
    id = db.Column(db.String(36), primary_key=True)
    section_id = db.Column(db.String(36), db.ForeignKey('sections.id'), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    room = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'section_id': self.section_id,
            'day_of_week': self.day_of_week,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'room': self.room,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 