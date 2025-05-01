from datetime import datetime
from .. import db
from sqlalchemy.dialects.postgresql import JSONB

class ResidenceHall(db.Model):
    """Model for university residence halls"""
    __tablename__ = 'residence_halls'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    gender_type = db.Column(db.String(20))  # male, female, coed
    room_types = db.Column(JSONB)  # Available room types and counts
    amenities = db.Column(JSONB)  # List of amenities
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = db.Column(JSONB)  # Additional hall data

    # Relationships
    rooms = db.relationship('Room', backref='hall', lazy=True)
    staff = db.relationship('ResidenceStaff', backref='hall', lazy=True)

    def __repr__(self):
        return f'<ResidenceHall {self.name}>'

class Room(db.Model):
    """Model for residence hall rooms"""
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    hall_id = db.Column(db.Integer, db.ForeignKey('residence_halls.id'), nullable=False)
    room_number = db.Column(db.String(20), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)  # single, double, suite, etc.
    capacity = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    features = db.Column(JSONB)  # Room features
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    occupants = db.relationship('RoomOccupancy', backref='room', lazy=True)
    maintenance_requests = db.relationship('MaintenanceRequest', backref='room', lazy=True)
    inspections = db.relationship('RoomInspection', backref='room', lazy=True)

    def __repr__(self):
        return f'<Room {self.room_number}>'

class RoomOccupancy(db.Model):
    """Model for room occupancy"""
    __tablename__ = 'room_occupancy'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = db.relationship('User', backref='room_occupancy')

    def __repr__(self):
        return f'<RoomOccupancy {self.id}>'

class ResidenceStaff(db.Model):
    """Model for residence hall staff"""
    __tablename__ = 'residence_staff'

    id = db.Column(db.Integer, primary_key=True)
    hall_id = db.Column(db.Integer, db.ForeignKey('residence_halls.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # RA, RD, maintenance, etc.
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    staff = db.relationship('User', backref='residence_staff')

    def __repr__(self):
        return f'<ResidenceStaff {self.role}>'

class MaintenanceRequest(db.Model):
    """Model for maintenance requests"""
    __tablename__ = 'maintenance_requests'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    request_type = db.Column(db.String(50), nullable=False)  # plumbing, electrical, etc.
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, emergency
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    completion_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = db.relationship('User', foreign_keys=[student_id], backref='maintenance_requests')
    assigned_staff = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_maintenance')

    def __repr__(self):
        return f'<MaintenanceRequest {self.id}>'

class RoomInspection(db.Model):
    """Model for room inspections"""
    __tablename__ = 'room_inspections'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    inspector_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    inspection_date = db.Column(db.DateTime, nullable=False)
    inspection_type = db.Column(db.String(50))  # regular, move_in, move_out, etc.
    findings = db.Column(JSONB)  # Inspection findings
    status = db.Column(db.String(20), default='pending')  # pending, completed, follow_up
    follow_up_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    inspector = db.relationship('User', backref='room_inspections')

    def __repr__(self):
        return f'<RoomInspection {self.id}>'

class HousingApplication(db.Model):
    """Model for housing applications"""
    __tablename__ = 'housing_applications'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    preferred_hall = db.Column(db.Integer, db.ForeignKey('residence_halls.id'))
    preferred_room_type = db.Column(db.String(50))
    roommate_preferences = db.Column(JSONB)  # Roommate preferences
    special_needs = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = db.relationship('User', backref='housing_applications')
    hall = db.relationship('ResidenceHall', backref='applications')

    def __repr__(self):
        return f'<HousingApplication {self.id}>' 