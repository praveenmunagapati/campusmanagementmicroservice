from . import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class HealthStaff(db.Model):
    __tablename__ = 'health_staff'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    staff_type = db.Column(db.String(50), nullable=False)  # doctor, nurse, etc.
    specialization = db.Column(db.String(100))
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    license_expiry = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    appointments = db.relationship('Appointment', backref='staff', lazy=True)
    prescriptions = db.relationship('Prescription', backref='prescribed_by', lazy=True)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('health_staff.id'), nullable=False)
    appointment_type = db.Column(db.String(50), nullable=False)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    medical_records = db.relationship('MedicalRecord', backref='appointment', lazy=True)

class MedicalRecord(db.Model):
    """Model for student medical records"""
    __tablename__ = 'medical_records'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blood_type = db.Column(db.String(10))
    allergies = db.Column(JSONB)  # List of allergies
    medications = db.Column(JSONB)  # Current medications
    conditions = db.Column(JSONB)  # Medical conditions
    emergency_contact = db.Column(JSONB)  # Emergency contact information
    insurance_info = db.Column(JSONB)  # Insurance details
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = db.Column(JSONB)  # For additional medical data

    # Relationships
    student = db.relationship('User', backref='medical_record')
    appointments = db.relationship('Appointment', backref='medical_record', lazy=True)

    def __repr__(self):
        return f'<MedicalRecord {self.id}>'

class Prescription(db.Model):
    """Model for medical prescriptions"""
    __tablename__ = 'prescriptions'

    id = db.Column(db.Integer, primary_key=True)
    medical_record_id = db.Column(db.Integer, db.ForeignKey('medical_records.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('health_staff.id'), nullable=False)
    medication = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    prescriber = db.relationship('HealthStaff', backref='prescriptions')

    def __repr__(self):
        return f'<Prescription {self.medication}>'

class HealthReport(db.Model):
    __tablename__ = 'health_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='draft')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HealthEquipment(db.Model):
    __tablename__ = 'health_equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    equipment_type = db.Column(db.String(50), nullable=False)
    serial_number = db.Column(db.String(50), unique=True, nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    last_maintenance = db.Column(db.DateTime)
    next_maintenance = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HealthInventory(db.Model):
    __tablename__ = 'health_inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    expiry_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ImmunizationRecord(db.Model):
    """Model for immunization records"""
    __tablename__ = 'immunization_records'

    id = db.Column(db.Integer, primary_key=True)
    medical_record_id = db.Column(db.Integer, db.ForeignKey('medical_records.id'), nullable=False)
    vaccine_name = db.Column(db.String(100), nullable=False)
    date_administered = db.Column(db.Date, nullable=False)
    administered_by = db.Column(db.String(200))
    next_due_date = db.Column(db.Date)
    batch_number = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    medical_record = db.relationship('MedicalRecord', backref='immunizations')

    def __repr__(self):
        return f'<ImmunizationRecord {self.vaccine_name}>'

class HealthAlert(db.Model):
    """Model for health alerts and notifications"""
    __tablename__ = 'health_alerts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    alert_type = db.Column(db.String(50))  # outbreak, advisory, reminder, etc.
    severity = db.Column(db.String(20))  # low, medium, high, critical
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    affected_groups = db.Column(JSONB)  # Groups affected by the alert
    actions_required = db.Column(JSONB)  # Required actions
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = db.relationship('User', backref='health_alerts')

    def __repr__(self):
        return f'<HealthAlert {self.title}>'

class HealthServiceStaff(db.Model):
    """Model for health service staff"""
    __tablename__ = 'health_service_staff'

    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # doctor, nurse, counselor, etc.
    specialization = db.Column(db.String(100))
    license_number = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    schedule = db.Column(JSONB)  # Staff schedule
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    staff = db.relationship('User', backref='health_service_staff')

    def __repr__(self):
        return f'<HealthServiceStaff {self.role}>' 