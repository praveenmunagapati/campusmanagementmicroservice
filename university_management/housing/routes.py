from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from .models import (
    ResidenceHall, Room, RoomOccupancy, 
    ResidenceStaff, MaintenanceRequest, 
    RoomInspection, HousingApplication,
    HousingUnit, UnitType, UnitBooking, UnitMaintenance,
    UnitInventory, UnitLocation, UnitAccess, UnitUsage,
    UnitDamage, UnitReport, UnitPayment, UnitAllocation,
    UnitInspection as UnitInspectionModel, UnitCleaning, UnitAmenity, UnitRule
)
from ..utils import role_required, validate_request, format_response, log_activity, handle_exception
from datetime import datetime

housing = Blueprint('housing', __name__)

# Residence Hall Routes
@housing.route('/halls', methods=['GET'])
@jwt_required()
def get_halls():
    """Get all residence halls"""
    halls = ResidenceHall.query.all()
    return jsonify([{
        'id': hall.id,
        'name': hall.name,
        'code': hall.code,
        'address': hall.address,
        'capacity': hall.capacity,
        'gender_type': hall.gender_type,
        'room_types': hall.room_types,
        'amenities': hall.amenities,
        'is_active': hall.is_active
    } for hall in halls]), 200

@housing.route('/halls', methods=['POST'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def create_hall():
    """Create a new residence hall"""
    data = request.get_json()
    hall = ResidenceHall(
        name=data['name'],
        code=data['code'],
        address=data['address'],
        capacity=data['capacity'],
        gender_type=data.get('gender_type'),
        room_types=data.get('room_types', {}),
        amenities=data.get('amenities', []),
        is_active=data.get('is_active', True)
    )
    db.session.add(hall)
    db.session.commit()
    return jsonify({'message': 'Residence hall created successfully', 'id': hall.id}), 201

# Room Routes
@housing.route('/rooms', methods=['GET'])
@jwt_required()
def get_rooms():
    """Get all rooms with optional hall filter"""
    hall_id = request.args.get('hall_id')
    query = Room.query
    if hall_id:
        query = query.filter_by(hall_id=hall_id)
    rooms = query.all()
    return jsonify([{
        'id': room.id,
        'hall_id': room.hall_id,
        'room_number': room.room_number,
        'room_type': room.room_type,
        'capacity': room.capacity,
        'floor': room.floor,
        'is_available': room.is_available,
        'features': room.features
    } for room in rooms]), 200

@housing.route('/rooms', methods=['POST'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def create_room():
    """Create a new room"""
    data = request.get_json()
    room = Room(
        hall_id=data['hall_id'],
        room_number=data['room_number'],
        room_type=data['room_type'],
        capacity=data['capacity'],
        floor=data['floor'],
        features=data.get('features', {})
    )
    db.session.add(room)
    db.session.commit()
    return jsonify({'message': 'Room created successfully', 'id': room.id}), 201

# Room Occupancy Routes
@housing.route('/occupancy', methods=['GET'])
@jwt_required()
def get_occupancy():
    """Get room occupancy records"""
    room_id = request.args.get('room_id')
    student_id = request.args.get('student_id')
    query = RoomOccupancy.query
    if room_id:
        query = query.filter_by(room_id=room_id)
    if student_id:
        query = query.filter_by(student_id=student_id)
    records = query.all()
    return jsonify([{
        'id': record.id,
        'room_id': record.room_id,
        'student_id': record.student_id,
        'start_date': record.start_date.isoformat(),
        'end_date': record.end_date.isoformat() if record.end_date else None,
        'status': record.status
    } for record in records]), 200

@housing.route('/occupancy', methods=['POST'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def create_occupancy():
    """Create a new room occupancy record"""
    data = request.get_json()
    occupancy = RoomOccupancy(
        room_id=data['room_id'],
        student_id=data['student_id'],
        start_date=data['start_date'],
        end_date=data.get('end_date'),
        status=data.get('status', 'active')
    )
    db.session.add(occupancy)
    db.session.commit()
    return jsonify({'message': 'Occupancy record created successfully', 'id': occupancy.id}), 201

# Maintenance Request Routes
@housing.route('/maintenance', methods=['GET'])
@jwt_required()
def get_maintenance_requests():
    """Get maintenance requests"""
    room_id = request.args.get('room_id')
    status = request.args.get('status')
    query = MaintenanceRequest.query
    if room_id:
        query = query.filter_by(room_id=room_id)
    if status:
        query = query.filter_by(status=status)
    requests = query.all()
    return jsonify([{
        'id': req.id,
        'room_id': req.room_id,
        'student_id': req.student_id,
        'request_type': req.request_type,
        'description': req.description,
        'priority': req.priority,
        'status': req.status,
        'assigned_to': req.assigned_to,
        'completion_date': req.completion_date.isoformat() if req.completion_date else None
    } for req in requests]), 200

@housing.route('/maintenance', methods=['POST'])
@jwt_required()
def create_maintenance_request():
    """Create a new maintenance request"""
    data = request.get_json()
    request = MaintenanceRequest(
        room_id=data['room_id'],
        student_id=data['student_id'],
        request_type=data['request_type'],
        description=data['description'],
        priority=data.get('priority', 'normal')
    )
    db.session.add(request)
    db.session.commit()
    return jsonify({'message': 'Maintenance request created successfully', 'id': request.id}), 201

# Room Inspection Routes
@housing.route('/inspections', methods=['GET'])
@jwt_required()
def get_inspections():
    """Get room inspections"""
    room_id = request.args.get('room_id')
    inspector_id = request.args.get('inspector_id')
    query = RoomInspection.query
    if room_id:
        query = query.filter_by(room_id=room_id)
    if inspector_id:
        query = query.filter_by(inspector_id=inspector_id)
    inspections = query.all()
    return jsonify([{
        'id': insp.id,
        'room_id': insp.room_id,
        'inspector_id': insp.inspector_id,
        'inspection_date': insp.inspection_date.isoformat(),
        'inspection_type': insp.inspection_type,
        'findings': insp.findings,
        'status': insp.status,
        'follow_up_date': insp.follow_up_date.isoformat() if insp.follow_up_date else None
    } for insp in inspections]), 200

@housing.route('/inspections', methods=['POST'])
@jwt_required()
@role_required(['admin', 'housing_manager', 'residence_staff'])
def create_inspection():
    """Create a new room inspection"""
    data = request.get_json()
    inspection = RoomInspection(
        room_id=data['room_id'],
        inspector_id=data['inspector_id'],
        inspection_date=data['inspection_date'],
        inspection_type=data['inspection_type'],
        findings=data.get('findings', {}),
        status=data.get('status', 'pending')
    )
    db.session.add(inspection)
    db.session.commit()
    return jsonify({'message': 'Inspection created successfully', 'id': inspection.id}), 201

# Housing Application Routes
@housing.route('/applications', methods=['GET'])
@jwt_required()
def get_applications():
    """Get housing applications"""
    student_id = request.args.get('student_id')
    status = request.args.get('status')
    query = HousingApplication.query
    if student_id:
        query = query.filter_by(student_id=student_id)
    if status:
        query = query.filter_by(status=status)
    applications = query.all()
    return jsonify([{
        'id': app.id,
        'student_id': app.student_id,
        'academic_year': app.academic_year,
        'semester': app.semester,
        'preferred_hall': app.preferred_hall,
        'preferred_room_type': app.preferred_room_type,
        'roommate_preferences': app.roommate_preferences,
        'special_needs': app.special_needs,
        'status': app.status
    } for app in applications]), 200

@housing.route('/applications', methods=['POST'])
@jwt_required()
def create_application():
    """Create a new housing application"""
    data = request.get_json()
    application = HousingApplication(
        student_id=data['student_id'],
        academic_year=data['academic_year'],
        semester=data['semester'],
        preferred_hall=data.get('preferred_hall'),
        preferred_room_type=data.get('preferred_room_type'),
        roommate_preferences=data.get('roommate_preferences', {}),
        special_needs=data.get('special_needs')
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({'message': 'Application created successfully', 'id': application.id}), 201

@housing.route('/applications/<int:application_id>/status', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def update_application_status(application_id):
    """Update housing application status"""
    data = request.get_json()
    application = HousingApplication.query.get_or_404(application_id)
    application.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Application status updated successfully'}), 200

@housing.route('/units', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_units():
    """Get all housing units with optional filters"""
    try:
        unit_type = request.args.get('unit_type')
        location = request.args.get('location')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = HousingUnit.query
        
        if unit_type:
            query = query.filter_by(unit_type=unit_type)
        if location:
            query = query.filter_by(location=location)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(HousingUnit.available_from >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(HousingUnit.available_until <= datetime.fromisoformat(end_date))
        
        units = query.all()
        return format_response([unit.to_dict() for unit in units])
    except Exception as e:
        return handle_exception(e)

@housing.route('/types', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_unit_types():
    """Get all unit types with optional filters"""
    try:
        name = request.args.get('name')
        capacity = request.args.get('capacity')
        status = request.args.get('status')
        
        query = UnitType.query
        
        if name:
            query = query.filter(UnitType.name.ilike(f'%{name}%'))
        if capacity:
            query = query.filter_by(capacity=capacity)
        if status:
            query = query.filter_by(status=status)
        
        types = query.all()
        return format_response([type_.to_dict() for type_ in types])
    except Exception as e:
        return handle_exception(e)

@housing.route('/bookings', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_bookings():
    """Get all unit bookings with optional filters"""
    try:
        unit_id = request.args.get('unit_id')
        student_id = request.args.get('student_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = UnitBooking.query
        
        if unit_id:
            query = query.filter_by(unit_id=unit_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(UnitBooking.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(UnitBooking.end_date <= datetime.fromisoformat(end_date))
        
        bookings = query.all()
        return format_response([booking.to_dict() for booking in bookings])
    except Exception as e:
        return handle_exception(e)

@housing.route('/maintenance', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_maintenance():
    """Get all maintenance records with optional filters"""
    try:
        unit_id = request.args.get('unit_id')
        maintenance_type = request.args.get('maintenance_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = UnitMaintenance.query
        
        if unit_id:
            query = query.filter_by(unit_id=unit_id)
        if maintenance_type:
            query = query.filter_by(maintenance_type=maintenance_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(UnitMaintenance.date_reported >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(UnitMaintenance.date_reported <= datetime.fromisoformat(end_date))
        
        maintenance = query.all()
        return format_response([record.to_dict() for record in maintenance])
    except Exception as e:
        return handle_exception(e)

@housing.route('/inventory', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_inventory():
    """Get all inventory records with optional filters"""
    try:
        unit_id = request.args.get('unit_id')
        item_type = request.args.get('item_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = UnitInventory.query
        
        if unit_id:
            query = query.filter_by(unit_id=unit_id)
        if item_type:
            query = query.filter_by(item_type=item_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(UnitInventory.acquisition_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(UnitInventory.acquisition_date <= datetime.fromisoformat(end_date))
        
        inventory = query.all()
        return format_response([item.to_dict() for item in inventory])
    except Exception as e:
        return handle_exception(e)

@housing.route('/locations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_locations():
    """Get all unit locations with optional filters"""
    try:
        location_type = request.args.get('location_type')
        status = request.args.get('status')
        
        query = UnitLocation.query
        
        if location_type:
            query = query.filter_by(location_type=location_type)
        if status:
            query = query.filter_by(status=status)
        
        locations = query.all()
        return format_response([location.to_dict() for location in locations])
    except Exception as e:
        return handle_exception(e)

@housing.route('/access', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_access():
    """Get all access records with optional filters"""
    try:
        unit_id = request.args.get('unit_id')
        student_id = request.args.get('student_id')
        access_type = request.args.get('access_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = UnitAccess.query
        
        if unit_id:
            query = query.filter_by(unit_id=unit_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if access_type:
            query = query.filter_by(access_type=access_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(UnitAccess.access_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(UnitAccess.access_date <= datetime.fromisoformat(end_date))
        
        access = query.all()
        return format_response([record.to_dict() for record in access])
    except Exception as e:
        return handle_exception(e)

@housing.route('/usage', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_usage():
    """Get all usage records with optional filters"""
    try:
        unit_id = request.args.get('unit_id')
        student_id = request.args.get('student_id')
        usage_type = request.args.get('usage_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = UnitUsage.query
        
        if unit_id:
            query = query.filter_by(unit_id=unit_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if usage_type:
            query = query.filter_by(usage_type=usage_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(UnitUsage.usage_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(UnitUsage.usage_date <= datetime.fromisoformat(end_date))
        
        usage = query.all()
        return format_response([record.to_dict() for record in usage])
    except Exception as e:
        return handle_exception(e)

@housing.route('/damage', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_damage():
    """Get all damage records with optional filters"""
    try:
        unit_id = request.args.get('unit_id')
        damage_type = request.args.get('damage_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = UnitDamage.query
        
        if unit_id:
            query = query.filter_by(unit_id=unit_id)
        if damage_type:
            query = query.filter_by(damage_type=damage_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(UnitDamage.date_reported >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(UnitDamage.date_reported <= datetime.fromisoformat(end_date))
        
        damage = query.all()
        return format_response([record.to_dict() for record in damage])
    except Exception as e:
        return handle_exception(e)

@housing.route('/reports', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_reports():
    """Get all reports with optional filters"""
    try:
        unit_id = request.args.get('unit_id')
        report_type = request.args.get('report_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = UnitReport.query
        
        if unit_id:
            query = query.filter_by(unit_id=unit_id)
        if report_type:
            query = query.filter_by(report_type=report_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(UnitReport.report_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(UnitReport.report_date <= datetime.fromisoformat(end_date))
        
        reports = query.all()
        return format_response([report.to_dict() for report in reports])
    except Exception as e:
        return handle_exception(e)

@housing.route('/payments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_payments():
    """Get all payments with optional filters"""
    try:
        unit_id = request.args.get('unit_id')
        student_id = request.args.get('student_id')
        payment_type = request.args.get('payment_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = UnitPayment.query
        
        if unit_id:
            query = query.filter_by(unit_id=unit_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if payment_type:
            query = query.filter_by(payment_type=payment_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(UnitPayment.payment_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(UnitPayment.payment_date <= datetime.fromisoformat(end_date))
        
        payments = query.all()
        return format_response([payment.to_dict() for payment in payments])
    except Exception as e:
        return handle_exception(e)

@housing.route('/allocations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_allocations():
    """Get all allocations with optional filters"""
    try:
        unit_id = request.args.get('unit_id')
        student_id = request.args.get('student_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = UnitAllocation.query
        
        if unit_id:
            query = query.filter_by(unit_id=unit_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(UnitAllocation.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(UnitAllocation.end_date <= datetime.fromisoformat(end_date))
        
        allocations = query.all()
        return format_response([allocation.to_dict() for allocation in allocations])
    except Exception as e:
        return handle_exception(e)

@housing.route('/inspections', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_inspections():
    """Get all inspections with optional filters"""
    try:
        unit_id = request.args.get('unit_id')
        inspector_id = request.args.get('inspector_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = UnitInspectionModel.query
        
        if unit_id:
            query = query.filter_by(unit_id=unit_id)
        if inspector_id:
            query = query.filter_by(inspector_id=inspector_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(UnitInspectionModel.inspection_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(UnitInspectionModel.inspection_date <= datetime.fromisoformat(end_date))
        
        inspections = query.all()
        return format_response([inspection.to_dict() for inspection in inspections])
    except Exception as e:
        return handle_exception(e)

@housing.route('/cleaning', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_cleaning():
    """Get all cleaning records with optional filters"""
    try:
        unit_id = request.args.get('unit_id')
        cleaner_id = request.args.get('cleaner_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = UnitCleaning.query
        
        if unit_id:
            query = query.filter_by(unit_id=unit_id)
        if cleaner_id:
            query = query.filter_by(cleaner_id=cleaner_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(UnitCleaning.cleaning_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(UnitCleaning.cleaning_date <= datetime.fromisoformat(end_date))
        
        cleaning = query.all()
        return format_response([record.to_dict() for record in cleaning])
    except Exception as e:
        return handle_exception(e)

@housing.route('/amenities', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_amenities():
    """Get all amenities with optional filters"""
    try:
        amenity_type = request.args.get('amenity_type')
        status = request.args.get('status')
        
        query = UnitAmenity.query
        
        if amenity_type:
            query = query.filter_by(amenity_type=amenity_type)
        if status:
            query = query.filter_by(status=status)
        
        amenities = query.all()
        return format_response([amenity.to_dict() for amenity in amenities])
    except Exception as e:
        return handle_exception(e)

@housing.route('/rules', methods=['GET'])
@jwt_required()
@role_required(['admin', 'housing_manager'])
def get_rules():
    """Get all rules with optional filters"""
    try:
        rule_type = request.args.get('rule_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = UnitRule.query
        
        if rule_type:
            query = query.filter_by(rule_type=rule_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(UnitRule.effective_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(UnitRule.effective_date <= datetime.fromisoformat(end_date))
        
        rules = query.all()
        return format_response([rule.to_dict() for rule in rules])
    except Exception as e:
        return handle_exception(e) 