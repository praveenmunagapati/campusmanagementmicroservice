from app import db
from datetime import datetime

class Accommodation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # dorm, apartment, etc.
    capacity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    amenities = db.Column(db.JSON)  # List of amenities
    monthly_rent = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='available')  # available, full, maintenance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'capacity': self.capacity,
            'location': self.location,
            'description': self.description,
            'amenities': self.amenities,
            'monthly_rent': self.monthly_rent,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accommodation_id = db.Column(db.Integer, db.ForeignKey('accommodation.id'), nullable=False)
    room_number = db.Column(db.String(20), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)  # single, double, suite
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='available')  # available, occupied, maintenance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    accommodation = db.relationship('Accommodation', backref=db.backref('rooms', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'accommodation_id': self.accommodation_id,
            'room_number': self.room_number,
            'room_type': self.room_type,
            'capacity': self.capacity,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class RoomAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    room = db.relationship('Room', backref=db.backref('assignments', lazy=True))
    student = db.relationship('Student', backref=db.backref('room_assignments', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'student_id': self.student_id,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class MaintenanceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    request_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    room = db.relationship('Room', backref=db.backref('maintenance_requests', lazy=True))
    student = db.relationship('Student', backref=db.backref('maintenance_requests', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'student_id': self.student_id,
            'request_type': self.request_type,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 