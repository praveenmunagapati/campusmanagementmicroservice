from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    CounselingSession, SessionType, SessionCategory,
    Counselor, Appointment, Assessment,
    Resource, Workshop, GroupSession,
    Feedback, Report, Policy,
    Location, Contact, Emergency
)
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

counseling_bp = Blueprint('counseling', __name__)

@counseling_bp.route('/sessions', methods=['GET'])
@jwt_required()
@role_required(['admin', 'counseling_manager'])
def get_sessions():
    """Get all counseling sessions with optional filters"""
    try:
        session_type = request.args.get('session_type')
        category = request.args.get('category')
        counselor_id = request.args.get('counselor_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CounselingSession.query
        
        if session_type:
            query = query.filter_by(session_type=session_type)
        if category:
            query = query.filter_by(category=category)
        if counselor_id:
            query = query.filter_by(counselor_id=counselor_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(CounselingSession.session_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CounselingSession.session_date <= datetime.fromisoformat(end_date))
        
        sessions = query.all()
        return format_response([session.to_dict() for session in sessions])
    except Exception as e:
        return handle_exception(e)

@counseling_bp.route('/types', methods=['GET'])
@jwt_required()
@role_required(['admin', 'counseling_manager'])
def get_session_types():
    """Get all session types with optional filters"""
    try:
        name = request.args.get('name')
        category = request.args.get('category')
        status = request.args.get('status')
        
        query = SessionType.query
        
        if name:
            query = query.filter(SessionType.name.ilike(f'%{name}%'))
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        
        types = query.all()
        return format_response([type_.to_dict() for type_ in types])
    except Exception as e:
        return handle_exception(e)

@counseling_bp.route('/categories', methods=['GET'])
@jwt_required()
@role_required(['admin', 'counseling_manager'])
def get_categories():
    """Get all session categories with optional filters"""
    try:
        name = request.args.get('name')
        parent_category = request.args.get('parent_category')
        status = request.args.get('status')
        
        query = SessionCategory.query
        
        if name:
            query = query.filter(SessionCategory.name.ilike(f'%{name}%'))
        if parent_category:
            query = query.filter_by(parent_category=parent_category)
        if status:
            query = query.filter_by(status=status)
        
        categories = query.all()
        return format_response([category.to_dict() for category in categories])
    except Exception as e:
        return handle_exception(e)

@counseling_bp.route('/counselors', methods=['GET'])
@jwt_required()
@role_required(['admin', 'counseling_manager'])
def get_counselors():
    """Get all counselors with optional filters"""
    try:
        counselor_type = request.args.get('counselor_type')
        specialty = request.args.get('specialty')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Counselor.query
        
        if counselor_type:
            query = query.filter_by(counselor_type=counselor_type)
        if specialty:
            query = query.filter_by(specialty=specialty)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Counselor.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Counselor.end_date <= datetime.fromisoformat(end_date))
        
        counselors = query.all()
        return format_response([counselor.to_dict() for counselor in counselors])
    except Exception as e:
        return handle_exception(e)

@counseling_bp.route('/appointments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'counseling_manager'])
def get_appointments():
    """Get all appointments with optional filters"""
    try:
        student_id = request.args.get('student_id')
        counselor_id = request.args.get('counselor_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Appointment.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if counselor_id:
            query = query.filter_by(counselor_id=counselor_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Appointment.appointment_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Appointment.appointment_date <= datetime.fromisoformat(end_date))
        
        appointments = query.all()
        return format_response([appointment.to_dict() for appointment in appointments])
    except Exception as e:
        return handle_exception(e)

@counseling_bp.route('/assessments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'counseling_manager'])
def get_assessments():
    """Get all assessments with optional filters"""
    try:
        student_id = request.args.get('student_id')
        assessment_type = request.args.get('assessment_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Assessment.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if assessment_type:
            query = query.filter_by(assessment_type=assessment_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Assessment.assessment_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Assessment.assessment_date <= datetime.fromisoformat(end_date))
        
        assessments = query.all()
        return format_response([assessment.to_dict() for assessment in assessments])
    except Exception as e:
        return handle_exception(e)

@counseling_bp.route('/resources', methods=['GET'])
@jwt_required()
@role_required(['admin', 'counseling_manager'])
def get_resources():
    """Get all resources with optional filters"""
    try:
        resource_type = request.args.get('resource_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Resource.query
        
        if resource_type:
            query = query.filter_by(resource_type=resource_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Resource.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Resource.created_at <= datetime.fromisoformat(end_date))
        
        resources = query.all()
        return format_response([resource.to_dict() for resource in resources])
    except Exception as e:
        return handle_exception(e)

@counseling_bp.route('/workshops', methods=['GET'])
@jwt_required()
@role_required(['admin', 'counseling_manager'])
def get_workshops():
    """Get all workshops with optional filters"""
    try:
        workshop_type = request.args.get('workshop_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Workshop.query
        
        if workshop_type:
            query = query.filter_by(workshop_type=workshop_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Workshop.workshop_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Workshop.workshop_date <= datetime.fromisoformat(end_date))
        
        workshops = query.all()
        return format_response([workshop.to_dict() for workshop in workshops])
    except Exception as e:
        return handle_exception(e)

@counseling_bp.route('/group-sessions', methods=['GET'])
@jwt_required()
@role_required(['admin', 'counseling_manager'])
def get_group_sessions():
    """Get all group sessions with optional filters"""
    try:
        group_type = request.args.get('group_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = GroupSession.query
        
        if group_type:
            query = query.filter_by(group_type=group_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(GroupSession.session_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(GroupSession.session_date <= datetime.fromisoformat(end_date))
        
        sessions = query.all()
        return format_response([session.to_dict() for session in sessions])
    except Exception as e:
        return handle_exception(e) 