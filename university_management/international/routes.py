from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    ExchangeProgram, PartnerInstitution, ExchangeApplication, VisaApplication,
    InternationalStudent, LanguageProficiency, CulturalEvent, EventRegistration,
    InternationalEvent, StudyAbroad, InternationalPartnership, ImmigrationDocument,
    InternationalScholarship, LanguageProgram, InternationalAlumni, InternationalStaff,
    InternationalOffice, InternationalAgreement, InternationalConference, InternationalResearch
)
from .. import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception
import json

international_bp = Blueprint('international', __name__)

# Exchange Program Routes
@international_bp.route('/exchange-programs', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international_office'])
def get_exchange_programs():
    """Get all exchange programs with optional filters"""
    try:
        program_type = request.args.get('program_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ExchangeProgram.query
        
        if program_type:
            query = query.filter_by(program_type=program_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ExchangeProgram.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ExchangeProgram.end_date <= datetime.fromisoformat(end_date))
        
        programs = query.all()
        return format_response([program.to_dict() for program in programs])
    except Exception as e:
        return handle_exception(e)

@international_bp.route('/exchange-programs/<int:id>', methods=['GET'])
@jwt_required()
def get_exchange_program_by_id(id):
    """Get specific exchange program by ID"""
    program = ExchangeProgram.query.get_or_404(id)
    return jsonify({
        'status': 'success',
        'data': program.to_dict()
    }), 200

@international_bp.route('/exchange-programs', methods=['POST'])
@jwt_required()
@role_required(['admin', 'international'])
def create_exchange_program():
    """Create new exchange program"""
    data = request.get_json()
    
    program = ExchangeProgram(
        name=data['name'],
        partner_institution=data['partner_institution'],
        country=data['country'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
        capacity=data['capacity'],
        requirements=data.get('requirements')
    )
    
    db.session.add(program)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': program.to_dict()
    }), 201

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
    return jsonify({
        'status': 'success',
        'data': [app.to_dict() for app in applications]
    }), 200

@international_bp.route('/exchange-applications/<int:id>', methods=['GET'])
@jwt_required()
def get_exchange_application_by_id(id):
    """Get specific exchange application by ID"""
    application = ExchangeApplication.query.get_or_404(id)
    return jsonify({
        'status': 'success',
        'data': application.to_dict()
    }), 200

@international_bp.route('/exchange-applications', methods=['POST'])
@jwt_required()
def create_exchange_application():
    """Create new exchange application"""
    data = request.get_json()
    
    application = ExchangeApplication(
        student_id=data['student_id'],
        program_id=data['program_id'],
        application_date=datetime.strptime(data['application_date'], '%Y-%m-%d').date(),
        documents=json.dumps(data.get('documents', [])),
        notes=data.get('notes')
    )
    
    db.session.add(application)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': application.to_dict()
    }), 201

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
@role_required(['admin', 'international_office'])
def get_visa_applications():
    """Get all visa applications with optional filters"""
    try:
        visa_type = request.args.get('visa_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = VisaApplication.query
        
        if visa_type:
            query = query.filter_by(visa_type=visa_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(VisaApplication.application_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(VisaApplication.application_date <= datetime.fromisoformat(end_date))
        
        applications = query.all()
        return format_response([application.to_dict() for application in applications])
    except Exception as e:
        return handle_exception(e)

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
@role_required(['admin', 'international_office'])
def get_international_students():
    """Get all international students with optional filters"""
    try:
        country = request.args.get('country')
        program = request.args.get('program')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = InternationalStudent.query
        
        if country:
            query = query.filter_by(country=country)
        if program:
            query = query.filter_by(program=program)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(InternationalStudent.enrollment_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(InternationalStudent.enrollment_date <= datetime.fromisoformat(end_date))
        
        students = query.all()
        return format_response([student.to_dict() for student in students])
    except Exception as e:
        return handle_exception(e)

@international_bp.route('/students/<int:id>', methods=['GET'])
@jwt_required()
def get_international_student_by_id(id):
    """Get specific international student by ID"""
    student = InternationalStudent.query.get_or_404(id)
    return jsonify({
        'status': 'success',
        'data': student.to_dict()
    }), 200

@international_bp.route('/students', methods=['POST'])
@jwt_required()
@role_required(['admin', 'international'])
def create_international_student():
    """Create new international student record"""
    data = request.get_json()
    
    student = InternationalStudent(
        student_id=data['student_id'],
        passport_number=data['passport_number'],
        visa_type=data['visa_type'],
        visa_expiry_date=datetime.strptime(data['visa_expiry_date'], '%Y-%m-%d').date(),
        country_of_origin=data['country_of_origin'],
        language_proficiency=data.get('language_proficiency'),
        arrival_date=datetime.strptime(data['arrival_date'], '%Y-%m-%d').date()
    )
    
    db.session.add(student)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': student.to_dict()
    }), 201

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
@role_required(['admin', 'international_office'])
def get_cultural_events():
    """Get all cultural events with optional filters"""
    try:
        event_type = request.args.get('event_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CulturalEvent.query
        
        if event_type:
            query = query.filter_by(event_type=event_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(CulturalEvent.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CulturalEvent.end_date <= datetime.fromisoformat(end_date))
        
        events = query.all()
        return format_response([event.to_dict() for event in events])
    except Exception as e:
        return handle_exception(e)

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

# International Event Routes
@international_bp.route('/international-events', methods=['GET'])
@jwt_required()
def get_international_events():
    """Get all international events"""
    events = InternationalEvent.query.all()
    return jsonify({
        'status': 'success',
        'data': [event.to_dict() for event in events]
    }), 200

@international_bp.route('/international-events/<int:id>', methods=['GET'])
@jwt_required()
def get_international_event(id):
    """Get a specific international event"""
    event = InternationalEvent.query.get_or_404(id)
    return jsonify({
        'status': 'success',
        'data': event.to_dict()
    }), 200

@international_bp.route('/international-events', methods=['POST'])
@jwt_required()
def create_international_event():
    """Create a new international event"""
    data = request.get_json()
    
    event = InternationalEvent(
        title=data['title'],
        description=data.get('description'),
        event_date=datetime.strptime(data['event_date'], '%Y-%m-%dT%H:%M:%S'),
        location=data.get('location'),
        target_audience=data.get('target_audience'),
        registration_link=data.get('registration_link')
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': event.to_dict()
    }), 201

# Study Abroad Routes
@international_bp.route('/study-abroad', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international_office'])
def get_study_abroad():
    """Get all study abroad programs with optional filters"""
    try:
        destination = request.args.get('destination')
        program_type = request.args.get('program_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = StudyAbroad.query
        
        if destination:
            query = query.filter_by(destination=destination)
        if program_type:
            query = query.filter_by(program_type=program_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(StudyAbroad.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(StudyAbroad.end_date <= datetime.fromisoformat(end_date))
        
        programs = query.all()
        return format_response([program.to_dict() for program in programs])
    except Exception as e:
        return handle_exception(e)

# International Partnership Routes
@international_bp.route('/partnerships', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international_office'])
def get_international_partnerships():
    """Get all international partnerships with optional filters"""
    try:
        partner_type = request.args.get('partner_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = InternationalPartnership.query
        
        if partner_type:
            query = query.filter_by(partner_type=partner_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(InternationalPartnership.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(InternationalPartnership.end_date <= datetime.fromisoformat(end_date))
        
        partnerships = query.all()
        return format_response([partnership.to_dict() for partnership in partnerships])
    except Exception as e:
        return handle_exception(e)

# Immigration Document Routes
@international_bp.route('/documents', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international_office'])
def get_immigration_documents():
    """Get all immigration documents with optional filters"""
    try:
        document_type = request.args.get('document_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ImmigrationDocument.query
        
        if document_type:
            query = query.filter_by(document_type=document_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ImmigrationDocument.issue_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ImmigrationDocument.issue_date <= datetime.fromisoformat(end_date))
        
        documents = query.all()
        return format_response([document.to_dict() for document in documents])
    except Exception as e:
        return handle_exception(e)

# International Scholarship Routes
@international_bp.route('/scholarships', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international_office'])
def get_international_scholarships():
    """Get all international scholarships with optional filters"""
    try:
        scholarship_type = request.args.get('scholarship_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = InternationalScholarship.query
        
        if scholarship_type:
            query = query.filter_by(scholarship_type=scholarship_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(InternationalScholarship.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(InternationalScholarship.end_date <= datetime.fromisoformat(end_date))
        
        scholarships = query.all()
        return format_response([scholarship.to_dict() for scholarship in scholarships])
    except Exception as e:
        return handle_exception(e)

# Language Program Routes
@international_bp.route('/language-programs', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international_office'])
def get_language_programs():
    """Get all language programs with optional filters"""
    try:
        language = request.args.get('language')
        program_type = request.args.get('program_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = LanguageProgram.query
        
        if language:
            query = query.filter_by(language=language)
        if program_type:
            query = query.filter_by(program_type=program_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(LanguageProgram.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(LanguageProgram.end_date <= datetime.fromisoformat(end_date))
        
        programs = query.all()
        return format_response([program.to_dict() for program in programs])
    except Exception as e:
        return handle_exception(e)

# International Alumni Routes
@international_bp.route('/alumni', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international_office'])
def get_international_alumni():
    """Get all international alumni with optional filters"""
    try:
        country = request.args.get('country')
        program = request.args.get('program')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = InternationalAlumni.query
        
        if country:
            query = query.filter_by(country=country)
        if program:
            query = query.filter_by(program=program)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(InternationalAlumni.graduation_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(InternationalAlumni.graduation_date <= datetime.fromisoformat(end_date))
        
        alumni = query.all()
        return format_response([alumnus.to_dict() for alumnus in alumni])
    except Exception as e:
        return handle_exception(e)

# International Staff Routes
@international_bp.route('/staff', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international_office'])
def get_international_staff():
    """Get all international staff with optional filters"""
    try:
        role = request.args.get('role')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = InternationalStaff.query
        
        if role:
            query = query.filter_by(role=role)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(InternationalStaff.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(InternationalStaff.start_date <= datetime.fromisoformat(end_date))
        
        staff = query.all()
        return format_response([member.to_dict() for member in staff])
    except Exception as e:
        return handle_exception(e)

# International Office Routes
@international_bp.route('/offices', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international_office'])
def get_international_offices():
    """Get all international offices with optional filters"""
    try:
        office_type = request.args.get('office_type')
        status = request.args.get('status')
        
        query = InternationalOffice.query
        
        if office_type:
            query = query.filter_by(office_type=office_type)
        if status:
            query = query.filter_by(status=status)
        
        offices = query.all()
        return format_response([office.to_dict() for office in offices])
    except Exception as e:
        return handle_exception(e)

# International Agreement Routes
@international_bp.route('/agreements', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international_office'])
def get_international_agreements():
    """Get all international agreements with optional filters"""
    try:
        agreement_type = request.args.get('agreement_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = InternationalAgreement.query
        
        if agreement_type:
            query = query.filter_by(agreement_type=agreement_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(InternationalAgreement.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(InternationalAgreement.end_date <= datetime.fromisoformat(end_date))
        
        agreements = query.all()
        return format_response([agreement.to_dict() for agreement in agreements])
    except Exception as e:
        return handle_exception(e)

# International Conference Routes
@international_bp.route('/conferences', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international_office'])
def get_international_conferences():
    """Get all international conferences with optional filters"""
    try:
        conference_type = request.args.get('conference_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = InternationalConference.query
        
        if conference_type:
            query = query.filter_by(conference_type=conference_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(InternationalConference.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(InternationalConference.end_date <= datetime.fromisoformat(end_date))
        
        conferences = query.all()
        return format_response([conference.to_dict() for conference in conferences])
    except Exception as e:
        return handle_exception(e)

# International Research Routes
@international_bp.route('/research', methods=['GET'])
@jwt_required()
@role_required(['admin', 'international_office'])
def get_international_research():
    """Get all international research collaborations with optional filters"""
    try:
        research_type = request.args.get('research_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = InternationalResearch.query
        
        if research_type:
            query = query.filter_by(research_type=research_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(InternationalResearch.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(InternationalResearch.end_date <= datetime.fromisoformat(end_date))
        
        research = query.all()
        return format_response([item.to_dict() for item in research])
    except Exception as e:
        return handle_exception(e) 