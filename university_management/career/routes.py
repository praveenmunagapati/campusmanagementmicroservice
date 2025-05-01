from flask import Blueprint, jsonify, request
from .models import JobPosting, CareerEvent, CareerCounseling
from .. import db

career_bp = Blueprint('career', __name__)

@career_bp.route('/career/jobs', methods=['GET'])
def get_job_postings():
    """Get all job postings"""
    jobs = JobPosting.query.all()
    return jsonify([job.to_dict() for job in jobs])

@career_bp.route('/career/jobs/<int:id>', methods=['GET'])
def get_job_posting_by_id(id):
    """Get specific job posting by ID"""
    job = JobPosting.query.get_or_404(id)
    return jsonify(job.to_dict())

@career_bp.route('/career/jobs', methods=['POST'])
def create_job_posting():
    """Create new job posting"""
    data = request.get_json()
    new_job = JobPosting(**data)
    db.session.add(new_job)
    db.session.commit()
    return jsonify(new_job.to_dict()), 201

@career_bp.route('/career/events', methods=['GET'])
def get_career_events():
    """Get all career events"""
    events = CareerEvent.query.all()
    return jsonify([event.to_dict() for event in events])

@career_bp.route('/career/events/<int:id>', methods=['GET'])
def get_career_event_by_id(id):
    """Get specific career event by ID"""
    event = CareerEvent.query.get_or_404(id)
    return jsonify(event.to_dict())

@career_bp.route('/career/counseling', methods=['GET'])
def get_career_counseling():
    """Get all career counseling sessions"""
    sessions = CareerCounseling.query.all()
    return jsonify([session.to_dict() for session in sessions])

@career_bp.route('/career/counseling/<int:id>', methods=['GET'])
def get_career_counseling_by_id(id):
    """Get specific career counseling session by ID"""
    session = CareerCounseling.query.get_or_404(id)
    return jsonify(session.to_dict())

@career_bp.route('/career/workshops', methods=['GET'])
def get_career_workshops():
    """Get all career workshops"""
    workshops = CareerEvent.query.filter_by(event_type='workshop').all()
    return jsonify([workshop.to_dict() for workshop in workshops])

@career_bp.route('/career/internships', methods=['GET'])
def get_internships():
    """Get all internship opportunities"""
    internships = JobPosting.query.filter_by(job_type='internship').all()
    return jsonify([internship.to_dict() for internship in internships]) 