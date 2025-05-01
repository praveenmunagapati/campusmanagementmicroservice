from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    EnergyUsage, EnergyGoal, WasteManagement, WasteReductionGoal,
    SustainabilityProject, ProjectTeam, SustainabilityEvent, EventRegistration,
    EnergyConsumption, GreenBuilding,
    SustainabilityGoal, SustainabilityMetric,
    SustainabilityReport, SustainabilityResource,
    SustainabilityWaste, SustainabilityEnergy, SustainabilityWater,
    SustainabilityTransport, SustainabilityFood, SustainabilityEducation,
    SustainabilityPolicy, SustainabilityAward
)
from .. import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception
import json

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
@role_required(['admin', 'sustainability_manager'])
def get_sustainability_projects():
    """Get all sustainability projects with optional filters"""
    try:
        project_type = request.args.get('project_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = SustainabilityProject.query
        
        if project_type:
            query = query.filter_by(project_type=project_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(SustainabilityProject.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(SustainabilityProject.end_date <= datetime.fromisoformat(end_date))
        
        projects = query.all()
        return format_response([project.to_dict() for project in projects])
    except Exception as e:
        return handle_exception(e)

@sustainability_bp.route('/projects/<int:id>', methods=['GET'])
@jwt_required()
def get_project(id):
    """Get specific sustainability project"""
    project = SustainabilityProject.query.get_or_404(id)
    return jsonify({
        'status': 'success',
        'data': project.to_dict()
    }), 200

@sustainability_bp.route('/projects', methods=['POST'])
@jwt_required()
@role_required(['admin', 'sustainability_staff'])
def create_project():
    """Create new sustainability project"""
    data = request.get_json()
    
    project = SustainabilityProject(
        title=data['title'],
        description=data.get('description'),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None,
        category=data['category'],
        impact_metrics=json.dumps(data.get('impact_metrics', {})),
        budget=data.get('budget'),
        created_by=get_jwt_identity()['id']
    )
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': project.to_dict()
    }), 201

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
@role_required(['admin', 'sustainability_manager'])
def get_sustainability_events():
    """Get all sustainability events with optional filters"""
    try:
        event_type = request.args.get('event_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = SustainabilityEvent.query
        
        if event_type:
            query = query.filter_by(event_type=event_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(SustainabilityEvent.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(SustainabilityEvent.end_date <= datetime.fromisoformat(end_date))
        
        events = query.all()
        return format_response([event.to_dict() for event in events])
    except Exception as e:
        return handle_exception(e)

@sustainability_bp.route('/events/<int:id>', methods=['GET'])
@jwt_required()
def get_event(id):
    """Get specific sustainability event"""
    event = SustainabilityEvent.query.get_or_404(id)
    return jsonify({
        'status': 'success',
        'data': event.to_dict()
    }), 200

@sustainability_bp.route('/events', methods=['POST'])
@jwt_required()
@role_required(['admin', 'sustainability_staff'])
def create_event():
    """Create new sustainability event"""
    data = request.get_json()
    
    event = SustainabilityEvent(
        title=data['title'],
        description=data.get('description'),
        event_date=datetime.strptime(data['event_date'], '%Y-%m-%dT%H:%M:%S'),
        location=data.get('location'),
        event_type=data['event_type'],
        target_audience=data.get('target_audience'),
        registration_link=data.get('registration_link'),
        created_by=get_jwt_identity()['id']
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': event.to_dict()
    }), 201

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

# Energy Consumption Routes
@sustainability_bp.route('/energy', methods=['GET'])
@jwt_required()
def get_energy_consumption():
    """Get energy consumption records"""
    building_id = request.args.get('building_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = EnergyConsumption.query
    
    if building_id:
        query = query.filter_by(building_id=building_id)
    if start_date:
        query = query.filter(EnergyConsumption.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(EnergyConsumption.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    records = query.all()
    return jsonify({
        'status': 'success',
        'data': [record.to_dict() for record in records]
    }), 200

@sustainability_bp.route('/energy', methods=['POST'])
@jwt_required()
@role_required(['admin', 'sustainability_staff'])
def create_energy_record():
    """Create new energy consumption record"""
    data = request.get_json()
    
    record = EnergyConsumption(
        building_id=data['building_id'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        electricity_usage=data.get('electricity_usage'),
        gas_usage=data.get('gas_usage'),
        water_usage=data.get('water_usage'),
        notes=data.get('notes')
    )
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': record.to_dict()
    }), 201

# Waste Management Routes
@sustainability_bp.route('/waste', methods=['GET'])
@jwt_required()
def get_waste_records():
    """Get waste management records"""
    building_id = request.args.get('building_id')
    waste_type = request.args.get('waste_type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = WasteManagement.query
    
    if building_id:
        query = query.filter_by(building_id=building_id)
    if waste_type:
        query = query.filter_by(waste_type=waste_type)
    if start_date:
        query = query.filter(WasteManagement.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(WasteManagement.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    records = query.all()
    return jsonify({
        'status': 'success',
        'data': [record.to_dict() for record in records]
    }), 200

@sustainability_bp.route('/waste', methods=['POST'])
@jwt_required()
@role_required(['admin', 'sustainability_staff'])
def create_waste_record():
    """Create new waste management record"""
    data = request.get_json()
    
    record = WasteManagement(
        building_id=data['building_id'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        waste_type=data['waste_type'],
        amount=data.get('amount'),
        disposal_method=data.get('disposal_method'),
        notes=data.get('notes')
    )
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': record.to_dict()
    }), 201

# Green Building Routes
@sustainability_bp.route('/green-buildings', methods=['GET'])
@jwt_required()
def get_green_buildings():
    """Get all green building certifications"""
    buildings = GreenBuilding.query.all()
    return jsonify({
        'status': 'success',
        'data': [building.to_dict() for building in buildings]
    }), 200

@sustainability_bp.route('/green-buildings/<int:id>', methods=['GET'])
@jwt_required()
def get_green_building(id):
    """Get specific green building certification"""
    building = GreenBuilding.query.get_or_404(id)
    return jsonify({
        'status': 'success',
        'data': building.to_dict()
    }), 200

@sustainability_bp.route('/green-buildings', methods=['POST'])
@jwt_required()
@role_required(['admin', 'sustainability_staff'])
def create_green_building():
    """Create new green building certification"""
    data = request.get_json()
    
    building = GreenBuilding(
        building_id=data['building_id'],
        certification=data.get('certification'),
        certification_level=data.get('certification_level'),
        certification_date=datetime.strptime(data['certification_date'], '%Y-%m-%d').date() if data.get('certification_date') else None,
        renewable_energy_usage=data.get('renewable_energy_usage'),
        water_efficiency_score=data.get('water_efficiency_score'),
        energy_efficiency_score=data.get('energy_efficiency_score'),
        waste_management_score=data.get('waste_management_score'),
        notes=data.get('notes')
    )
    
    db.session.add(building)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': building.to_dict()
    }), 201

# Sustainability Goal Routes
@sustainability_bp.route('/goals', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sustainability_manager'])
def get_sustainability_goals():
    """Get all sustainability goals with optional filters"""
    try:
        goal_type = request.args.get('goal_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = SustainabilityGoal.query
        
        if goal_type:
            query = query.filter_by(goal_type=goal_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(SustainabilityGoal.target_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(SustainabilityGoal.target_date <= datetime.fromisoformat(end_date))
        
        goals = query.all()
        return format_response([goal.to_dict() for goal in goals])
    except Exception as e:
        return handle_exception(e)

# Sustainability Metric Routes
@sustainability_bp.route('/metrics', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sustainability_manager'])
def get_sustainability_metrics():
    """Get all sustainability metrics with optional filters"""
    try:
        metric_type = request.args.get('metric_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = SustainabilityMetric.query
        
        if metric_type:
            query = query.filter_by(metric_type=metric_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(SustainabilityMetric.measurement_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(SustainabilityMetric.measurement_date <= datetime.fromisoformat(end_date))
        
        metrics = query.all()
        return format_response([metric.to_dict() for metric in metrics])
    except Exception as e:
        return handle_exception(e)

# Sustainability Report Routes
@sustainability_bp.route('/reports', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sustainability_manager'])
def get_sustainability_reports():
    """Get all sustainability reports with optional filters"""
    try:
        report_type = request.args.get('report_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = SustainabilityReport.query
        
        if report_type:
            query = query.filter_by(report_type=report_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(SustainabilityReport.report_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(SustainabilityReport.report_date <= datetime.fromisoformat(end_date))
        
        reports = query.all()
        return format_response([report.to_dict() for report in reports])
    except Exception as e:
        return handle_exception(e)

# Sustainability Resource Routes
@sustainability_bp.route('/resources', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sustainability_manager'])
def get_sustainability_resources():
    """Get all sustainability resources with optional filters"""
    try:
        resource_type = request.args.get('resource_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = SustainabilityResource.query
        
        if resource_type:
            query = query.filter_by(resource_type=resource_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(SustainabilityResource.acquisition_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(SustainabilityResource.acquisition_date <= datetime.fromisoformat(end_date))
        
        resources = query.all()
        return format_response([resource.to_dict() for resource in resources])
    except Exception as e:
        return handle_exception(e)

# Sustainability Waste Routes
@sustainability_bp.route('/waste', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sustainability_manager'])
def get_sustainability_waste():
    """Get all sustainability waste records with optional filters"""
    try:
        waste_type = request.args.get('waste_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = SustainabilityWaste.query
        
        if waste_type:
            query = query.filter_by(waste_type=waste_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(SustainabilityWaste.measurement_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(SustainabilityWaste.measurement_date <= datetime.fromisoformat(end_date))
        
        waste_records = query.all()
        return format_response([record.to_dict() for record in waste_records])
    except Exception as e:
        return handle_exception(e)

# Sustainability Energy Routes
@sustainability_bp.route('/energy', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sustainability_manager'])
def get_sustainability_energy():
    """Get all sustainability energy records with optional filters"""
    try:
        energy_type = request.args.get('energy_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = SustainabilityEnergy.query
        
        if energy_type:
            query = query.filter_by(energy_type=energy_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(SustainabilityEnergy.measurement_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(SustainabilityEnergy.measurement_date <= datetime.fromisoformat(end_date))
        
        energy_records = query.all()
        return format_response([record.to_dict() for record in energy_records])
    except Exception as e:
        return handle_exception(e)

# Sustainability Water Routes
@sustainability_bp.route('/water', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sustainability_manager'])
def get_sustainability_water():
    """Get all sustainability water records with optional filters"""
    try:
        water_type = request.args.get('water_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = SustainabilityWater.query
        
        if water_type:
            query = query.filter_by(water_type=water_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(SustainabilityWater.measurement_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(SustainabilityWater.measurement_date <= datetime.fromisoformat(end_date))
        
        water_records = query.all()
        return format_response([record.to_dict() for record in water_records])
    except Exception as e:
        return handle_exception(e)

# Sustainability Transport Routes
@sustainability_bp.route('/transport', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sustainability_manager'])
def get_sustainability_transport():
    """Get all sustainability transport records with optional filters"""
    try:
        transport_type = request.args.get('transport_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = SustainabilityTransport.query
        
        if transport_type:
            query = query.filter_by(transport_type=transport_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(SustainabilityTransport.measurement_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(SustainabilityTransport.measurement_date <= datetime.fromisoformat(end_date))
        
        transport_records = query.all()
        return format_response([record.to_dict() for record in transport_records])
    except Exception as e:
        return handle_exception(e)

# Sustainability Food Routes
@sustainability_bp.route('/food', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sustainability_manager'])
def get_sustainability_food():
    """Get all sustainability food records with optional filters"""
    try:
        food_type = request.args.get('food_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = SustainabilityFood.query
        
        if food_type:
            query = query.filter_by(food_type=food_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(SustainabilityFood.measurement_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(SustainabilityFood.measurement_date <= datetime.fromisoformat(end_date))
        
        food_records = query.all()
        return format_response([record.to_dict() for record in food_records])
    except Exception as e:
        return handle_exception(e)

# Sustainability Education Routes
@sustainability_bp.route('/education', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sustainability_manager'])
def get_sustainability_education():
    """Get all sustainability education records with optional filters"""
    try:
        education_type = request.args.get('education_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = SustainabilityEducation.query
        
        if education_type:
            query = query.filter_by(education_type=education_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(SustainabilityEducation.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(SustainabilityEducation.end_date <= datetime.fromisoformat(end_date))
        
        education_records = query.all()
        return format_response([record.to_dict() for record in education_records])
    except Exception as e:
        return handle_exception(e)

# Sustainability Policy Routes
@sustainability_bp.route('/policies', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sustainability_manager'])
def get_sustainability_policies():
    """Get all sustainability policies with optional filters"""
    try:
        policy_type = request.args.get('policy_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = SustainabilityPolicy.query
        
        if policy_type:
            query = query.filter_by(policy_type=policy_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(SustainabilityPolicy.effective_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(SustainabilityPolicy.effective_date <= datetime.fromisoformat(end_date))
        
        policies = query.all()
        return format_response([policy.to_dict() for policy in policies])
    except Exception as e:
        return handle_exception(e)

# Sustainability Award Routes
@sustainability_bp.route('/awards', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sustainability_manager'])
def get_sustainability_awards():
    """Get all sustainability awards with optional filters"""
    try:
        award_type = request.args.get('award_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = SustainabilityAward.query
        
        if award_type:
            query = query.filter_by(award_type=award_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(SustainabilityAward.award_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(SustainabilityAward.award_date <= datetime.fromisoformat(end_date))
        
        awards = query.all()
        return format_response([award.to_dict() for award in awards])
    except Exception as e:
        return handle_exception(e) 