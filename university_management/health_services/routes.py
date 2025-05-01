from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db
from .models import HealthStaff, Appointment, MedicalRecord, Prescription, HealthReport, HealthEquipment, HealthInventory, Patient, Immunization, Allergy, TestResult, Treatment, Staff, Facility, Insurance, EmergencyContact, Service, ServiceType, ServiceProvider, ServiceBooking, ServicePayment, ServiceFeedback, ServiceReport, ServicePolicy, ServiceResource, ServiceStaff, ServiceFacility, ServiceEquipment, ServiceInventory, ServiceLocation, ServiceSchedule
from ..auth.models import User
from ..auth.utils import role_required
from datetime import datetime
from utils import validate_request, format_response, log_activity, handle_exception

health_bp = Blueprint('health', __name__)

# Health Staff Routes
@health_bp.route('/staff', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_staff'])
def get_health_staff():
    """Get all health staff with optional filters"""
    try:
        staff_type = request.args.get('staff_type')
        status = request.args.get('status')
        
        query = HealthStaff.query
        
        if staff_type:
            query = query.filter_by(staff_type=staff_type)
        if status:
            query = query.filter_by(status=status)
        
        staff = query.all()
        return format_response([{
            'id': s.id,
            'user_id': s.user_id,
            'staff_type': s.staff_type,
            'specialization': s.specialization,
            'license_number': s.license_number,
            'license_expiry': s.license_expiry.isoformat(),
            'status': s.status
        } for s in staff])
    except Exception as e:
        return handle_exception(e)

@health_bp.route('/staff', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_health_staff():
    data = request.get_json()
    staff = HealthStaff(
        user_id=data['user_id'],
        staff_type=data['staff_type'],
        specialization=data.get('specialization'),
        license_number=data['license_number'],
        license_expiry=datetime.fromisoformat(data['license_expiry']).date(),
        status=data.get('status', 'active')
    )
    db.session.add(staff)
    db.session.commit()
    return jsonify({'message': 'Health staff created successfully', 'id': staff.id}), 201

# Appointment Routes
@health_bp.route('/appointments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_staff'])
def get_appointments():
    """Get all appointments with optional filters"""
    try:
        patient_id = request.args.get('patient_id')
        staff_id = request.args.get('staff_id')
        appointment_type = request.args.get('appointment_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Appointment.query
        
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        if staff_id:
            query = query.filter_by(staff_id=staff_id)
        if appointment_type:
            query = query.filter_by(appointment_type=appointment_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Appointment.scheduled_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Appointment.scheduled_date <= datetime.fromisoformat(end_date))
        
        appointments = query.all()
        return format_response([{
            'id': a.id,
            'patient_id': a.patient_id,
            'staff_id': a.staff_id,
            'appointment_type': a.appointment_type,
            'scheduled_date': a.scheduled_date.isoformat(),
            'status': a.status,
            'notes': a.notes
        } for a in appointments])
    except Exception as e:
        return handle_exception(e)

@health_bp.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()
    appointment = Appointment(
        patient_id=get_jwt_identity(),
        staff_id=data['staff_id'],
        appointment_type=data['appointment_type'],
        scheduled_date=datetime.fromisoformat(data['scheduled_date']),
        status=data.get('status', 'scheduled'),
        notes=data.get('notes')
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment created successfully', 'id': appointment.id}), 201

# Medical Record Routes
@health_bp.route('/medical-records', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_staff'])
def get_medical_records():
    """Get all medical records with optional filters"""
    try:
        patient_id = request.args.get('patient_id')
        record_type = request.args.get('record_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = MedicalRecord.query
        
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        if record_type:
            query = query.filter_by(record_type=record_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(MedicalRecord.follow_up_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(MedicalRecord.follow_up_date <= datetime.fromisoformat(end_date))
        
        records = query.all()
        return format_response([{
            'id': r.id,
            'patient_id': r.patient_id,
            'appointment_id': r.appointment_id,
            'diagnosis': r.diagnosis,
            'treatment': r.treatment,
            'notes': r.notes,
            'follow_up_date': r.follow_up_date.isoformat() if r.follow_up_date else None,
            'status': r.status
        } for r in records])
    except Exception as e:
        return handle_exception(e)

@health_bp.route('/medical-records', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_medical_record():
    data = request.get_json()
    record = MedicalRecord(
        patient_id=data['patient_id'],
        appointment_id=data['appointment_id'],
        diagnosis=data['diagnosis'],
        treatment=data.get('treatment'),
        notes=data.get('notes'),
        follow_up_date=datetime.fromisoformat(data['follow_up_date']) if data.get('follow_up_date') else None,
        status=data.get('status', 'active')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Medical record created successfully', 'id': record.id}), 201

# Prescription Routes
@health_bp.route('/prescriptions', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_staff'])
def get_prescriptions():
    """Get all prescriptions with optional filters"""
    try:
        patient_id = request.args.get('patient_id')
        staff_id = request.args.get('staff_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Prescription.query
        
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        if staff_id:
            query = query.filter_by(staff_id=staff_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Prescription.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Prescription.date <= datetime.fromisoformat(end_date))
        
        prescriptions = query.all()
        return format_response([{
            'id': p.id,
            'medical_record_id': p.medical_record_id,
            'staff_id': p.staff_id,
            'medication': p.medication,
            'dosage': p.dosage,
            'frequency': p.frequency,
            'duration': p.duration,
            'instructions': p.instructions,
            'status': p.status
        } for p in prescriptions])
    except Exception as e:
        return handle_exception(e)

@health_bp.route('/prescriptions', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_prescription():
    data = request.get_json()
    prescription = Prescription(
        medical_record_id=data['medical_record_id'],
        staff_id=get_jwt_identity(),
        medication=data['medication'],
        dosage=data['dosage'],
        frequency=data['frequency'],
        duration=data['duration'],
        instructions=data.get('instructions'),
        status=data.get('status', 'active')
    )
    db.session.add(prescription)
    db.session.commit()
    return jsonify({'message': 'Prescription created successfully', 'id': prescription.id}), 201

# Health Equipment Routes
@health_bp.route('/equipment', methods=['GET'])
@jwt_required()
def get_health_equipment():
    equipment = HealthEquipment.query.all()
    return jsonify([{
        'id': e.id,
        'name': e.name,
        'equipment_type': e.equipment_type,
        'serial_number': e.serial_number,
        'purchase_date': e.purchase_date.isoformat(),
        'last_maintenance': e.last_maintenance.isoformat() if e.last_maintenance else None,
        'next_maintenance': e.next_maintenance.isoformat() if e.next_maintenance else None,
        'status': e.status
    } for e in equipment]), 200

@health_bp.route('/equipment', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_health_equipment():
    data = request.get_json()
    equipment = HealthEquipment(
        name=data['name'],
        equipment_type=data['equipment_type'],
        serial_number=data['serial_number'],
        purchase_date=datetime.fromisoformat(data['purchase_date']).date(),
        last_maintenance=datetime.fromisoformat(data['last_maintenance']) if data.get('last_maintenance') else None,
        next_maintenance=datetime.fromisoformat(data['next_maintenance']) if data.get('next_maintenance') else None,
        status=data.get('status', 'active')
    )
    db.session.add(equipment)
    db.session.commit()
    return jsonify({'message': 'Health equipment created successfully', 'id': equipment.id}), 201

# Health Inventory Routes
@health_bp.route('/inventory', methods=['GET'])
@jwt_required()
def get_health_inventory():
    inventory = HealthInventory.query.all()
    return jsonify([{
        'id': i.id,
        'item_name': i.item_name,
        'item_type': i.item_type,
        'quantity': i.quantity,
        'unit': i.unit,
        'expiry_date': i.expiry_date.isoformat() if i.expiry_date else None,
        'status': i.status
    } for i in inventory]), 200

@health_bp.route('/inventory', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_health_inventory():
    data = request.get_json()
    inventory = HealthInventory(
        item_name=data['item_name'],
        item_type=data['item_type'],
        quantity=data['quantity'],
        unit=data['unit'],
        expiry_date=datetime.fromisoformat(data['expiry_date']).date() if data.get('expiry_date') else None,
        status=data.get('status', 'active')
    )
    db.session.add(inventory)
    db.session.commit()
    return jsonify({'message': 'Health inventory item created successfully', 'id': inventory.id}), 201

# Health Report Routes
@health_bp.route('/reports', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health'])
def get_health_reports():
    reports = HealthReport.query.all()
    return jsonify([{
        'id': r.id,
        'report_type': r.report_type,
        'patient_id': r.patient_id,
        'content': r.content,
        'created_by': r.created_by,
        'created_at': r.created_at.isoformat(),
        'status': r.status
    } for r in reports]), 200

@health_bp.route('/reports', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_health_report():
    data = request.get_json()
    report = HealthReport(
        report_type=data['report_type'],
        patient_id=data['patient_id'],
        content=data['content'],
        created_by=get_jwt_identity(),
        status=data.get('status', 'draft')
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({'message': 'Health report created successfully', 'id': report.id}), 201

@health_bp.route('/patients', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_staff'])
def get_patients():
    """Get all patients with optional filters"""
    try:
        patient_type = request.args.get('patient_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Patient.query
        
        if patient_type:
            query = query.filter_by(patient_type=patient_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Patient.registration_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Patient.registration_date <= datetime.fromisoformat(end_date))
        
        patients = query.all()
        return format_response([patient.to_dict() for patient in patients])
    except Exception as e:
        return handle_exception(e)

@health_bp.route('/immunizations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_staff'])
def get_immunizations():
    """Get all immunizations with optional filters"""
    try:
        patient_id = request.args.get('patient_id')
        vaccine_type = request.args.get('vaccine_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Immunization.query
        
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        if vaccine_type:
            query = query.filter_by(vaccine_type=vaccine_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Immunization.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Immunization.date <= datetime.fromisoformat(end_date))
        
        immunizations = query.all()
        return format_response([immunization.to_dict() for immunization in immunizations])
    except Exception as e:
        return handle_exception(e)

@health_bp.route('/allergies', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_staff'])
def get_allergies():
    """Get all allergies with optional filters"""
    try:
        patient_id = request.args.get('patient_id')
        allergy_type = request.args.get('allergy_type')
        severity = request.args.get('severity')
        
        query = Allergy.query
        
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        if allergy_type:
            query = query.filter_by(allergy_type=allergy_type)
        if severity:
            query = query.filter_by(severity=severity)
        
        allergies = query.all()
        return format_response([allergy.to_dict() for allergy in allergies])
    except Exception as e:
        return handle_exception(e)

@health_bp.route('/test-results', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_staff'])
def get_test_results():
    """Get all test results with optional filters"""
    try:
        patient_id = request.args.get('patient_id')
        test_type = request.args.get('test_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = TestResult.query
        
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        if test_type:
            query = query.filter_by(test_type=test_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(TestResult.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(TestResult.date <= datetime.fromisoformat(end_date))
        
        results = query.all()
        return format_response([result.to_dict() for result in results])
    except Exception as e:
        return handle_exception(e)

@health_bp.route('/treatments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_staff'])
def get_treatments():
    """Get all treatments with optional filters"""
    try:
        patient_id = request.args.get('patient_id')
        treatment_type = request.args.get('treatment_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Treatment.query
        
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        if treatment_type:
            query = query.filter_by(treatment_type=treatment_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Treatment.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Treatment.end_date <= datetime.fromisoformat(end_date))
        
        treatments = query.all()
        return format_response([treatment.to_dict() for treatment in treatments])
    except Exception as e:
        return handle_exception(e)

@health_bp.route('/facilities', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_staff'])
def get_facilities():
    """Get all health facilities with optional filters"""
    try:
        facility_type = request.args.get('facility_type')
        status = request.args.get('status')
        
        query = Facility.query
        
        if facility_type:
            query = query.filter_by(facility_type=facility_type)
        if status:
            query = query.filter_by(status=status)
        
        facilities = query.all()
        return format_response([facility.to_dict() for facility in facilities])
    except Exception as e:
        return handle_exception(e)

@health_bp.route('/insurance', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_staff'])
def get_insurance():
    """Get all insurance records with optional filters"""
    try:
        patient_id = request.args.get('patient_id')
        insurance_type = request.args.get('insurance_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Insurance.query
        
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        if insurance_type:
            query = query.filter_by(insurance_type=insurance_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Insurance.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Insurance.end_date <= datetime.fromisoformat(end_date))
        
        insurance_records = query.all()
        return format_response([record.to_dict() for record in insurance_records])
    except Exception as e:
        return handle_exception(e)

@health_bp.route('/emergency-contacts', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_staff'])
def get_emergency_contacts():
    """Get all emergency contacts with optional filters"""
    try:
        patient_id = request.args.get('patient_id')
        relationship = request.args.get('relationship')
        status = request.args.get('status')
        
        query = EmergencyContact.query
        
        if patient_id:
            query = query.filter_by(patient_id=patient_id)
        if relationship:
            query = query.filter_by(relationship=relationship)
        if status:
            query = query.filter_by(status=status)
        
        contacts = query.all()
        return format_response([contact.to_dict() for contact in contacts])
    except Exception as e:
        return handle_exception(e)

health_services_bp = Blueprint('health_services', __name__)

@health_services_bp.route('/services', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_services_manager'])
def get_services():
    """Get all health services with optional filters"""
    try:
        service_type = request.args.get('service_type')
        provider_id = request.args.get('provider_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Service.query
        
        if service_type:
            query = query.filter_by(service_type=service_type)
        if provider_id:
            query = query.filter_by(provider_id=provider_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Service.available_from >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Service.available_until <= datetime.fromisoformat(end_date))
        
        services = query.all()
        return format_response([service.to_dict() for service in services])
    except Exception as e:
        return handle_exception(e)

@health_services_bp.route('/types', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_services_manager'])
def get_service_types():
    """Get all service types with optional filters"""
    try:
        name = request.args.get('name')
        category = request.args.get('category')
        status = request.args.get('status')
        
        query = ServiceType.query
        
        if name:
            query = query.filter(ServiceType.name.ilike(f'%{name}%'))
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        
        types = query.all()
        return format_response([type_.to_dict() for type_ in types])
    except Exception as e:
        return handle_exception(e)

@health_services_bp.route('/providers', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_services_manager'])
def get_providers():
    """Get all service providers with optional filters"""
    try:
        provider_type = request.args.get('provider_type')
        specialty = request.args.get('specialty')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ServiceProvider.query
        
        if provider_type:
            query = query.filter_by(provider_type=provider_type)
        if specialty:
            query = query.filter_by(specialty=specialty)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ServiceProvider.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ServiceProvider.end_date <= datetime.fromisoformat(end_date))
        
        providers = query.all()
        return format_response([provider.to_dict() for provider in providers])
    except Exception as e:
        return handle_exception(e)

@health_services_bp.route('/bookings', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_services_manager'])
def get_bookings():
    """Get all service bookings with optional filters"""
    try:
        service_id = request.args.get('service_id')
        student_id = request.args.get('student_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ServiceBooking.query
        
        if service_id:
            query = query.filter_by(service_id=service_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ServiceBooking.booking_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ServiceBooking.booking_date <= datetime.fromisoformat(end_date))
        
        bookings = query.all()
        return format_response([booking.to_dict() for booking in bookings])
    except Exception as e:
        return handle_exception(e)

@health_services_bp.route('/payments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health_services_manager'])
def get_payments():
    """Get all service payments with optional filters"""
    try:
        service_id = request.args.get('service_id')
        student_id = request.args.get('student_id')
        payment_type = request.args.get('payment_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ServicePayment.query
        
        if service_id:
            query = query.filter_by(service_id=service_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if payment_type:
            query = query.filter_by(payment_type=payment_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ServicePayment.payment_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ServicePayment.payment_date <= datetime.fromisoformat(end_date))
        
        payments = query.all()
        return format_response([payment.to_dict() for payment in payments])
    except Exception as e:
        return handle_exception(e) 