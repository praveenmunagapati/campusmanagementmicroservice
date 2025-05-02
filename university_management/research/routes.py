from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    ResearchProject, ResearchGrant,
    ResearchPublication, ResearchPatent,
    ResearchCollaboration, ResearchEquipment,
    ResearchLab, ResearchConference,
    ResearchWorkshop, ResearchSeminar,
    ResearchStudent, ResearchSupervisor,
    ResearchLocation, ResearchContact,
    ResearchPolicy
)
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

research_bp = Blueprint('research', __name__)

@research_bp.route('/projects', methods=['GET'])
@jwt_required()
@role_required(['admin', 'research_manager'])
def get_projects():
    """Get all research projects with optional filters"""
    try:
        project_type = request.args.get('project_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchProject.query
        
        if project_type:
            query = query.filter_by(project_type=project_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchProject.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchProject.end_date <= datetime.fromisoformat(end_date))
        
        projects = query.all()
        return format_response([project.to_dict() for project in projects])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/grants', methods=['GET'])
@jwt_required()
@role_required(['admin', 'research_manager'])
def get_grants():
    """Get all research grants with optional filters"""
    try:
        grant_type = request.args.get('grant_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchGrant.query
        
        if grant_type:
            query = query.filter_by(grant_type=grant_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchGrant.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchGrant.end_date <= datetime.fromisoformat(end_date))
        
        grants = query.all()
        return format_response([grant.to_dict() for grant in grants])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/publications', methods=['GET'])
@jwt_required()
@role_required(['admin', 'research_manager'])
def get_publications():
    """Get all research publications with optional filters"""
    try:
        publication_type = request.args.get('publication_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchPublication.query
        
        if publication_type:
            query = query.filter_by(publication_type=publication_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchPublication.publication_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchPublication.publication_date <= datetime.fromisoformat(end_date))
        
        publications = query.all()
        return format_response([publication.to_dict() for publication in publications])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/patents', methods=['GET'])
@jwt_required()
@role_required(['admin', 'research_manager'])
def get_patents():
    """Get all research patents with optional filters"""
    try:
        patent_type = request.args.get('patent_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchPatent.query
        
        if patent_type:
            query = query.filter_by(patent_type=patent_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchPatent.filing_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchPatent.filing_date <= datetime.fromisoformat(end_date))
        
        patents = query.all()
        return format_response([patent.to_dict() for patent in patents])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/collaborations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'research_manager'])
def get_collaborations():
    """Get all research collaborations with optional filters"""
    try:
        collaboration_type = request.args.get('collaboration_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchCollaboration.query
        
        if collaboration_type:
            query = query.filter_by(collaboration_type=collaboration_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchCollaboration.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchCollaboration.end_date <= datetime.fromisoformat(end_date))
        
        collaborations = query.all()
        return format_response([collaboration.to_dict() for collaboration in collaborations])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/equipment', methods=['GET'])
@jwt_required()
@role_required(['admin', 'research_manager'])
def get_equipment():
    """Get all research equipment with optional filters"""
    try:
        equipment_type = request.args.get('equipment_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchEquipment.query
        
        if equipment_type:
            query = query.filter_by(equipment_type=equipment_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchEquipment.acquisition_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchEquipment.acquisition_date <= datetime.fromisoformat(end_date))
        
        equipment = query.all()
        return format_response([item.to_dict() for item in equipment])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/labs', methods=['GET'])
@jwt_required()
@role_required(['admin', 'research_manager'])
def get_labs():
    """Get all research labs with optional filters"""
    try:
        lab_type = request.args.get('lab_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchLab.query
        
        if lab_type:
            query = query.filter_by(lab_type=lab_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchLab.establishment_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchLab.establishment_date <= datetime.fromisoformat(end_date))
        
        labs = query.all()
        return format_response([lab.to_dict() for lab in labs])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/conferences', methods=['GET'])
@jwt_required()
@role_required(['admin', 'research_manager'])
def get_conferences():
    """Get all research conferences with optional filters"""
    try:
        conference_type = request.args.get('conference_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchConference.query
        
        if conference_type:
            query = query.filter_by(conference_type=conference_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchConference.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchConference.end_date <= datetime.fromisoformat(end_date))
        
        conferences = query.all()
        return format_response([conference.to_dict() for conference in conferences])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/workshops', methods=['GET'])
@jwt_required()
@role_required(['admin', 'research_manager'])
def get_workshops():
    """Get all research workshops with optional filters"""
    try:
        workshop_type = request.args.get('workshop_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchWorkshop.query
        
        if workshop_type:
            query = query.filter_by(workshop_type=workshop_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchWorkshop.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchWorkshop.end_date <= datetime.fromisoformat(end_date))
        
        workshops = query.all()
        return format_response([workshop.to_dict() for workshop in workshops])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/seminars', methods=['GET'])
@jwt_required()
@role_required(['admin', 'research_manager'])
def get_seminars():
    """Get all research seminars with optional filters"""
    try:
        seminar_type = request.args.get('seminar_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchSeminar.query
        
        if seminar_type:
            query = query.filter_by(seminar_type=seminar_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchSeminar.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchSeminar.end_date <= datetime.fromisoformat(end_date))
        
        seminars = query.all()
        return format_response([seminar.to_dict() for seminar in seminars])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/students', methods=['GET'])
@jwt_required()
@role_required(['admin', 'research_manager'])
def get_students():
    """Get all research students with optional filters"""
    try:
        student_type = request.args.get('student_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchStudent.query
        
        if student_type:
            query = query.filter_by(student_type=student_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchStudent.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchStudent.end_date <= datetime.fromisoformat(end_date))
        
        students = query.all()
        return format_response([student.to_dict() for student in students])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/supervisors', methods=['GET'])
@jwt_required()
@role_required(['admin', 'research_manager'])
def get_supervisors():
    """Get all research supervisors with optional filters"""
    try:
        supervisor_type = request.args.get('supervisor_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchSupervisor.query
        
        if supervisor_type:
            query = query.filter_by(supervisor_type=supervisor_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchSupervisor.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchSupervisor.end_date <= datetime.fromisoformat(end_date))
        
        supervisors = query.all()
        return format_response([supervisor.to_dict() for supervisor in supervisors])
    except Exception as e:
        return handle_exception(e) 