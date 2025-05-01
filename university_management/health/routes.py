from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    MedicalRecord, Appointment, HealthService, Visit,
    Immunization, HealthAlert
)
from .. import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

health_bp = Blueprint('health', __name__)

# Medical Record Routes
@health_bp.route('/medical-records', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health'])
def get_medical_records():
    """Get all medical records"""
    records = MedicalRecord.query.all()
    return jsonify([record.to_dict() for record in records])

@health_bp.route('/medical-records/<int:id>', methods=['GET'])
@jwt_required()
def get_medical_record_by_id(id):
    """Get specific medical record by ID"""
    record = MedicalRecord.query.get_or_404(id)
    return jsonify(record.to_dict())

@health_bp.route('/medical-records', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_medical_record():
    """Create new medical record"""
    data = request.get_json()
    new_record = MedicalRecord(**data)
    db.session.add(new_record)
    db.session.commit()
    return jsonify(new_record.to_dict()), 201

@health_bp.route('/medical-records/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'health'])
def update_medical_record(id):
    """Update existing medical record"""
    record = MedicalRecord.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(record, key, value)
    db.session.commit()
    return jsonify(record.to_dict())

# Appointment Routes
@health_bp.route('/appointments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health'])
def get_appointments():
    """Get all appointments"""
    appointments = Appointment.query.all()
    return jsonify([appointment.to_dict() for appointment in appointments])

@health_bp.route('/appointments/<int:id>', methods=['GET'])
@jwt_required()
def get_appointment_by_id(id):
    """Get specific appointment by ID"""
    appointment = Appointment.query.get_or_404(id)
    return jsonify(appointment.to_dict())

@health_bp.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    """Create new appointment"""
    data = request.get_json()
    new_appointment = Appointment(**data)
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify(new_appointment.to_dict()), 201

@health_bp.route('/appointments/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'health'])
def update_appointment(id):
    """Update existing appointment"""
    appointment = Appointment.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(appointment, key, value)
    db.session.commit()
    return jsonify(appointment.to_dict())

@health_bp.route('/appointments/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'health'])
def delete_appointment(id):
    """Delete appointment"""
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return '', 204

# Health Service Routes
@health_bp.route('/services', methods=['GET'])
@jwt_required()
def get_health_services():
    """Get all health services"""
    services = HealthService.query.all()
    return jsonify([service.to_dict() for service in services])

@health_bp.route('/services/<int:id>', methods=['GET'])
@jwt_required()
def get_health_service_by_id(id):
    """Get specific health service by ID"""
    service = HealthService.query.get_or_404(id)
    return jsonify(service.to_dict())

@health_bp.route('/services', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_health_service():
    """Create new health service"""
    data = request.get_json()
    new_service = HealthService(**data)
    db.session.add(new_service)
    db.session.commit()
    return jsonify(new_service.to_dict()), 201

@health_bp.route('/services/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'health'])
def update_health_service(id):
    """Update existing health service"""
    service = HealthService.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(service, key, value)
    db.session.commit()
    return jsonify(service.to_dict())

@health_bp.route('/services/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_health_service(id):
    """Delete health service"""
    service = HealthService.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return '', 204

# Visit Routes
@health_bp.route('/visits', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health'])
def get_visits():
    """Get all visits"""
    visits = Visit.query.all()
    return jsonify([visit.to_dict() for visit in visits])

@health_bp.route('/visits/<int:id>', methods=['GET'])
@jwt_required()
def get_visit_by_id(id):
    """Get specific visit by ID"""
    visit = Visit.query.get_or_404(id)
    return jsonify(visit.to_dict())

@health_bp.route('/visits', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_visit():
    """Create new visit"""
    data = request.get_json()
    new_visit = Visit(**data)
    db.session.add(new_visit)
    db.session.commit()
    return jsonify(new_visit.to_dict()), 201

@health_bp.route('/visits/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'health'])
def update_visit(id):
    """Update existing visit"""
    visit = Visit.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(visit, key, value)
    db.session.commit()
    return jsonify(visit.to_dict())

# Immunization Routes
@health_bp.route('/immunizations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health'])
def get_immunizations():
    """Get all immunizations"""
    immunizations = Immunization.query.all()
    return jsonify([immunization.to_dict() for immunization in immunizations])

@health_bp.route('/immunizations/<int:id>', methods=['GET'])
@jwt_required()
def get_immunization_by_id(id):
    """Get specific immunization by ID"""
    immunization = Immunization.query.get_or_404(id)
    return jsonify(immunization.to_dict())

@health_bp.route('/immunizations', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_immunization():
    """Create new immunization record"""
    data = request.get_json()
    new_immunization = Immunization(**data)
    db.session.add(new_immunization)
    db.session.commit()
    return jsonify(new_immunization.to_dict()), 201

@health_bp.route('/immunizations/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'health'])
def update_immunization(id):
    """Update existing immunization record"""
    immunization = Immunization.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(immunization, key, value)
    db.session.commit()
    return jsonify(immunization.to_dict())

@health_bp.route('/immunizations/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'health'])
def delete_immunization(id):
    """Delete immunization record"""
    immunization = Immunization.query.get_or_404(id)
    db.session.delete(immunization)
    db.session.commit()
    return '', 204

# Health Alert Routes
@health_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_health_alerts():
    """Get all health alerts"""
    alerts = HealthAlert.query.all()
    return jsonify([alert.to_dict() for alert in alerts])

@health_bp.route('/alerts/<int:id>', methods=['GET'])
@jwt_required()
def get_health_alert_by_id(id):
    """Get specific health alert by ID"""
    alert = HealthAlert.query.get_or_404(id)
    return jsonify(alert.to_dict())

@health_bp.route('/alerts', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_health_alert():
    """Create new health alert"""
    data = request.get_json()
    new_alert = HealthAlert(**data)
    db.session.add(new_alert)
    db.session.commit()
    return jsonify(new_alert.to_dict()), 201

@health_bp.route('/alerts/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'health'])
def update_health_alert(id):
    """Update existing health alert"""
    alert = HealthAlert.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(alert, key, value)
    db.session.commit()
    return jsonify(alert.to_dict())

@health_bp.route('/alerts/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'health'])
def delete_health_alert(id):
    """Delete health alert"""
    alert = HealthAlert.query.get_or_404(id)
    db.session.delete(alert)
    db.session.commit()
    return '', 204 