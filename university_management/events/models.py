from datetime import datetime
from .. import db
from sqlalchemy.dialects.postgresql import JSONB

class Event(db.Model):
    """Model for university events"""
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    capacity = db.Column(db.Integer)
    category = db.Column(db.String(50))  # academic, social, sports, etc.
    status = db.Column(db.String(20), default='scheduled')  # scheduled, ongoing, completed, cancelled
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = db.Column(JSONB)  # For additional event-specific data

    # Relationships
    registrations = db.relationship('EventRegistration', backref='event', lazy=True)
    organizer = db.relationship('User', backref='organized_events')

    def __repr__(self):
        return f'<Event {self.title}>'

class EventRegistration(db.Model):
    """Model for event registrations"""
    __tablename__ = 'event_registrations'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='registered')  # registered, attended, cancelled
    additional_info = db.Column(JSONB)  # For custom registration fields

    # Relationships
    user = db.relationship('User', backref='event_registrations')

    def __repr__(self):
        return f'<EventRegistration {self.id}>'

class EventCategory(db.Model):
    """Model for event categories"""
    __tablename__ = 'event_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    color_code = db.Column(db.String(7))  # For UI display
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<EventCategory {self.name}>'

class EventFeedback(db.Model):
    """Model for event feedback"""
    __tablename__ = 'event_feedback'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer)  # 1-5 scale
    comment = db.Column(db.Text)
    feedback_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_anonymous = db.Column(db.Boolean, default=False)

    # Relationships
    event = db.relationship('Event', backref='feedback')
    user = db.relationship('User', backref='event_feedback')

    def __repr__(self):
        return f'<EventFeedback {self.id}>'

class EventResource(db.Model):
    """Model for event resources"""
    __tablename__ = 'event_resources'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    file_type = db.Column(db.String(50))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_public = db.Column(db.Boolean, default=True)

    # Relationships
    event = db.relationship('Event', backref='resources')
    uploader = db.relationship('User', backref='uploaded_resources')

    def __repr__(self):
        return f'<EventResource {self.name}>' 