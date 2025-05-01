from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import JobPosting, CareerEvent, CareerCounseling, JobApplication, Interview, CareerResource, Employer, CareerWorkshop
from .. import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

career_bp = Blueprint('career', __name__)

@career_bp.route('/jobs', methods=['GET'])
@jwt_required()
def get_job_postings():
    """Get all job postings with optional filters"""
    try:
        employer_id = request.args.get('employer_id')
        job_type = request.args.get('job_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = JobPosting.query
        
        if employer_id:
            query = query.filter_by(employer_id=employer_id)
        if job_type:
            query = query.filter_by(job_type=job_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(JobPosting.posted_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(JobPosting.posted_date <= datetime.fromisoformat(end_date))
        
        jobs = query.all()
        return format_response([job.to_dict() for job in jobs])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/events', methods=['GET'])
@jwt_required()
def get_career_events():
    """Get all career events with optional filters"""
    try:
        event_type = request.args.get('event_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CareerEvent.query
        
        if event_type:
            query = query.filter_by(event_type=event_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(CareerEvent.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CareerEvent.end_date <= datetime.fromisoformat(end_date))
        
        events = query.all()
        return format_response([event.to_dict() for event in events])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/counseling', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_staff', 'student'])
def get_counseling_sessions():
    """Get career counseling sessions with optional filters"""
    try:
        counselor_id = request.args.get('counselor_id')
        student_id = request.args.get('student_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CareerCounseling.query
        
        if counselor_id:
            query = query.filter_by(counselor_id=counselor_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(CareerCounseling.scheduled_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CareerCounseling.scheduled_date <= datetime.fromisoformat(end_date))
        
        sessions = query.all()
        return format_response([session.to_dict() for session in sessions])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/applications', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_staff', 'student'])
def get_job_applications():
    """Get job applications with optional filters"""
    try:
        student_id = request.args.get('student_id')
        job_id = request.args.get('job_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = JobApplication.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if job_id:
            query = query.filter_by(job_id=job_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(JobApplication.application_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(JobApplication.application_date <= datetime.fromisoformat(end_date))
        
        applications = query.all()
        return format_response([app.to_dict() for app in applications])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/interviews', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_staff', 'student'])
def get_interviews():
    """Get interviews with optional filters"""
    try:
        student_id = request.args.get('student_id')
        job_id = request.args.get('job_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Interview.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if job_id:
            query = query.filter_by(job_id=job_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Interview.scheduled_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Interview.scheduled_date <= datetime.fromisoformat(end_date))
        
        interviews = query.all()
        return format_response([interview.to_dict() for interview in interviews])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/resources', methods=['GET'])
@jwt_required()
def get_career_resources():
    """Get career resources with optional filters"""
    try:
        resource_type = request.args.get('resource_type')
        category = request.args.get('category')
        
        query = CareerResource.query
        
        if resource_type:
            query = query.filter_by(resource_type=resource_type)
        if category:
            query = query.filter_by(category=category)
        
        resources = query.all()
        return format_response([resource.to_dict() for resource in resources])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/employers', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_staff'])
def get_employers():
    """Get employers with optional filters"""
    try:
        industry = request.args.get('industry')
        status = request.args.get('status')
        
        query = Employer.query
        
        if industry:
            query = query.filter_by(industry=industry)
        if status:
            query = query.filter_by(status=status)
        
        employers = query.all()
        return format_response([employer.to_dict() for employer in employers])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/workshops', methods=['GET'])
@jwt_required()
def get_workshops():
    """Get career workshops with optional filters"""
    try:
        workshop_type = request.args.get('workshop_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CareerWorkshop.query
        
        if workshop_type:
            query = query.filter_by(workshop_type=workshop_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(CareerWorkshop.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CareerWorkshop.end_date <= datetime.fromisoformat(end_date))
        
        workshops = query.all()
        return format_response([workshop.to_dict() for workshop in workshops])
    except Exception as e:
        return handle_exception(e) 