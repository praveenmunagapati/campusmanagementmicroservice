from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from .models import (
    ResidenceHall, Room, RoomOccupancy, 
    ResidenceStaff, MaintenanceRequest, 
    RoomInspection, HousingApplication
)
from ..utils import role_required

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