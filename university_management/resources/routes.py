from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Resource, ResourceBooking, ResourceCategory, ResourceMaintenance
from .. import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

resources_bp = Blueprint('resources', __name__)

# Resource Routes
@resources_bp.route('/resources', methods=['GET'])
@jwt_required()
def get_resources():
    """Get all resources"""
    category = request.args.get('category')
    status = request.args.get('status')
    
    query = Resource.query
    
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)
    
    resources = query.all()
    return jsonify({
        'status': 'success',
        'data': [resource.to_dict() for resource in resources]
    }), 200

@resources_bp.route('/resources/<int:id>', methods=['GET'])
@jwt_required()
def get_resource(id):
    """Get specific resource"""
    resource = Resource.query.get_or_404(id)
    return jsonify({
        'status': 'success',
        'data': resource.to_dict()
    }), 200

@resources_bp.route('/resources', methods=['POST'])
@jwt_required()
@role_required(['admin', 'resource_manager'])
def create_resource():
    """Create new resource"""
    data = request.get_json()
    
    resource = Resource(
        name=data['name'],
        description=data.get('description'),
        category=data['category'],
        quantity=data.get('quantity', 1),
        location=data.get('location'),
        status=data.get('status', 'available')
    )
    
    db.session.add(resource)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': resource.to_dict()
    }), 201

@resources_bp.route('/resources/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'facilities'])
def update_resource(id):
    """Update existing resource"""
    resource = Resource.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(resource, key, value)
    db.session.commit()
    return jsonify(resource.to_dict())

@resources_bp.route('/resources/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'facilities'])
def delete_resource(id):
    """Delete resource"""
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    return '', 204

# Resource Booking Routes
@resources_bp.route('/bookings', methods=['GET'])
@jwt_required()
def get_bookings():
    """Get all resource bookings"""
    resource_id = request.args.get('resource_id')
    user_id = request.args.get('user_id')
    status = request.args.get('status')
    
    query = ResourceBooking.query
    
    if resource_id:
        query = query.filter_by(resource_id=resource_id)
    if user_id:
        query = query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    bookings = query.all()
    return jsonify({
        'status': 'success',
        'data': [booking.to_dict() for booking in bookings]
    }), 200

@resources_bp.route('/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    """Create new resource booking"""
    data = request.get_json()
    
    booking = ResourceBooking(
        resource_id=data['resource_id'],
        user_id=get_jwt_identity()['id'],
        start_time=datetime.strptime(data['start_time'], '%Y-%m-%dT%H:%M:%S'),
        end_time=datetime.strptime(data['end_time'], '%Y-%m-%dT%H:%M:%S'),
        purpose=data.get('purpose'),
        status='pending'
    )
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': booking.to_dict()
    }), 201

@resources_bp.route('/bookings/<int:id>/approve', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'resource_manager'])
def approve_booking(id):
    """Approve resource booking"""
    booking = ResourceBooking.query.get_or_404(id)
    booking.status = 'approved'
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': booking.to_dict()
    }), 200

# Resource Category Routes
@resources_bp.route('/resources/categories', methods=['GET'])
@jwt_required()
def get_resource_categories():
    """Get all resource categories"""
    categories = ResourceCategory.query.all()
    return jsonify([category.to_dict() for category in categories])

@resources_bp.route('/resources/categories', methods=['POST'])
@jwt_required()
@role_required(['admin', 'facilities'])
def create_resource_category():
    """Create new resource category"""
    data = request.get_json()
    new_category = ResourceCategory(**data)
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.to_dict()), 201

@resources_bp.route('/resources/categories/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'facilities'])
def update_resource_category(id):
    """Update existing resource category"""
    category = ResourceCategory.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(category, key, value)
    db.session.commit()
    return jsonify(category.to_dict())

@resources_bp.route('/resources/categories/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'facilities'])
def delete_resource_category(id):
    """Delete resource category"""
    category = ResourceCategory.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return '', 204

# Resource Maintenance Routes
@resources_bp.route('/maintenance', methods=['GET'])
@jwt_required()
def get_maintenance():
    """Get all maintenance records"""
    resource_id = request.args.get('resource_id')
    status = request.args.get('status')
    
    query = ResourceMaintenance.query
    
    if resource_id:
        query = query.filter_by(resource_id=resource_id)
    if status:
        query = query.filter_by(status=status)
    
    maintenance_records = query.all()
    return jsonify({
        'status': 'success',
        'data': [record.to_dict() for record in maintenance_records]
    }), 200

@resources_bp.route('/maintenance', methods=['POST'])
@jwt_required()
@role_required(['admin', 'resource_manager'])
def create_maintenance():
    """Create new maintenance record"""
    data = request.get_json()
    
    maintenance = ResourceMaintenance(
        resource_id=data['resource_id'],
        maintenance_type=data['maintenance_type'],
        description=data.get('description'),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%dT%H:%M:%S'),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%dT%H:%M:%S') if data.get('end_date') else None,
        status='scheduled',
        cost=data.get('cost'),
        technician=data.get('technician')
    )
    
    db.session.add(maintenance)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': maintenance.to_dict()
    }), 201

@resources_bp.route('/resources/available', methods=['GET'])
@jwt_required()
def get_available_resources():
    """Get all available resources"""
    resources = Resource.query.filter_by(status='available').all()
    return jsonify([resource.to_dict() for resource in resources]) 