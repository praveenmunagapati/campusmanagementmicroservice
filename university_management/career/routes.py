from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    JobPosting, CareerEvent, CareerCounseling, JobApplication, Interview, CareerResource,
    Employer, CareerWorkshop, CareerAdvisor, CareerAppointment, CareerFeedback,
    CareerSurvey, CareerProgram, CareerNetwork, CareerLocation, CareerContact, CareerPolicy
)
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

@career_bp.route('/advisors', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_manager'])
def get_advisors():
    """Get all career advisors with optional filters"""
    try:
        advisor_type = request.args.get('advisor_type')
        specialty = request.args.get('specialty')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CareerAdvisor.query
        
        if advisor_type:
            query = query.filter_by(advisor_type=advisor_type)
        if specialty:
            query = query.filter_by(specialty=specialty)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(CareerAdvisor.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CareerAdvisor.end_date <= datetime.fromisoformat(end_date))
        
        advisors = query.all()
        return format_response([advisor.to_dict() for advisor in advisors])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/events', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_manager'])
def get_events():
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
            query = query.filter(CareerEvent.event_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CareerEvent.event_date <= datetime.fromisoformat(end_date))
        
        events = query.all()
        return format_response([event.to_dict() for event in events])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/workshops', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_manager'])
def get_workshops():
    """Get all career workshops with optional filters"""
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
            query = query.filter(CareerWorkshop.workshop_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CareerWorkshop.workshop_date <= datetime.fromisoformat(end_date))
        
        workshops = query.all()
        return format_response([workshop.to_dict() for workshop in workshops])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/job-postings', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_manager'])
def get_job_postings():
    """Get all job postings with optional filters"""
    try:
        job_type = request.args.get('job_type')
        company = request.args.get('company')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = JobPosting.query
        
        if job_type:
            query = query.filter_by(job_type=job_type)
        if company:
            query = query.filter(JobPosting.company.ilike(f'%{company}%'))
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(JobPosting.posting_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(JobPosting.posting_date <= datetime.fromisoformat(end_date))
        
        postings = query.all()
        return format_response([posting.to_dict() for posting in postings])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/internships', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_manager'])
def get_internships():
    """Get all internships with optional filters"""
    try:
        internship_type = request.args.get('internship_type')
        company = request.args.get('company')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Internship.query
        
        if internship_type:
            query = query.filter_by(internship_type=internship_type)
        if company:
            query = query.filter(Internship.company.ilike(f'%{company}%'))
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Internship.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Internship.end_date <= datetime.fromisoformat(end_date))
        
        internships = query.all()
        return format_response([internship.to_dict() for internship in internships])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/resources', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_manager'])
def get_resources():
    """Get all career resources with optional filters"""
    try:
        resource_type = request.args.get('resource_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CareerResource.query
        
        if resource_type:
            query = query.filter_by(resource_type=resource_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(CareerResource.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CareerResource.created_at <= datetime.fromisoformat(end_date))
        
        resources = query.all()
        return format_response([resource.to_dict() for resource in resources])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/assessments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_manager'])
def get_assessments():
    """Get all career assessments with optional filters"""
    try:
        assessment_type = request.args.get('assessment_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CareerAssessment.query
        
        if assessment_type:
            query = query.filter_by(assessment_type=assessment_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(CareerAssessment.assessment_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CareerAssessment.assessment_date <= datetime.fromisoformat(end_date))
        
        assessments = query.all()
        return format_response([assessment.to_dict() for assessment in assessments])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/appointments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_manager'])
def get_appointments():
    """Get all career appointments with optional filters"""
    try:
        student_id = request.args.get('student_id')
        advisor_id = request.args.get('advisor_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CareerAppointment.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if advisor_id:
            query = query.filter_by(advisor_id=advisor_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(CareerAppointment.appointment_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CareerAppointment.appointment_date <= datetime.fromisoformat(end_date))
        
        appointments = query.all()
        return format_response([appointment.to_dict() for appointment in appointments])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/feedback', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_manager'])
def get_feedback():
    """Get all career feedback with optional filters"""
    try:
        feedback_type = request.args.get('feedback_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CareerFeedback.query
        
        if feedback_type:
            query = query.filter_by(feedback_type=feedback_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(CareerFeedback.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CareerFeedback.created_at <= datetime.fromisoformat(end_date))
        
        feedback = query.all()
        return format_response([item.to_dict() for item in feedback])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/surveys', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_manager'])
def get_surveys():
    """Get all career surveys with optional filters"""
    try:
        survey_type = request.args.get('survey_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CareerSurvey.query
        
        if survey_type:
            query = query.filter_by(survey_type=survey_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(CareerSurvey.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CareerSurvey.created_at <= datetime.fromisoformat(end_date))
        
        surveys = query.all()
        return format_response([survey.to_dict() for survey in surveys])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/programs', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_manager'])
def get_programs():
    """Get all career programs with optional filters"""
    try:
        program_type = request.args.get('program_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CareerProgram.query
        
        if program_type:
            query = query.filter_by(program_type=program_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(CareerProgram.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CareerProgram.end_date <= datetime.fromisoformat(end_date))
        
        programs = query.all()
        return format_response([program.to_dict() for program in programs])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/networks', methods=['GET'])
@jwt_required()
@role_required(['admin', 'career_manager'])
def get_networks():
    """Get all career networks with optional filters"""
    try:
        network_type = request.args.get('network_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = CareerNetwork.query
        
        if network_type:
            query = query.filter_by(network_type=network_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(CareerNetwork.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(CareerNetwork.created_at <= datetime.fromisoformat(end_date))
        
        networks = query.all()
        return format_response([network.to_dict() for network in networks])
    except Exception as e:
        return handle_exception(e) 