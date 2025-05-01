from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    Facility, FacilityType, FacilityBooking,
    FacilityMaintenance, FacilityInventory,
    FacilityLocation, FacilityAccess, FacilityUsage,
    FacilityDamage, FacilityReport, FacilityPayment,
    FacilityAllocation, FacilityInspection, FacilityCleaning,
    FacilityAmenity, FacilityRule
)
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

facilities_bp = Blueprint('facilities', __name__)

@facilities_bp.route('/facilities', methods=['GET'])
@jwt_required()
@role_required(['admin', 'facilities_manager'])
def get_facilities():
    """Get all facilities with optional filters"""
    try:
        facility_type = request.args.get('facility_type')
        location = request.args.get('location')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Facility.query
        
        if facility_type:
            query = query.filter_by(facility_type=facility_type)
        if location:
            query = query.filter_by(location=location)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Facility.available_from >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Facility.available_until <= datetime.fromisoformat(end_date))
        
        facilities = query.all()
        return format_response([facility.to_dict() for facility in facilities])
    except Exception as e:
        return handle_exception(e)

@facilities_bp.route('/types', methods=['GET'])
@jwt_required()
@role_required(['admin', 'facilities_manager'])
def get_facility_types():
    """Get all facility types with optional filters"""
    try:
        name = request.args.get('name')
        category = request.args.get('category')
        status = request.args.get('status')
        
        query = FacilityType.query
        
        if name:
            query = query.filter(FacilityType.name.ilike(f'%{name}%'))
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        
        types = query.all()
        return format_response([type_.to_dict() for type_ in types])
    except Exception as e:
        return handle_exception(e)

@facilities_bp.route('/bookings', methods=['GET'])
@jwt_required()
@role_required(['admin', 'facilities_manager'])
def get_bookings():
    """Get all facility bookings with optional filters"""
    try:
        facility_id = request.args.get('facility_id')
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = FacilityBooking.query
        
        if facility_id:
            query = query.filter_by(facility_id=facility_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(FacilityBooking.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(FacilityBooking.end_date <= datetime.fromisoformat(end_date))
        
        bookings = query.all()
        return format_response([booking.to_dict() for booking in bookings])
    except Exception as e:
        return handle_exception(e)

@facilities_bp.route('/maintenance', methods=['GET'])
@jwt_required()
@role_required(['admin', 'facilities_manager'])
def get_maintenance():
    """Get all maintenance records with optional filters"""
    try:
        facility_id = request.args.get('facility_id')
        maintenance_type = request.args.get('maintenance_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = FacilityMaintenance.query
        
        if facility_id:
            query = query.filter_by(facility_id=facility_id)
        if maintenance_type:
            query = query.filter_by(maintenance_type=maintenance_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(FacilityMaintenance.date_reported >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(FacilityMaintenance.date_reported <= datetime.fromisoformat(end_date))
        
        maintenance = query.all()
        return format_response([record.to_dict() for record in maintenance])
    except Exception as e:
        return handle_exception(e)

@facilities_bp.route('/inventory', methods=['GET'])
@jwt_required()
@role_required(['admin', 'facilities_manager'])
def get_inventory():
    """Get all inventory records with optional filters"""
    try:
        facility_id = request.args.get('facility_id')
        item_type = request.args.get('item_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = FacilityInventory.query
        
        if facility_id:
            query = query.filter_by(facility_id=facility_id)
        if item_type:
            query = query.filter_by(item_type=item_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(FacilityInventory.acquisition_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(FacilityInventory.acquisition_date <= datetime.fromisoformat(end_date))
        
        inventory = query.all()
        return format_response([item.to_dict() for item in inventory])
    except Exception as e:
        return handle_exception(e) 