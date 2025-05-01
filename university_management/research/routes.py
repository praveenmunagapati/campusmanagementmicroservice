from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    ResearchProject, ResearchGrant, ResearchPublication,
    ResearchCollaboration, ResearchEquipment, ResearchData,
    ResearchTeam, ResearchMilestone, ResearchExpense,
    ResearchEthics, ResearchPatent, ResearchConference,
    ResearchTraining, ResearchAward
)
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

research_bp = Blueprint('research', __name__)

@research_bp.route('/projects', methods=['GET'])
@jwt_required()
@role_required(['admin', 'researcher'])
def get_research_projects():
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
@role_required(['admin', 'researcher'])
def get_research_grants():
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
@role_required(['admin', 'researcher'])
def get_research_publications():
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

@research_bp.route('/collaborations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'researcher'])
def get_research_collaborations():
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
@role_required(['admin', 'researcher'])
def get_research_equipment():
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

@research_bp.route('/data', methods=['GET'])
@jwt_required()
@role_required(['admin', 'researcher'])
def get_research_data():
    """Get all research data with optional filters"""
    try:
        data_type = request.args.get('data_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchData.query
        
        if data_type:
            query = query.filter_by(data_type=data_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchData.collection_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchData.collection_date <= datetime.fromisoformat(end_date))
        
        data = query.all()
        return format_response([item.to_dict() for item in data])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/teams', methods=['GET'])
@jwt_required()
@role_required(['admin', 'researcher'])
def get_research_teams():
    """Get all research teams with optional filters"""
    try:
        team_type = request.args.get('team_type')
        status = request.args.get('status')
        
        query = ResearchTeam.query
        
        if team_type:
            query = query.filter_by(team_type=team_type)
        if status:
            query = query.filter_by(status=status)
        
        teams = query.all()
        return format_response([team.to_dict() for team in teams])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/milestones', methods=['GET'])
@jwt_required()
@role_required(['admin', 'researcher'])
def get_research_milestones():
    """Get all research milestones with optional filters"""
    try:
        milestone_type = request.args.get('milestone_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchMilestone.query
        
        if milestone_type:
            query = query.filter_by(milestone_type=milestone_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchMilestone.target_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchMilestone.target_date <= datetime.fromisoformat(end_date))
        
        milestones = query.all()
        return format_response([milestone.to_dict() for milestone in milestones])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/expenses', methods=['GET'])
@jwt_required()
@role_required(['admin', 'researcher'])
def get_research_expenses():
    """Get all research expenses with optional filters"""
    try:
        expense_type = request.args.get('expense_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchExpense.query
        
        if expense_type:
            query = query.filter_by(expense_type=expense_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchExpense.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchExpense.date <= datetime.fromisoformat(end_date))
        
        expenses = query.all()
        return format_response([expense.to_dict() for expense in expenses])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/ethics', methods=['GET'])
@jwt_required()
@role_required(['admin', 'researcher'])
def get_research_ethics():
    """Get all research ethics records with optional filters"""
    try:
        ethics_type = request.args.get('ethics_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchEthics.query
        
        if ethics_type:
            query = query.filter_by(ethics_type=ethics_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchEthics.approval_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchEthics.approval_date <= datetime.fromisoformat(end_date))
        
        ethics_records = query.all()
        return format_response([record.to_dict() for record in ethics_records])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/patents', methods=['GET'])
@jwt_required()
@role_required(['admin', 'researcher'])
def get_research_patents():
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

@research_bp.route('/conferences', methods=['GET'])
@jwt_required()
@role_required(['admin', 'researcher'])
def get_research_conferences():
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

@research_bp.route('/training', methods=['GET'])
@jwt_required()
@role_required(['admin', 'researcher'])
def get_research_training():
    """Get all research training records with optional filters"""
    try:
        training_type = request.args.get('training_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchTraining.query
        
        if training_type:
            query = query.filter_by(training_type=training_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchTraining.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchTraining.end_date <= datetime.fromisoformat(end_date))
        
        training_records = query.all()
        return format_response([record.to_dict() for record in training_records])
    except Exception as e:
        return handle_exception(e)

@research_bp.route('/awards', methods=['GET'])
@jwt_required()
@role_required(['admin', 'researcher'])
def get_research_awards():
    """Get all research awards with optional filters"""
    try:
        award_type = request.args.get('award_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ResearchAward.query
        
        if award_type:
            query = query.filter_by(award_type=award_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(ResearchAward.award_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(ResearchAward.award_date <= datetime.fromisoformat(end_date))
        
        awards = query.all()
        return format_response([award.to_dict() for award in awards])
    except Exception as e:
        return handle_exception(e) 