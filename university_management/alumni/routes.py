from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Alumni, AlumniEvent, AlumniDonation, AlumniNetwork, AlumniJob, AlumniEducation, AlumniAchievement, AlumniContact, AlumniGroup, AlumniSurvey
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

alumni_bp = Blueprint('alumni', __name__)

@alumni_bp.route('/alumni', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_staff', 'alumni'])
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
        return format_response([alum.to_dict() for alum in alumni])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/events', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_staff', 'alumni'])
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
            query = query.filter(AlumniEvent.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AlumniEvent.date <= datetime.fromisoformat(end_date))
        
        events = query.all()
        return format_response([event.to_dict() for event in events])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/donations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_staff'])
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
            query = query.filter(AlumniDonation.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AlumniDonation.date <= datetime.fromisoformat(end_date))
        
        donations = query.all()
        return format_response([donation.to_dict() for donation in donations])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/network', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_staff', 'alumni'])
def get_network():
    """Get all alumni network connections with optional filters"""
    try:
        alumni_id = request.args.get('alumni_id')
        connection_type = request.args.get('connection_type')
        status = request.args.get('status')
        
        query = AlumniNetwork.query
        
        if alumni_id:
            query = query.filter_by(alumni_id=alumni_id)
        if connection_type:
            query = query.filter_by(connection_type=connection_type)
        if status:
            query = query.filter_by(status=status)
        
        connections = query.all()
        return format_response([conn.to_dict() for conn in connections])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/jobs', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_staff', 'alumni'])
def get_jobs():
    """Get all alumni jobs with optional filters"""
    try:
        alumni_id = request.args.get('alumni_id')
        job_type = request.args.get('job_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = AlumniJob.query
        
        if alumni_id:
            query = query.filter_by(alumni_id=alumni_id)
        if job_type:
            query = query.filter_by(job_type=job_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(AlumniJob.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AlumniJob.end_date <= datetime.fromisoformat(end_date))
        
        jobs = query.all()
        return format_response([job.to_dict() for job in jobs])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/education', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_staff', 'alumni'])
def get_education():
    """Get all alumni education records with optional filters"""
    try:
        alumni_id = request.args.get('alumni_id')
        degree_type = request.args.get('degree_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = AlumniEducation.query
        
        if alumni_id:
            query = query.filter_by(alumni_id=alumni_id)
        if degree_type:
            query = query.filter_by(degree_type=degree_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(AlumniEducation.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AlumniEducation.end_date <= datetime.fromisoformat(end_date))
        
        education_records = query.all()
        return format_response([record.to_dict() for record in education_records])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/achievements', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_staff', 'alumni'])
def get_achievements():
    """Get all alumni achievements with optional filters"""
    try:
        alumni_id = request.args.get('alumni_id')
        achievement_type = request.args.get('achievement_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = AlumniAchievement.query
        
        if alumni_id:
            query = query.filter_by(alumni_id=alumni_id)
        if achievement_type:
            query = query.filter_by(achievement_type=achievement_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(AlumniAchievement.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AlumniAchievement.date <= datetime.fromisoformat(end_date))
        
        achievements = query.all()
        return format_response([achievement.to_dict() for achievement in achievements])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/contacts', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_staff'])
def get_contacts():
    """Get all alumni contacts with optional filters"""
    try:
        alumni_id = request.args.get('alumni_id')
        contact_type = request.args.get('contact_type')
        status = request.args.get('status')
        
        query = AlumniContact.query
        
        if alumni_id:
            query = query.filter_by(alumni_id=alumni_id)
        if contact_type:
            query = query.filter_by(contact_type=contact_type)
        if status:
            query = query.filter_by(status=status)
        
        contacts = query.all()
        return format_response([contact.to_dict() for contact in contacts])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/groups', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_staff', 'alumni'])
def get_groups():
    """Get all alumni groups with optional filters"""
    try:
        group_type = request.args.get('group_type')
        status = request.args.get('status')
        
        query = AlumniGroup.query
        
        if group_type:
            query = query.filter_by(group_type=group_type)
        if status:
            query = query.filter_by(status=status)
        
        groups = query.all()
        return format_response([group.to_dict() for group in groups])
    except Exception as e:
        return handle_exception(e)

@alumni_bp.route('/surveys', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni_staff'])
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
            query = query.filter(AlumniSurvey.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(AlumniSurvey.end_date <= datetime.fromisoformat(end_date))
        
        surveys = query.all()
        return format_response([survey.to_dict() for survey in surveys])
    except Exception as e:
        return handle_exception(e) 