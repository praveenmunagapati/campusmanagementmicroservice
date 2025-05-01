from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ExchangeProgram(db.Model):
    __tablename__ = 'exchange_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    partner_institution = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    requirements = db.Column(db.Text)
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'partner_institution': self.partner_institution,
            'country': self.country,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'capacity': self.capacity,
            'requirements': self.requirements,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class PartnerInstitution(db.Model):
    __tablename__ = 'partner_institutions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100))
    website = db.Column(db.String(255))
    contact_name = db.Column(db.String(100))
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(50))
    agreement_start_date = db.Column(db.DateTime)
    agreement_end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ExchangeApplication(db.Model):
    __tablename__ = 'exchange_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('exchange_programs.id'), nullable=False)
    application_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='pending')
    documents = db.Column(db.Text)  # JSON string of document paths
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'program_id': self.program_id,
            'application_date': self.application_date.isoformat(),
            'status': self.status,
            'documents': self.documents,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class VisaApplication(db.Model):
    __tablename__ = 'visa_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    visa_type = db.Column(db.String(50), nullable=False)  # student, work, tourist
    country = db.Column(db.String(100), nullable=False)
    application_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    passport_number = db.Column(db.String(50))
    passport_expiry = db.Column(db.DateTime)
    visa_expiry = db.Column(db.DateTime)
    documents = db.Column(db.Text)  # JSON string of submitted documents
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('visa_applications', lazy=True))

class InternationalStudent(db.Model):
    __tablename__ = 'international_students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    passport_number = db.Column(db.String(50), unique=True, nullable=False)
    visa_type = db.Column(db.String(50), nullable=False)
    visa_expiry_date = db.Column(db.Date, nullable=False)
    country_of_origin = db.Column(db.String(100), nullable=False)
    language_proficiency = db.Column(db.String(50))
    arrival_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'passport_number': self.passport_number,
            'visa_type': self.visa_type,
            'visa_expiry_date': self.visa_expiry_date.isoformat(),
            'country_of_origin': self.country_of_origin,
            'language_proficiency': self.language_proficiency,
            'arrival_date': self.arrival_date.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class LanguageProficiency(db.Model):
    __tablename__ = 'language_proficiencies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    proficiency_level = db.Column(db.String(20), nullable=False)  # A1, A2, B1, B2, C1, C2
    test_type = db.Column(db.String(50))  # TOEFL, IELTS, etc.
    score = db.Column(db.Float)
    test_date = db.Column(db.DateTime)
    certificate_path = db.Column(db.String(255))  # file path
    status = db.Column(db.String(20), default='active')  # active, expired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('language_proficiencies', lazy=True))

class CulturalEvent(db.Model):
    __tablename__ = 'cultural_events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50), nullable=False)  # workshop, festival, orientation
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    location = db.Column(db.String(200))
    capacity = db.Column(db.Integer)
    target_audience = db.Column(db.String(100))  # international, all students
    status = db.Column(db.String(20), default='planned')  # planned, ongoing, completed, cancelled
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('created_cultural_events', lazy=True))

class EventRegistration(db.Model):
    __tablename__ = 'cultural_event_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('cultural_events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='registered')  # registered, attended, cancelled
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    event = db.relationship('CulturalEvent', backref=db.backref('registrations', lazy=True))
    user = db.relationship('User', backref=db.backref('cultural_event_registrations', lazy=True))

class InternationalEvent(db.Model):
    __tablename__ = 'international_events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    target_audience = db.Column(db.String(100))
    registration_link = db.Column(db.String(200))
    status = db.Column(db.String(50), default='upcoming')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'event_date': self.event_date.isoformat(),
            'location': self.location,
            'target_audience': self.target_audience,
            'registration_link': self.registration_link,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 