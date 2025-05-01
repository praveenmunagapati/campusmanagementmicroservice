from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    Alumni, AlumniEducation, AlumniEmployment,
    AlumniEvent, AlumniDonation, AlumniMembership,
    AlumniNetwork, AlumniProgram, AlumniSurvey,
    AlumniFeedback, AlumniResource, AlumniLocation,
    AlumniContact, AlumniAchievement, AlumniPublication
)
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

alumni_bp = Blueprint('alumni', __name__)

@alumni_bp.route('/alumni', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_manager'])
def get_alumni():
    """Get all alumni with optional filters"""
    try:
        graduation_year = request.args.get('graduation_year')
        program = request.args.get('program')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Alumni.query
        
        if graduation_year:
            query = query.filter_by(graduation_year=graduation_year)
        if program:
            query = query.filter_by(program=program)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Alumni.graduation_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Alumni.graduation_date <= datetime.fromisoformat(end_date))
        
        alumni = query.all()
        return format_response([alumnus.to_dict() for alumnus in alumni])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/education', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_manager'])
def get_education():
    """Get all alumni education records with optional filters"""
    try:
        alumni_id = request.args.get('alumni_id')
        degree = request.args.get('degree')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = AlumniEducation.query
        
        if alumni_id:
            query = query.filter_by(alumni_id=alumni_id)
        if degree:
            query = query.filter_by(degree=degree)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(AlumniEducation.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AlumniEducation.end_date <= datetime.fromisoformat(end_date))
        
        education = query.all()
        return format_response([record.to_dict() for record in education])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/employment', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_manager'])
def get_employment():
    """Get all alumni employment records with optional filters"""
    try:
        alumni_id = request.args.get('alumni_id')
        company = request.args.get('company')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = AlumniEmployment.query
        
        if alumni_id:
            query = query.filter_by(alumni_id=alumni_id)
        if company:
            query = query.filter(AlumniEmployment.company.ilike(f'%{company}%'))
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(AlumniEmployment.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AlumniEmployment.end_date <= datetime.fromisoformat(end_date))
        
        employment = query.all()
        return format_response([record.to_dict() for record in employment])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/events', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_manager'])
def get_events():
    """Get all alumni events with optional filters"""
    try:
        event_type = request.args.get('event_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = AlumniEvent.query
        
        if event_type:
            query = query.filter_by(event_type=event_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(AlumniEvent.event_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AlumniEvent.event_date <= datetime.fromisoformat(end_date))
        
        events = query.all()
        return format_response([event.to_dict() for event in events])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/donations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_manager'])
def get_donations():
    """Get all alumni donations with optional filters"""
    try:
        alumni_id = request.args.get('alumni_id')
        donation_type = request.args.get('donation_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = AlumniDonation.query
        
        if alumni_id:
            query = query.filter_by(alumni_id=alumni_id)
        if donation_type:
            query = query.filter_by(donation_type=donation_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(AlumniDonation.donation_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AlumniDonation.donation_date <= datetime.fromisoformat(end_date))
        
        donations = query.all()
        return format_response([donation.to_dict() for donation in donations])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/memberships', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_manager'])
def get_memberships():
    """Get all alumni memberships with optional filters"""
    try:
        alumni_id = request.args.get('alumni_id')
        membership_type = request.args.get('membership_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = AlumniMembership.query
        
        if alumni_id:
            query = query.filter_by(alumni_id=alumni_id)
        if membership_type:
            query = query.filter_by(membership_type=membership_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(AlumniMembership.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AlumniMembership.end_date <= datetime.fromisoformat(end_date))
        
        memberships = query.all()
        return format_response([membership.to_dict() for membership in memberships])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/networks', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_manager'])
def get_networks():
    """Get all alumni networks with optional filters"""
    try:
        network_type = request.args.get('network_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = AlumniNetwork.query
        
        if network_type:
            query = query.filter_by(network_type=network_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(AlumniNetwork.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AlumniNetwork.created_at <= datetime.fromisoformat(end_date))
        
        networks = query.all()
        return format_response([network.to_dict() for network in networks])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/programs', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_manager'])
def get_programs():
    """Get all alumni programs with optional filters"""
    try:
        program_type = request.args.get('program_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = AlumniProgram.query
        
        if program_type:
            query = query.filter_by(program_type=program_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(AlumniProgram.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AlumniProgram.end_date <= datetime.fromisoformat(end_date))
        
        programs = query.all()
        return format_response([program.to_dict() for program in programs])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/surveys', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_manager'])
def get_surveys():
    """Get all alumni surveys with optional filters"""
    try:
        survey_type = request.args.get('survey_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = AlumniSurvey.query
        
        if survey_type:
            query = query.filter_by(survey_type=survey_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(AlumniSurvey.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AlumniSurvey.created_at <= datetime.fromisoformat(end_date))
        
        surveys = query.all()
        return format_response([survey.to_dict() for survey in surveys])
    except Exception as e:
        return handle_exception(e) 