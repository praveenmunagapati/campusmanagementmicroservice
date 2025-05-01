from datetime import datetime
from .. import db
from sqlalchemy.dialects.postgresql import JSONB

class Application(db.Model):
    """Model for student applications"""
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='submitted')  # submitted, under_review, accepted, rejected, waitlisted
    term = db.Column(db.String(20))  # e.g., Fall 2024
    application_type = db.Column(db.String(20))  # freshman, transfer, graduate
    priority = db.Column(db.String(20))  # regular, early_action, early_decision
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = db.Column(JSONB)  # For additional application data

    # Relationships
    applicant = db.relationship('User', backref='applications')
    program = db.relationship('Program', backref='applications')
    documents = db.relationship('ApplicationDocument', backref='application', lazy=True)
    decisions = db.relationship('AdmissionDecision', backref='application', lazy=True)

    def __repr__(self):
        return f'<Application {self.id}>'

class ApplicationDocument(db.Model):
    """Model for application documents"""
    __tablename__ = 'application_documents'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # transcript, recommendation, essay, etc.
    file_path = db.Column(db.String(500))
    file_type = db.Column(db.String(50))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, verified, rejected
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    verification_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    verifier = db.relationship('User', backref='verified_documents')

    def __repr__(self):
        return f'<ApplicationDocument {self.document_type}>'

class AdmissionDecision(db.Model):
    """Model for admission decisions"""
    __tablename__ = 'admission_decisions'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    decision = db.Column(db.String(20), nullable=False)  # accepted, rejected, waitlisted
    decision_date = db.Column(db.DateTime, default=datetime.utcnow)
    decided_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notes = db.Column(db.Text)
    scholarship_amount = db.Column(db.Float)
    deadline_to_accept = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    decision_maker = db.relationship('User', backref='made_decisions')

    def __repr__(self):
        return f'<AdmissionDecision {self.decision}>'

class Program(db.Model):
    """Model for academic programs"""
    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # e.g., CS-BS
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    degree_type = db.Column(db.String(50))  # bachelor, master, phd
    duration_years = db.Column(db.Integer)
    total_credits = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = db.Column(JSONB)  # For additional program data

    # Relationships
    department = db.relationship('Department', backref='programs')
    requirements = db.relationship('ProgramRequirement', backref='program', lazy=True)

    def __repr__(self):
        return f'<Program {self.code}>'

class ProgramRequirement(db.Model):
    """Model for program requirements"""
    __tablename__ = 'program_requirements'

    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    requirement_type = db.Column(db.String(50), nullable=False)  # gpa, test_score, prerequisite, etc.
    requirement_name = db.Column(db.String(100), nullable=False)
    minimum_value = db.Column(db.Float)
    maximum_value = db.Column(db.Float)
    description = db.Column(db.Text)
    is_mandatory = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ProgramRequirement {self.requirement_name}>'

class ApplicationFee(db.Model):
    """Model for application fees"""
    __tablename__ = 'application_fees'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    payment_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    application = db.relationship('Application', backref='fee')

    def __repr__(self):
        return f'<ApplicationFee {self.amount}>' 