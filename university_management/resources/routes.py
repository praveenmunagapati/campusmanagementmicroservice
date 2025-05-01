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
    resources = Resource.query.all()
    return jsonify([resource.to_dict() for resource in resources])

@resources_bp.route('/resources/<int:id>', methods=['GET'])
@jwt_required()
def get_resource_by_id(id):
    """Get specific resource by ID"""
    resource = Resource.query.get_or_404(id)
    return jsonify(resource.to_dict())

@resources_bp.route('/resources', methods=['POST'])
@jwt_required()
@role_required(['admin', 'facilities'])
def create_resource():
    """Create new resource"""
    data = request.get_json()
    new_resource = Resource(**data)
    db.session.add(new_resource)
    db.session.commit()
    return jsonify(new_resource.to_dict()), 201

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
@resources_bp.route('/resources/bookings', methods=['GET'])
@jwt_required()
def get_resource_bookings():
    """Get all resource bookings"""
    bookings = ResourceBooking.query.all()
    return jsonify([booking.to_dict() for booking in bookings])

@resources_bp.route('/resources/bookings', methods=['POST'])
@jwt_required()
def create_resource_booking():
    """Create new resource booking"""
    data = request.get_json()
    new_booking = ResourceBooking(**data)
    db.session.add(new_booking)
    db.session.commit()
    return jsonify(new_booking.to_dict()), 201

@resources_bp.route('/resources/<int:resource_id>/bookings', methods=['GET'])
@jwt_required()
def get_resource_bookings_by_resource(resource_id):
    """Get bookings for specific resource"""
    bookings = ResourceBooking.query.filter_by(resource_id=resource_id).all()
    return jsonify([booking.to_dict() for booking in bookings])

@resources_bp.route('/resources/bookings/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'facilities'])
def update_resource_booking(id):
    """Update existing resource booking"""
    booking = ResourceBooking.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(booking, key, value)
    db.session.commit()
    return jsonify(booking.to_dict())

@resources_bp.route('/resources/bookings/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'facilities'])
def delete_resource_booking(id):
    """Delete resource booking"""
    booking = ResourceBooking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    return '', 204

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
@resources_bp.route('/resources/maintenance', methods=['GET'])
@jwt_required()
def get_resource_maintenance():
    """Get all resource maintenance records"""
    maintenance = ResourceMaintenance.query.all()
    return jsonify([record.to_dict() for record in maintenance])

@resources_bp.route('/resources/maintenance', methods=['POST'])
@jwt_required()
@role_required(['admin', 'facilities'])
def create_resource_maintenance():
    """Create new resource maintenance record"""
    data = request.get_json()
    new_maintenance = ResourceMaintenance(**data)
    db.session.add(new_maintenance)
    db.session.commit()
    return jsonify(new_maintenance.to_dict()), 201

@resources_bp.route('/resources/maintenance/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'facilities'])
def update_resource_maintenance(id):
    """Update existing resource maintenance record"""
    maintenance = ResourceMaintenance.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(maintenance, key, value)
    db.session.commit()
    return jsonify(maintenance.to_dict())

@resources_bp.route('/resources/maintenance/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'facilities'])
def delete_resource_maintenance(id):
    """Delete resource maintenance record"""
    maintenance = ResourceMaintenance.query.get_or_404(id)
    db.session.delete(maintenance)
    db.session.commit()
    return '', 204

@resources_bp.route('/resources/available', methods=['GET'])
@jwt_required()
def get_available_resources():
    """Get all available resources"""
    resources = Resource.query.filter_by(status='available').all()
    return jsonify([resource.to_dict() for resource in resources]) 