from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    EnergyUsage, EnergyGoal, WasteManagement, WasteReductionGoal,
    SustainabilityProject, ProjectTeam, SustainabilityEvent, EventRegistration
)
from .. import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

sustainability_bp = Blueprint('sustainability', __name__)

# Energy Usage Routes
@sustainability_bp.route('/energy/usage', methods=['GET'])
@jwt_required()
def get_energy_usage():
    """Get all energy usage records"""
    usage = EnergyUsage.query.all()
    return jsonify([record.to_dict() for record in usage])

@sustainability_bp.route('/energy/usage', methods=['POST'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def create_energy_usage():
    """Create new energy usage record"""
    data = request.get_json()
    new_usage = EnergyUsage(**data)
    db.session.add(new_usage)
    db.session.commit()
    return jsonify(new_usage.to_dict()), 201

@sustainability_bp.route('/energy/usage/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def update_energy_usage(id):
    """Update existing energy usage record"""
    usage = EnergyUsage.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(usage, key, value)
    db.session.commit()
    return jsonify(usage.to_dict())

@sustainability_bp.route('/energy/usage/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def delete_energy_usage(id):
    """Delete energy usage record"""
    usage = EnergyUsage.query.get_or_404(id)
    db.session.delete(usage)
    db.session.commit()
    return '', 204

# Energy Goal Routes
@sustainability_bp.route('/energy/goals', methods=['GET'])
@jwt_required()
def get_energy_goals():
    """Get all energy goals"""
    goals = EnergyGoal.query.all()
    return jsonify([goal.to_dict() for goal in goals])

@sustainability_bp.route('/energy/goals', methods=['POST'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def create_energy_goal():
    """Create new energy goal"""
    data = request.get_json()
    new_goal = EnergyGoal(**data)
    db.session.add(new_goal)
    db.session.commit()
    return jsonify(new_goal.to_dict()), 201

@sustainability_bp.route('/energy/goals/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def update_energy_goal(id):
    """Update existing energy goal"""
    goal = EnergyGoal.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(goal, key, value)
    db.session.commit()
    return jsonify(goal.to_dict())

@sustainability_bp.route('/energy/goals/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def delete_energy_goal(id):
    """Delete energy goal"""
    goal = EnergyGoal.query.get_or_404(id)
    db.session.delete(goal)
    db.session.commit()
    return '', 204

# Waste Management Routes
@sustainability_bp.route('/waste/management', methods=['GET'])
@jwt_required()
def get_waste_management():
    """Get all waste management records"""
    waste = WasteManagement.query.all()
    return jsonify([record.to_dict() for record in waste])

@sustainability_bp.route('/waste/management', methods=['POST'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def create_waste_management():
    """Create new waste management record"""
    data = request.get_json()
    new_waste = WasteManagement(**data)
    db.session.add(new_waste)
    db.session.commit()
    return jsonify(new_waste.to_dict()), 201

@sustainability_bp.route('/waste/management/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def update_waste_management(id):
    """Update existing waste management record"""
    waste = WasteManagement.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(waste, key, value)
    db.session.commit()
    return jsonify(waste.to_dict())

@sustainability_bp.route('/waste/management/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def delete_waste_management(id):
    """Delete waste management record"""
    waste = WasteManagement.query.get_or_404(id)
    db.session.delete(waste)
    db.session.commit()
    return '', 204

# Waste Reduction Goal Routes
@sustainability_bp.route('/waste/goals', methods=['GET'])
@jwt_required()
def get_waste_goals():
    """Get all waste reduction goals"""
    goals = WasteReductionGoal.query.all()
    return jsonify([goal.to_dict() for goal in goals])

@sustainability_bp.route('/waste/goals', methods=['POST'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def create_waste_goal():
    """Create new waste reduction goal"""
    data = request.get_json()
    new_goal = WasteReductionGoal(**data)
    db.session.add(new_goal)
    db.session.commit()
    return jsonify(new_goal.to_dict()), 201

@sustainability_bp.route('/waste/goals/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def update_waste_goal(id):
    """Update existing waste reduction goal"""
    goal = WasteReductionGoal.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(goal, key, value)
    db.session.commit()
    return jsonify(goal.to_dict())

@sustainability_bp.route('/waste/goals/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def delete_waste_goal(id):
    """Delete waste reduction goal"""
    goal = WasteReductionGoal.query.get_or_404(id)
    db.session.delete(goal)
    db.session.commit()
    return '', 204

# Sustainability Project Routes
@sustainability_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    """Get all sustainability projects"""
    projects = SustainabilityProject.query.all()
    return jsonify([project.to_dict() for project in projects])

@sustainability_bp.route('/projects', methods=['POST'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def create_project():
    """Create new sustainability project"""
    data = request.get_json()
    new_project = SustainabilityProject(**data)
    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project.to_dict()), 201

@sustainability_bp.route('/projects/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def update_project(id):
    """Update existing sustainability project"""
    project = SustainabilityProject.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(project, key, value)
    db.session.commit()
    return jsonify(project.to_dict())

@sustainability_bp.route('/projects/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def delete_project(id):
    """Delete sustainability project"""
    project = SustainabilityProject.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return '', 204

# Project Team Routes
@sustainability_bp.route('/projects/<int:project_id>/team', methods=['GET'])
@jwt_required()
def get_project_team(project_id):
    """Get team members for a project"""
    team = ProjectTeam.query.filter_by(project_id=project_id).all()
    return jsonify([member.to_dict() for member in team])

@sustainability_bp.route('/projects/<int:project_id>/team', methods=['POST'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def add_team_member(project_id):
    """Add team member to project"""
    data = request.get_json()
    data['project_id'] = project_id
    new_member = ProjectTeam(**data)
    db.session.add(new_member)
    db.session.commit()
    return jsonify(new_member.to_dict()), 201

@sustainability_bp.route('/projects/team/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def update_team_member(id):
    """Update team member role"""
    member = ProjectTeam.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(member, key, value)
    db.session.commit()
    return jsonify(member.to_dict())

@sustainability_bp.route('/projects/team/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def remove_team_member(id):
    """Remove team member from project"""
    member = ProjectTeam.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return '', 204

# Sustainability Event Routes
@sustainability_bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    """Get all sustainability events"""
    events = SustainabilityEvent.query.all()
    return jsonify([event.to_dict() for event in events])

@sustainability_bp.route('/events', methods=['POST'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def create_event():
    """Create new sustainability event"""
    data = request.get_json()
    new_event = SustainabilityEvent(**data)
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict()), 201

@sustainability_bp.route('/events/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def update_event(id):
    """Update existing sustainability event"""
    event = SustainabilityEvent.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(event, key, value)
    db.session.commit()
    return jsonify(event.to_dict())

@sustainability_bp.route('/events/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'sustainability'])
def delete_event(id):
    """Delete sustainability event"""
    event = SustainabilityEvent.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return '', 204

# Event Registration Routes
@sustainability_bp.route('/events/<int:event_id>/registrations', methods=['GET'])
@jwt_required()
def get_event_registrations(event_id):
    """Get registrations for an event"""
    registrations = EventRegistration.query.filter_by(event_id=event_id).all()
    return jsonify([reg.to_dict() for reg in registrations])

@sustainability_bp.route('/events/<int:event_id>/register', methods=['POST'])
@jwt_required()
def register_for_event(event_id):
    """Register for an event"""
    data = request.get_json()
    data['event_id'] = event_id
    new_registration = EventRegistration(**data)
    db.session.add(new_registration)
    db.session.commit()
    return jsonify(new_registration.to_dict()), 201

@sustainability_bp.route('/events/registrations/<int:id>', methods=['PUT'])
@jwt_required()
def update_registration(id):
    """Update event registration"""
    registration = EventRegistration.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(registration, key, value)
    db.session.commit()
    return jsonify(registration.to_dict())

@sustainability_bp.route('/events/registrations/<int:id>', methods=['DELETE'])
@jwt_required()
def cancel_registration(id):
    """Cancel event registration"""
    registration = EventRegistration.query.get_or_404(id)
    db.session.delete(registration)
    db.session.commit()
    return '', 204 