from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    Resource, ResourceType, ResourceCategory, ResourceBooking,
    ResourceMaintenance, ResourceInventory, ResourceLocation,
    ResourceAccess, ResourceUsage, ResourceDamage, ResourceReport
)
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/resources', methods=['GET'])
@jwt_required()
@role_required(['admin', 'resource_manager'])
def get_resources():
    """Get all resources with optional filters"""
    try:
        resource_type = request.args.get('resource_type')
        category = request.args.get('category')
        location = request.args.get('location')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Resource.query
        
        if resource_type:
            query = query.filter_by(resource_type=resource_type)
        if category:
            query = query.filter_by(category=category)
        if location:
            query = query.filter_by(location=location)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Resource.acquisition_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Resource.acquisition_date <= datetime.fromisoformat(end_date))
        
        resources = query.all()
        return format_response([resource.to_dict() for resource in resources])
    except Exception as e:
        return handle_exception(e)

@resources_bp.route('/types', methods=['GET'])
@jwt_required()
@role_required(['admin', 'resource_manager'])
def get_resource_types():
    """Get all resource types with optional filters"""
    try:
        category = request.args.get('category')
        status = request.args.get('status')
        
        query = ResourceType.query
        
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        
        types = query.all()
        return format_response([type.to_dict() for type in types])
    except Exception as e:
        return handle_exception(e)

@resources_bp.route('/categories', methods=['GET'])
@jwt_required()
@role_required(['admin', 'resource_manager'])
def get_resource_categories():
    """Get all resource categories with optional filters"""
    try:
        parent_category = request.args.get('parent_category')
        status = request.args.get('status')
        
        query = ResourceCategory.query
        
        if parent_category:
            query = query.filter_by(parent_category=parent_category)
        if status:
            query = query.filter_by(status=status)
        
        categories = query.all()
        return format_response([category.to_dict() for category in categories])
    except Exception as e:
        return handle_exception(e)

@resources_bp.route('/bookings', methods=['GET'])
@jwt_required()
@role_required(['admin', 'resource_manager'])
def get_resource_bookings():
    """Get all resource bookings with optional filters"""
    try:
        resource_id = request.args.get('resource_id')
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResourceBooking.query
        
        if resource_id:
            query = query.filter_by(resource_id=resource_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResourceBooking.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResourceBooking.end_date <= datetime.fromisoformat(end_date))
        
        bookings = query.all()
        return format_response([booking.to_dict() for booking in bookings])
    except Exception as e:
        return handle_exception(e)

@resources_bp.route('/maintenance', methods=['GET'])
@jwt_required()
@role_required(['admin', 'resource_manager'])
def get_resource_maintenance():
    """Get all resource maintenance records with optional filters"""
    try:
        resource_id = request.args.get('resource_id')
        maintenance_type = request.args.get('maintenance_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResourceMaintenance.query
        
        if resource_id:
            query = query.filter_by(resource_id=resource_id)
        if maintenance_type:
            query = query.filter_by(maintenance_type=maintenance_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResourceMaintenance.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResourceMaintenance.date <= datetime.fromisoformat(end_date))
        
        maintenance_records = query.all()
        return format_response([record.to_dict() for record in maintenance_records])
    except Exception as e:
        return handle_exception(e)

@resources_bp.route('/inventory', methods=['GET'])
@jwt_required()
@role_required(['admin', 'resource_manager'])
def get_resource_inventory():
    """Get all resource inventory records with optional filters"""
    try:
        resource_id = request.args.get('resource_id')
        item_type = request.args.get('item_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResourceInventory.query
        
        if resource_id:
            query = query.filter_by(resource_id=resource_id)
        if item_type:
            query = query.filter_by(item_type=item_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResourceInventory.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResourceInventory.date <= datetime.fromisoformat(end_date))
        
        inventory_records = query.all()
        return format_response([record.to_dict() for record in inventory_records])
    except Exception as e:
        return handle_exception(e)

@resources_bp.route('/locations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'resource_manager'])
def get_resource_locations():
    """Get all resource locations with optional filters"""
    try:
        location_type = request.args.get('location_type')
        status = request.args.get('status')
        
        query = ResourceLocation.query
        
        if location_type:
            query = query.filter_by(location_type=location_type)
        if status:
            query = query.filter_by(status=status)
        
        locations = query.all()
        return format_response([location.to_dict() for location in locations])
    except Exception as e:
        return handle_exception(e)

@resources_bp.route('/access', methods=['GET'])
@jwt_required()
@role_required(['admin', 'resource_manager'])
def get_resource_access():
    """Get all resource access records with optional filters"""
    try:
        resource_id = request.args.get('resource_id')
        user_id = request.args.get('user_id')
        access_type = request.args.get('access_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResourceAccess.query
        
        if resource_id:
            query = query.filter_by(resource_id=resource_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if access_type:
            query = query.filter_by(access_type=access_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResourceAccess.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResourceAccess.date <= datetime.fromisoformat(end_date))
        
        access_records = query.all()
        return format_response([record.to_dict() for record in access_records])
    except Exception as e:
        return handle_exception(e)

@resources_bp.route('/usage', methods=['GET'])
@jwt_required()
@role_required(['admin', 'resource_manager'])
def get_resource_usage():
    """Get all resource usage records with optional filters"""
    try:
        resource_id = request.args.get('resource_id')
        user_id = request.args.get('user_id')
        usage_type = request.args.get('usage_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResourceUsage.query
        
        if resource_id:
            query = query.filter_by(resource_id=resource_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if usage_type:
            query = query.filter_by(usage_type=usage_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResourceUsage.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResourceUsage.date <= datetime.fromisoformat(end_date))
        
        usage_records = query.all()
        return format_response([record.to_dict() for record in usage_records])
    except Exception as e:
        return handle_exception(e)

@resources_bp.route('/damage', methods=['GET'])
@jwt_required()
@role_required(['admin', 'resource_manager'])
def get_resource_damage():
    """Get all resource damage records with optional filters"""
    try:
        resource_id = request.args.get('resource_id')
        damage_type = request.args.get('damage_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResourceDamage.query
        
        if resource_id:
            query = query.filter_by(resource_id=resource_id)
        if damage_type:
            query = query.filter_by(damage_type=damage_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResourceDamage.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResourceDamage.date <= datetime.fromisoformat(end_date))
        
        damage_records = query.all()
        return format_response([record.to_dict() for record in damage_records])
    except Exception as e:
        return handle_exception(e)

@resources_bp.route('/reports', methods=['GET'])
@jwt_required()
@role_required(['admin', 'resource_manager'])
def get_resource_reports():
    """Get all resource reports with optional filters"""
    try:
        resource_id = request.args.get('resource_id')
        report_type = request.args.get('report_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResourceReport.query
        
        if resource_id:
            query = query.filter_by(resource_id=resource_id)
        if report_type:
            query = query.filter_by(report_type=report_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResourceReport.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResourceReport.date <= datetime.fromisoformat(end_date))
        
        reports = query.all()
        return format_response([report.to_dict() for report in reports])
    except Exception as e:
        return handle_exception(e)

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

@resources_bp.route('/resources/available', methods=['GET'])
@jwt_required()
def get_available_resources():
    """Get all available resources"""
    resources = Resource.query.filter_by(status='available').all()
    return jsonify([resource.to_dict() for resource in resources]) 