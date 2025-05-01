from datetime import datetime
from .. import db
from sqlalchemy.dialects.postgresql import JSONB

class AlumniProfile(db.Model):
    """Model for alumni profiles"""
    __tablename__ = 'alumni_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100))
    current_employer = db.Column(db.String(200))
    job_title = db.Column(db.String(200))
    industry = db.Column(db.String(100))
    location = db.Column(db.String(200))
    contact_info = db.Column(JSONB)  # Contact details
    social_media = db.Column(JSONB)  # Social media links
    achievements = db.Column(JSONB)  # Professional achievements
    is_mentor = db.Column(db.Boolean, default=False)
    is_volunteer = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = db.Column(JSONB)  # Additional profile data

    # Relationships
    user = db.relationship('User', backref='alumni_profile')
    donations = db.relationship('Donation', backref='alumni', lazy=True)
    event_registrations = db.relationship('AlumniEventRegistration', backref='alumni', lazy=True)
    mentorship_relationships = db.relationship('Mentorship', backref='alumni', lazy=True)

    def __repr__(self):
        return f'<AlumniProfile {self.user_id}>'

class Donation(db.Model):
    """Model for alumni donations"""
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni_profiles.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    donation_type = db.Column(db.String(50))  # one-time, recurring, endowment, etc.
    purpose = db.Column(db.String(200))  # scholarship, research, general, etc.
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    donation_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')  # pending, completed, failed
    is_anonymous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Donation {self.amount}>'

class AlumniEvent(db.Model):
    """Model for alumni events"""
    __tablename__ = 'alumni_events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50))  # reunion, networking, workshop, etc.
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    capacity = db.Column(db.Integer)
    registration_deadline = db.Column(db.DateTime)
    fee = db.Column(db.Float)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, ongoing, completed, cancelled
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = db.Column(JSONB)  # Additional event data

    # Relationships
    organizer = db.relationship('User', backref='organized_alumni_events')
    registrations = db.relationship('AlumniEventRegistration', backref='event', lazy=True)

    def __repr__(self):
        return f'<AlumniEvent {self.title}>'

class AlumniEventRegistration(db.Model):
    """Model for alumni event registrations"""
    __tablename__ = 'alumni_event_registrations'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('alumni_events.id'), nullable=False)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni_profiles.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='registered')  # registered, attended, cancelled
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    additional_info = db.Column(JSONB)  # Custom registration fields
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<AlumniEventRegistration {self.id}>'

class Mentorship(db.Model):
    """Model for alumni-student mentorship relationships"""
    __tablename__ = 'mentorships'

    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni_profiles.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, completed, terminated
    focus_area = db.Column(db.String(100))
    goals = db.Column(JSONB)  # Mentorship goals
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    student = db.relationship('User', backref='mentorships')

    def __repr__(self):
        return f'<Mentorship {self.id}>'

class AlumniChapter(db.Model):
    """Model for alumni chapters/groups"""
    __tablename__ = 'alumni_chapters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    chapter_type = db.Column(db.String(50))  # regional, professional, interest-based
    president_id = db.Column(db.Integer, db.ForeignKey('alumni_profiles.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = db.Column(JSONB)  # Additional chapter data

    # Relationships
    president = db.relationship('AlumniProfile', backref='president_of_chapters')
    members = db.relationship('AlumniChapterMembership', backref='chapter', lazy=True)

    def __repr__(self):
        return f'<AlumniChapter {self.name}>'

class AlumniChapterMembership(db.Model):
    """Model for alumni chapter memberships"""
    __tablename__ = 'alumni_chapter_memberships'

    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('alumni_chapters.id'), nullable=False)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni_profiles.id'), nullable=False)
    role = db.Column(db.String(50))  # member, officer, etc.
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    alumni = db.relationship('AlumniProfile', backref='chapter_memberships')

    def __repr__(self):
        return f'<AlumniChapterMembership {self.id}>' 