from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    Ticket, TicketType, TicketCategory,
    TicketPriority, TicketStatus, TicketComment,
    TicketAttachment, TicketAssignment, TicketResolution,
    TicketFeedback, TicketReport, TicketPolicy,
    TicketResource, TicketStaff, TicketFacility,
    TicketEquipment, TicketInventory, TicketLocation,
    SupportTicket, ITEquipment, SupportStaff, SoftwareLicense, NetworkIssue, SystemMaintenance, ITResource
)
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

it_support_bp = Blueprint('it_support', __name__)

@it_support_bp.route('/tickets', methods=['GET'])
@jwt_required()
@role_required(['admin', 'it_support_manager'])
def get_tickets():
    """Get all tickets with optional filters"""
    try:
        ticket_type = request.args.get('ticket_type')
        category = request.args.get('category')
        priority = request.args.get('priority')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Ticket.query
        
        if ticket_type:
            query = query.filter_by(ticket_type=ticket_type)
        if category:
            query = query.filter_by(category=category)
        if priority:
            query = query.filter_by(priority=priority)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Ticket.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Ticket.created_at <= datetime.fromisoformat(end_date))
        
        tickets = query.all()
        return format_response([ticket.to_dict() for ticket in tickets])
    except Exception as e:
        return handle_exception(e)

@it_support_bp.route('/types', methods=['GET'])
@jwt_required()
@role_required(['admin', 'it_support_manager'])
def get_ticket_types():
    """Get all ticket types with optional filters"""
    try:
        name = request.args.get('name')
        category = request.args.get('category')
        status = request.args.get('status')
        
        query = TicketType.query
        
        if name:
            query = query.filter(TicketType.name.ilike(f'%{name}%'))
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        
        types = query.all()
        return format_response([type_.to_dict() for type_ in types])
    except Exception as e:
        return handle_exception(e)

@it_support_bp.route('/categories', methods=['GET'])
@jwt_required()
@role_required(['admin', 'it_support_manager'])
def get_categories():
    """Get all ticket categories with optional filters"""
    try:
        name = request.args.get('name')
        parent_category = request.args.get('parent_category')
        status = request.args.get('status')
        
        query = TicketCategory.query
        
        if name:
            query = query.filter(TicketCategory.name.ilike(f'%{name}%'))
        if parent_category:
            query = query.filter_by(parent_category=parent_category)
        if status:
            query = query.filter_by(status=status)
        
        categories = query.all()
        return format_response([category.to_dict() for category in categories])
    except Exception as e:
        return handle_exception(e)

@it_support_bp.route('/priorities', methods=['GET'])
@jwt_required()
@role_required(['admin', 'it_support_manager'])
def get_priorities():
    """Get all ticket priorities with optional filters"""
    try:
        name = request.args.get('name')
        level = request.args.get('level')
        status = request.args.get('status')
        
        query = TicketPriority.query
        
        if name:
            query = query.filter(TicketPriority.name.ilike(f'%{name}%'))
        if level:
            query = query.filter_by(level=level)
        if status:
            query = query.filter_by(status=status)
        
        priorities = query.all()
        return format_response([priority.to_dict() for priority in priorities])
    except Exception as e:
        return handle_exception(e)

@it_support_bp.route('/statuses', methods=['GET'])
@jwt_required()
@role_required(['admin', 'it_support_manager'])
def get_statuses():
    """Get all ticket statuses with optional filters"""
    try:
        name = request.args.get('name')
        category = request.args.get('category')
        status = request.args.get('status')
        
        query = TicketStatus.query
        
        if name:
            query = query.filter(TicketStatus.name.ilike(f'%{name}%'))
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        
        statuses = query.all()
        return format_response([status_.to_dict() for status_ in statuses])
    except Exception as e:
        return handle_exception(e)

# Support Ticket Routes
@it_support_bp.route('/tickets', methods=['POST'])
@jwt_required()
def create_ticket():
    data = request.get_json()
    ticket = SupportTicket(
        user_id=data['user_id'],
        title=data['title'],
        description=data['description'],
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'open'),
        created_at=datetime.fromisoformat(data['created_at'])
    )
    db.session.add(ticket)
    db.session.commit()
    return jsonify({'message': 'Support ticket created successfully', 'id': ticket.id}), 201

# IT Equipment Routes
@it_support_bp.route('/equipment', methods=['GET'])
@jwt_required()
@role_required(['admin', 'it_support'])
def get_equipment():
    equipment = ITEquipment.query.all()
    return jsonify([{
        'id': e.id,
        'name': e.name,
        'type': e.type,
        'serial_number': e.serial_number,
        'location': e.location,
        'status': e.status,
        'last_maintenance': e.last_maintenance.isoformat() if e.last_maintenance else None
    } for e in equipment])

@it_support_bp.route('/equipment', methods=['POST'])
@jwt_required()
@role_required(['admin', 'it_support'])
def create_equipment():
    data = request.get_json()
    equipment = ITEquipment(
        name=data['name'],
        type=data['type'],
        serial_number=data['serial_number'],
        location=data['location'],
        status=data.get('status', 'active'),
        last_maintenance=datetime.fromisoformat(data['last_maintenance']) if data.get('last_maintenance') else None
    )
    db.session.add(equipment)
    db.session.commit()
    return jsonify({'message': 'IT equipment added successfully', 'id': equipment.id}), 201

# Support Staff Routes
@it_support_bp.route('/staff', methods=['GET'])
@jwt_required()
@role_required(['admin', 'it_support'])
def get_staff():
    staff = SupportStaff.query.all()
    return jsonify([{
        'id': s.id,
        'user_id': s.user_id,
        'role': s.role,
        'specialization': s.specialization,
        'status': s.status
    } for s in staff])

@it_support_bp.route('/staff', methods=['POST'])
@jwt_required()
@role_required(['admin', 'it_support'])
def create_staff():
    data = request.get_json()
    staff = SupportStaff(
        user_id=data['user_id'],
        role=data['role'],
        specialization=data['specialization'],
        status=data.get('status', 'active')
    )
    db.session.add(staff)
    db.session.commit()
    return jsonify({'message': 'Support staff added successfully', 'id': staff.id}), 201

# Software License Routes
@it_support_bp.route('/licenses', methods=['GET'])
@jwt_required()
@role_required(['admin', 'it_support'])
def get_licenses():
    licenses = SoftwareLicense.query.all()
    return jsonify([{
        'id': l.id,
        'software_name': l.software_name,
        'license_key': l.license_key,
        'purchase_date': l.purchase_date.isoformat(),
        'expiry_date': l.expiry_date.isoformat() if l.expiry_date else None,
        'status': l.status
    } for l in licenses])

@it_support_bp.route('/licenses', methods=['POST'])
@jwt_required()
@role_required(['admin', 'it_support'])
def create_license():
    data = request.get_json()
    license = SoftwareLicense(
        software_name=data['software_name'],
        license_key=data['license_key'],
        purchase_date=datetime.fromisoformat(data['purchase_date']),
        expiry_date=datetime.fromisoformat(data['expiry_date']) if data.get('expiry_date') else None,
        status=data.get('status', 'active')
    )
    db.session.add(license)
    db.session.commit()
    return jsonify({'message': 'Software license added successfully', 'id': license.id}), 201

# Network Issue Routes
@it_support_bp.route('/network-issues', methods=['GET'])
@jwt_required()
@role_required(['admin', 'it_support'])
def get_network_issues():
    issues = NetworkIssue.query.all()
    return jsonify([{
        'id': i.id,
        'title': i.title,
        'description': i.description,
        'severity': i.severity,
        'status': i.status,
        'reported_at': i.reported_at.isoformat(),
        'resolved_at': i.resolved_at.isoformat() if i.resolved_at else None
    } for i in issues])

@it_support_bp.route('/network-issues', methods=['POST'])
@jwt_required()
@role_required(['admin', 'it_support'])
def create_network_issue():
    data = request.get_json()
    issue = NetworkIssue(
        title=data['title'],
        description=data['description'],
        severity=data.get('severity', 'medium'),
        status=data.get('status', 'reported'),
        reported_at=datetime.fromisoformat(data['reported_at'])
    )
    db.session.add(issue)
    db.session.commit()
    return jsonify({'message': 'Network issue reported successfully', 'id': issue.id}), 201

# System Maintenance Routes
@it_support_bp.route('/maintenance', methods=['GET'])
@jwt_required()
@role_required(['admin', 'it_support'])
def get_maintenance():
    maintenance = SystemMaintenance.query.all()
    return jsonify([{
        'id': m.id,
        'title': m.title,
        'description': m.description,
        'scheduled_date': m.scheduled_date.isoformat(),
        'completed_date': m.completed_date.isoformat() if m.completed_date else None,
        'status': m.status
    } for m in maintenance])

@it_support_bp.route('/maintenance', methods=['POST'])
@jwt_required()
@role_required(['admin', 'it_support'])
def create_maintenance():
    data = request.get_json()
    maintenance = SystemMaintenance(
        title=data['title'],
        description=data['description'],
        scheduled_date=datetime.fromisoformat(data['scheduled_date']),
        status=data.get('status', 'scheduled')
    )
    db.session.add(maintenance)
    db.session.commit()
    return jsonify({'message': 'System maintenance scheduled successfully', 'id': maintenance.id}), 201

# IT Resource Routes
@it_support_bp.route('/resources', methods=['GET'])
@jwt_required()
@role_required(['admin', 'it_support'])
def get_resources():
    resources = ITResource.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'type': r.type,
        'description': r.description,
        'status': r.status
    } for r in resources])

@it_support_bp.route('/resources', methods=['POST'])
@jwt_required()
@role_required(['admin', 'it_support'])
def create_resource():
    data = request.get_json()
    resource = ITResource(
        name=data['name'],
        type=data['type'],
        description=data.get('description'),
        status=data.get('status', 'active')
    )
    db.session.add(resource)
    db.session.commit()
    return jsonify({'message': 'IT resource added successfully', 'id': resource.id}), 201 