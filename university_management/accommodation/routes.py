from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    Room, RoomType, RoomBooking, RoomMaintenance,
    RoomInventory, RoomLocation, RoomAccess,
    RoomUsage, RoomDamage, RoomReport, RoomPayment,
    RoomAllocation, RoomInspection, RoomCleaning
)
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

accommodation_bp = Blueprint('accommodation', __name__)

@accommodation_bp.route('/rooms', methods=['GET'])
@jwt_required()
@role_required(['admin', 'accommodation_manager'])
def get_rooms():
    """Get all rooms with optional filters"""
    try:
        room_type = request.args.get('room_type')
        location = request.args.get('location')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Room.query
        
        if room_type:
            query = query.filter_by(room_type=room_type)
        if location:
            query = query.filter_by(location=location)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Room.available_from >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Room.available_until <= datetime.fromisoformat(end_date))
        
        rooms = query.all()
        return format_response([room.to_dict() for room in rooms])
    except Exception as e:
        return handle_exception(e)

@accommodation_bp.route('/types', methods=['GET'])
@jwt_required()
@role_required(['admin', 'accommodation_manager'])
def get_room_types():
    """Get all room types with optional filters"""
    try:
        capacity = request.args.get('capacity')
        status = request.args.get('status')
        
        query = RoomType.query
        
        if capacity:
            query = query.filter_by(capacity=capacity)
        if status:
            query = query.filter_by(status=status)
        
        types = query.all()
        return format_response([type.to_dict() for type in types])
    except Exception as e:
        return handle_exception(e)

@accommodation_bp.route('/bookings', methods=['GET'])
@jwt_required()
@role_required(['admin', 'accommodation_manager'])
def get_room_bookings():
    """Get all room bookings with optional filters"""
    try:
        room_id = request.args.get('room_id')
        student_id = request.args.get('student_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = RoomBooking.query
        
        if room_id:
            query = query.filter_by(room_id=room_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(RoomBooking.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(RoomBooking.end_date <= datetime.fromisoformat(end_date))
        
        bookings = query.all()
        return format_response([booking.to_dict() for booking in bookings])
    except Exception as e:
        return handle_exception(e)

@accommodation_bp.route('/maintenance', methods=['GET'])
@jwt_required()
@role_required(['admin', 'accommodation_manager'])
def get_room_maintenance():
    """Get all room maintenance records with optional filters"""
    try:
        room_id = request.args.get('room_id')
        maintenance_type = request.args.get('maintenance_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = RoomMaintenance.query
        
        if room_id:
            query = query.filter_by(room_id=room_id)
        if maintenance_type:
            query = query.filter_by(maintenance_type=maintenance_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(RoomMaintenance.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(RoomMaintenance.date <= datetime.fromisoformat(end_date))
        
        maintenance_records = query.all()
        return format_response([record.to_dict() for record in maintenance_records])
    except Exception as e:
        return handle_exception(e)

@accommodation_bp.route('/inventory', methods=['GET'])
@jwt_required()
@role_required(['admin', 'accommodation_manager'])
def get_room_inventory():
    """Get all room inventory records with optional filters"""
    try:
        room_id = request.args.get('room_id')
        item_type = request.args.get('item_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = RoomInventory.query
        
        if room_id:
            query = query.filter_by(room_id=room_id)
        if item_type:
            query = query.filter_by(item_type=item_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(RoomInventory.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(RoomInventory.date <= datetime.fromisoformat(end_date))
        
        inventory_records = query.all()
        return format_response([record.to_dict() for record in inventory_records])
    except Exception as e:
        return handle_exception(e)

@accommodation_bp.route('/locations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'accommodation_manager'])
def get_room_locations():
    """Get all room locations with optional filters"""
    try:
        location_type = request.args.get('location_type')
        status = request.args.get('status')
        
        query = RoomLocation.query
        
        if location_type:
            query = query.filter_by(location_type=location_type)
        if status:
            query = query.filter_by(status=status)
        
        locations = query.all()
        return format_response([location.to_dict() for location in locations])
    except Exception as e:
        return handle_exception(e)

@accommodation_bp.route('/access', methods=['GET'])
@jwt_required()
@role_required(['admin', 'accommodation_manager'])
def get_room_access():
    """Get all room access records with optional filters"""
    try:
        room_id = request.args.get('room_id')
        student_id = request.args.get('student_id')
        access_type = request.args.get('access_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = RoomAccess.query
        
        if room_id:
            query = query.filter_by(room_id=room_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if access_type:
            query = query.filter_by(access_type=access_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(RoomAccess.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(RoomAccess.date <= datetime.fromisoformat(end_date))
        
        access_records = query.all()
        return format_response([record.to_dict() for record in access_records])
    except Exception as e:
        return handle_exception(e)

@accommodation_bp.route('/usage', methods=['GET'])
@jwt_required()
@role_required(['admin', 'accommodation_manager'])
def get_room_usage():
    """Get all room usage records with optional filters"""
    try:
        room_id = request.args.get('room_id')
        student_id = request.args.get('student_id')
        usage_type = request.args.get('usage_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = RoomUsage.query
        
        if room_id:
            query = query.filter_by(room_id=room_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if usage_type:
            query = query.filter_by(usage_type=usage_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(RoomUsage.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(RoomUsage.date <= datetime.fromisoformat(end_date))
        
        usage_records = query.all()
        return format_response([record.to_dict() for record in usage_records])
    except Exception as e:
        return handle_exception(e)

@accommodation_bp.route('/damage', methods=['GET'])
@jwt_required()
@role_required(['admin', 'accommodation_manager'])
def get_room_damage():
    """Get all room damage records with optional filters"""
    try:
        room_id = request.args.get('room_id')
        damage_type = request.args.get('damage_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = RoomDamage.query
        
        if room_id:
            query = query.filter_by(room_id=room_id)
        if damage_type:
            query = query.filter_by(damage_type=damage_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(RoomDamage.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(RoomDamage.date <= datetime.fromisoformat(end_date))
        
        damage_records = query.all()
        return format_response([record.to_dict() for record in damage_records])
    except Exception as e:
        return handle_exception(e)

@accommodation_bp.route('/reports', methods=['GET'])
@jwt_required()
@role_required(['admin', 'accommodation_manager'])
def get_room_reports():
    """Get all room reports with optional filters"""
    try:
        room_id = request.args.get('room_id')
        report_type = request.args.get('report_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = RoomReport.query
        
        if room_id:
            query = query.filter_by(room_id=room_id)
        if report_type:
            query = query.filter_by(report_type=report_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(RoomReport.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(RoomReport.date <= datetime.fromisoformat(end_date))
        
        reports = query.all()
        return format_response([report.to_dict() for report in reports])
    except Exception as e:
        return handle_exception(e)

@accommodation_bp.route('/payments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'accommodation_manager'])
def get_room_payments():
    """Get all room payments with optional filters"""
    try:
        room_id = request.args.get('room_id')
        student_id = request.args.get('student_id')
        payment_type = request.args.get('payment_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = RoomPayment.query
        
        if room_id:
            query = query.filter_by(room_id=room_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if payment_type:
            query = query.filter_by(payment_type=payment_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(RoomPayment.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(RoomPayment.date <= datetime.fromisoformat(end_date))
        
        payments = query.all()
        return format_response([payment.to_dict() for payment in payments])
    except Exception as e:
        return handle_exception(e)

@accommodation_bp.route('/allocations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'accommodation_manager'])
def get_room_allocations():
    """Get all room allocations with optional filters"""
    try:
        room_id = request.args.get('room_id')
        student_id = request.args.get('student_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = RoomAllocation.query
        
        if room_id:
            query = query.filter_by(room_id=room_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(RoomAllocation.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(RoomAllocation.end_date <= datetime.fromisoformat(end_date))
        
        allocations = query.all()
        return format_response([allocation.to_dict() for allocation in allocations])
    except Exception as e:
        return handle_exception(e)

@accommodation_bp.route('/inspections', methods=['GET'])
@jwt_required()
@role_required(['admin', 'accommodation_manager'])
def get_room_inspections():
    """Get all room inspections with optional filters"""
    try:
        room_id = request.args.get('room_id')
        inspector_id = request.args.get('inspector_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = RoomInspection.query
        
        if room_id:
            query = query.filter_by(room_id=room_id)
        if inspector_id:
            query = query.filter_by(inspector_id=inspector_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(RoomInspection.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(RoomInspection.date <= datetime.fromisoformat(end_date))
        
        inspections = query.all()
        return format_response([inspection.to_dict() for inspection in inspections])
    except Exception as e:
        return handle_exception(e)

@accommodation_bp.route('/cleaning', methods=['GET'])
@jwt_required()
@role_required(['admin', 'accommodation_manager'])
def get_room_cleaning():
    """Get all room cleaning records with optional filters"""
    try:
        room_id = request.args.get('room_id')
        cleaner_id = request.args.get('cleaner_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = RoomCleaning.query
        
        if room_id:
            query = query.filter_by(room_id=room_id)
        if cleaner_id:
            query = query.filter_by(cleaner_id=cleaner_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(RoomCleaning.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(RoomCleaning.date <= datetime.fromisoformat(end_date))
        
        cleaning_records = query.all()
        return format_response([record.to_dict() for record in cleaning_records])
    except Exception as e:
        return handle_exception(e) 