from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EnergyUsage(db.Model):
    __tablename__ = 'energy_usage'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    energy_type = db.Column(db.String(50), nullable=False)  # electricity, gas, water
    reading_date = db.Column(db.DateTime, nullable=False)
    reading_value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)  # kWh, m³, etc.
    cost = db.Column(db.Float)
    currency = db.Column(db.String(3), default='USD')
    source = db.Column(db.String(100))  # meter_id, provider, etc.
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    building = db.relationship('Building', backref=db.backref('energy_usage', lazy=True))

class EnergyGoal(db.Model):
    __tablename__ = 'energy_goals'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    energy_type = db.Column(db.String(50), nullable=False)
    target_value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    current_value = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')  # active, achieved, failed
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    building = db.relationship('Building', backref=db.backref('energy_goals', lazy=True))
    creator = db.relationship('User', backref=db.backref('created_energy_goals', lazy=True))

class WasteManagement(db.Model):
    __tablename__ = 'waste_management'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    waste_type = db.Column(db.String(50), nullable=False)  # paper, plastic, organic, etc.
    collection_date = db.Column(db.DateTime, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='kg')
    disposal_method = db.Column(db.String(100))
    recycling_rate = db.Column(db.Float)  # percentage
    cost = db.Column(db.Float)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    building = db.relationship('Building', backref=db.backref('waste_management', lazy=True))

class WasteReductionGoal(db.Model):
    __tablename__ = 'waste_reduction_goals'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    waste_type = db.Column(db.String(50), nullable=False)
    target_reduction = db.Column(db.Float, nullable=False)  # percentage
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    current_reduction = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')  # active, achieved, failed
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    building = db.relationship('Building', backref=db.backref('waste_reduction_goals', lazy=True))
    creator = db.relationship('User', backref=db.backref('created_waste_goals', lazy=True))

class SustainabilityProject(db.Model):
    __tablename__ = 'sustainability_projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='active')
    category = db.Column(db.String(100), nullable=False)  # energy, waste, water, etc.
    impact_metrics = db.Column(db.Text)  # JSON string of metrics
    budget = db.Column(db.Float)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'category': self.category,
            'impact_metrics': self.impact_metrics,
            'budget': self.budget,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ProjectTeam(db.Model):
    __tablename__ = 'project_teams'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('sustainability_projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = db.relationship('SustainabilityProject', backref=db.backref('team_members', lazy=True))
    user = db.relationship('User', backref=db.backref('project_roles', lazy=True))

class SustainabilityEvent(db.Model):
    __tablename__ = 'sustainability_events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    event_type = db.Column(db.String(50), nullable=False)  # workshop, campaign, cleanup, etc.
    target_audience = db.Column(db.String(100))
    registration_link = db.Column(db.String(200))
    status = db.Column(db.String(50), default='upcoming')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'event_date': self.event_date.isoformat(),
            'location': self.location,
            'event_type': self.event_type,
            'target_audience': self.target_audience,
            'registration_link': self.registration_link,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class EventRegistration(db.Model):
    __tablename__ = 'event_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('sustainability_events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='registered')  # registered, attended, cancelled
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    event = db.relationship('SustainabilityEvent', backref=db.backref('registrations', lazy=True))
    user = db.relationship('User', backref=db.backref('event_registrations', lazy=True))

class EnergyConsumption(db.Model):
    __tablename__ = 'energy_consumption'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    electricity_usage = db.Column(db.Float)  # kWh
    gas_usage = db.Column(db.Float)  # cubic meters
    water_usage = db.Column(db.Float)  # cubic meters
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'building_id': self.building_id,
            'date': self.date.isoformat(),
            'electricity_usage': self.electricity_usage,
            'gas_usage': self.gas_usage,
            'water_usage': self.water_usage,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class GreenBuilding(db.Model):
    __tablename__ = 'green_buildings'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    certification = db.Column(db.String(100))  # LEED, BREEAM, etc.
    certification_level = db.Column(db.String(50))
    certification_date = db.Column(db.Date)
    renewable_energy_usage = db.Column(db.Float)  # percentage
    water_efficiency_score = db.Column(db.Float)  # percentage
    energy_efficiency_score = db.Column(db.Float)  # percentage
    waste_management_score = db.Column(db.Float)  # percentage
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'building_id': self.building_id,
            'certification': self.certification,
            'certification_level': self.certification_level,
            'certification_date': self.certification_date.isoformat() if self.certification_date else None,
            'renewable_energy_usage': self.renewable_energy_usage,
            'water_efficiency_score': self.water_efficiency_score,
            'energy_efficiency_score': self.energy_efficiency_score,
            'waste_management_score': self.waste_management_score,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 