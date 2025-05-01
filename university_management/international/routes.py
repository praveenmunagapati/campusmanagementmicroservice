from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    ExchangeProgram, PartnerInstitution, ExchangeApplication, VisaApplication,
    InternationalStudent, LanguageProficiency, CulturalEvent, EventRegistration
)
from .. import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

international_bp = Blueprint('international', __name__)

# Exchange Program Routes
@international_bp.route('/exchange-programs', methods=['GET'])
@jwt_required()
def get_exchange_programs():
    """Get all exchange programs"""
    programs = ExchangeProgram.query.all()
    return jsonify([program.to_dict() for program in programs])

@international_bp.route('/exchange-programs/<int:id>', methods=['GET'])
@jwt_required()
def get_exchange_program_by_id(id):
    """Get specific exchange program by ID"""
    program = ExchangeProgram.query.get_or_404(id)
    return jsonify(program.to_dict())

@international_bp.route('/exchange-programs', methods=['POST'])
@jwt_required()
@role_required(['admin', 'international'])
def create_exchange_program():
    """Create new exchange program"""
    data = request.get_json()
    new_program = ExchangeProgram(**data)
    db.session.add(new_program)
    db.session.commit()
    return jsonify(new_program.to_dict()), 201

@international_bp.route('/exchange-programs/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'international'])
def update_exchange_program(id):
    """Update existing exchange program"""
    program = ExchangeProgram.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(program, key, value)
    db.session.commit()
    return jsonify(program.to_dict())

@international_bp.route('/exchange-programs/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_exchange_program(id):
    """Delete exchange program"""
    program = ExchangeProgram.query.get_or_404(id)
    db.session.delete(program)
    db.session.commit()
    return '', 204

# Partner Institution Routes
@international_bp.route('/partner-institutions', methods=['GET'])
@jwt_required()
def get_partner_institutions():
    """Get all partner institutions"""
    institutions = PartnerInstitution.query.all()
    return jsonify([institution.to_dict() for institution in institutions])

@international_bp.route('/partner-institutions/<int:id>', methods=['GET'])
@jwt_required()
def get_partner_institution_by_id(id):
    """Get specific partner institution by ID"""
    institution = PartnerInstitution.query.get_or_404(id)
    return jsonify(institution.to_dict())

@international_bp.route('/partner-institutions', methods=['POST'])
@jwt_required()
@role_required(['admin', 'international'])
def create_partner_institution():
    """Create new partner institution"""
    data = request.get_json()
    new_institution = PartnerInstitution(**data)
    db.session.add(new_institution)
    db.session.commit()
    return jsonify(new_institution.to_dict()), 201

@international_bp.route('/partner-institutions/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'international'])
def update_partner_institution(id):
    """Update existing partner institution"""
    institution = PartnerInstitution.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(institution, key, value)
    db.session.commit()
    return jsonify(institution.to_dict())

@international_bp.route('/partner-institutions/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_partner_institution(id):
    """Delete partner institution"""
    institution = PartnerInstitution.query.get_or_404(id)
    db.session.delete(institution)
    db.session.commit()
    return '', 204

# Exchange Application Routes
@international_bp.route('/exchange-applications', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international'])
def get_exchange_applications():
    """Get all exchange applications"""
    applications = ExchangeApplication.query.all()
    return jsonify([application.to_dict() for application in applications])

@international_bp.route('/exchange-applications/<int:id>', methods=['GET'])
@jwt_required()
def get_exchange_application_by_id(id):
    """Get specific exchange application by ID"""
    application = ExchangeApplication.query.get_or_404(id)
    return jsonify(application.to_dict())

@international_bp.route('/exchange-applications', methods=['POST'])
@jwt_required()
def create_exchange_application():
    """Create new exchange application"""
    data = request.get_json()
    new_application = ExchangeApplication(**data)
    db.session.add(new_application)
    db.session.commit()
    return jsonify(new_application.to_dict()), 201

@international_bp.route('/exchange-applications/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'international'])
def update_exchange_application(id):
    """Update existing exchange application"""
    application = ExchangeApplication.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(application, key, value)
    db.session.commit()
    return jsonify(application.to_dict())

# Visa Application Routes
@international_bp.route('/visa-applications', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international'])
def get_visa_applications():
    """Get all visa applications"""
    applications = VisaApplication.query.all()
    return jsonify([application.to_dict() for application in applications])

@international_bp.route('/visa-applications/<int:id>', methods=['GET'])
@jwt_required()
def get_visa_application_by_id(id):
    """Get specific visa application by ID"""
    application = VisaApplication.query.get_or_404(id)
    return jsonify(application.to_dict())

@international_bp.route('/visa-applications', methods=['POST'])
@jwt_required()
def create_visa_application():
    """Create new visa application"""
    data = request.get_json()
    new_application = VisaApplication(**data)
    db.session.add(new_application)
    db.session.commit()
    return jsonify(new_application.to_dict()), 201

@international_bp.route('/visa-applications/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'international'])
def update_visa_application(id):
    """Update existing visa application"""
    application = VisaApplication.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(application, key, value)
    db.session.commit()
    return jsonify(application.to_dict())

# International Student Routes
@international_bp.route('/students', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international'])
def get_international_students():
    """Get all international students"""
    students = InternationalStudent.query.all()
    return jsonify([student.to_dict() for student in students])

@international_bp.route('/students/<int:id>', methods=['GET'])
@jwt_required()
def get_international_student_by_id(id):
    """Get specific international student by ID"""
    student = InternationalStudent.query.get_or_404(id)
    return jsonify(student.to_dict())

@international_bp.route('/students', methods=['POST'])
@jwt_required()
@role_required(['admin', 'international'])
def create_international_student():
    """Create new international student record"""
    data = request.get_json()
    new_student = InternationalStudent(**data)
    db.session.add(new_student)
    db.session.commit()
    return jsonify(new_student.to_dict()), 201

@international_bp.route('/students/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'international'])
def update_international_student(id):
    """Update existing international student record"""
    student = InternationalStudent.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(student, key, value)
    db.session.commit()
    return jsonify(student.to_dict())

# Language Proficiency Routes
@international_bp.route('/language-proficiencies', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international'])
def get_language_proficiencies():
    """Get all language proficiency records"""
    proficiencies = LanguageProficiency.query.all()
    return jsonify([proficiency.to_dict() for proficiency in proficiencies])

@international_bp.route('/language-proficiencies/<int:id>', methods=['GET'])
@jwt_required()
def get_language_proficiency_by_id(id):
    """Get specific language proficiency record by ID"""
    proficiency = LanguageProficiency.query.get_or_404(id)
    return jsonify(proficiency.to_dict())

@international_bp.route('/language-proficiencies', methods=['POST'])
@jwt_required()
def create_language_proficiency():
    """Create new language proficiency record"""
    data = request.get_json()
    new_proficiency = LanguageProficiency(**data)
    db.session.add(new_proficiency)
    db.session.commit()
    return jsonify(new_proficiency.to_dict()), 201

@international_bp.route('/language-proficiencies/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'international'])
def update_language_proficiency(id):
    """Update existing language proficiency record"""
    proficiency = LanguageProficiency.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(proficiency, key, value)
    db.session.commit()
    return jsonify(proficiency.to_dict())

# Cultural Event Routes
@international_bp.route('/cultural-events', methods=['GET'])
@jwt_required()
def get_cultural_events():
    """Get all cultural events"""
    events = CulturalEvent.query.all()
    return jsonify([event.to_dict() for event in events])

@international_bp.route('/cultural-events/<int:id>', methods=['GET'])
@jwt_required()
def get_cultural_event_by_id(id):
    """Get specific cultural event by ID"""
    event = CulturalEvent.query.get_or_404(id)
    return jsonify(event.to_dict())

@international_bp.route('/cultural-events', methods=['POST'])
@jwt_required()
@role_required(['admin', 'international'])
def create_cultural_event():
    """Create new cultural event"""
    data = request.get_json()
    new_event = CulturalEvent(**data)
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict()), 201

@international_bp.route('/cultural-events/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'international'])
def update_cultural_event(id):
    """Update existing cultural event"""
    event = CulturalEvent.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(event, key, value)
    db.session.commit()
    return jsonify(event.to_dict())

@international_bp.route('/cultural-events/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'international'])
def delete_cultural_event(id):
    """Delete cultural event"""
    event = CulturalEvent.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return '', 204

# Event Registration Routes
@international_bp.route('/cultural-events/<int:event_id>/registrations', methods=['GET'])
@jwt_required()
def get_event_registrations(event_id):
    """Get registrations for a cultural event"""
    registrations = EventRegistration.query.filter_by(event_id=event_id).all()
    return jsonify([registration.to_dict() for registration in registrations])

@international_bp.route('/cultural-events/<int:event_id>/register', methods=['POST'])
@jwt_required()
def register_for_event(event_id):
    """Register for a cultural event"""
    data = request.get_json()
    data['event_id'] = event_id
    new_registration = EventRegistration(**data)
    db.session.add(new_registration)
    db.session.commit()
    return jsonify(new_registration.to_dict()), 201

@international_bp.route('/cultural-events/registrations/<int:id>', methods=['PUT'])
@jwt_required()
def update_event_registration(id):
    """Update event registration"""
    registration = EventRegistration.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(registration, key, value)
    db.session.commit()
    return jsonify(registration.to_dict())

@international_bp.route('/cultural-events/registrations/<int:id>', methods=['DELETE'])
@jwt_required()
def cancel_event_registration(id):
    """Cancel event registration"""
    registration = EventRegistration.query.get_or_404(id)
    db.session.delete(registration)
    db.session.commit()
    return '', 204 