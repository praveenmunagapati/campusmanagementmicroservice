from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    Sport, Team, Player, Coach, Match, Tournament,
    Facility, Equipment, Schedule, Training,
    Achievement, Injury, Membership, Payment,
    Event, Staff, Report, Policy
)
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

sports_bp = Blueprint('sports', __name__)

@ sports_bp.route('/sports', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_sports():
    """Get all sports with optional filters"""
    try:
        name = request.args.get('name')
        category = request.args.get('category')
        status = request.args.get('status')
        
        query = Sport.query
        
        if name:
            query = query.filter(Sport.name.ilike(f'%{name}%'))
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        
        sports = query.all()
        return format_response([sport.to_dict() for sport in sports])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/teams', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_teams():
    """Get all teams with optional filters"""
    try:
        sport_id = request.args.get('sport_id')
        level = request.args.get('level')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Team.query
        
        if sport_id:
            query = query.filter_by(sport_id=sport_id)
        if level:
            query = query.filter_by(level=level)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Team.formation_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Team.formation_date <= datetime.fromisoformat(end_date))
        
        teams = query.all()
        return format_response([team.to_dict() for team in teams])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/players', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_players():
    """Get all players with optional filters"""
    try:
        team_id = request.args.get('team_id')
        position = request.args.get('position')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Player.query
        
        if team_id:
            query = query.filter_by(team_id=team_id)
        if position:
            query = query.filter_by(position=position)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Player.join_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Player.join_date <= datetime.fromisoformat(end_date))
        
        players = query.all()
        return format_response([player.to_dict() for player in players])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/coaches', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_coaches():
    """Get all coaches with optional filters"""
    try:
        team_id = request.args.get('team_id')
        role = request.args.get('role')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Coach.query
        
        if team_id:
            query = query.filter_by(team_id=team_id)
        if role:
            query = query.filter_by(role=role)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Coach.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Coach.start_date <= datetime.fromisoformat(end_date))
        
        coaches = query.all()
        return format_response([coach.to_dict() for coach in coaches])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/matches', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_matches():
    """Get all matches with optional filters"""
    try:
        team_id = request.args.get('team_id')
        opponent = request.args.get('opponent')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Match.query
        
        if team_id:
            query = query.filter_by(team_id=team_id)
        if opponent:
            query = query.filter(Match.opponent.ilike(f'%{opponent}%'))
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Match.match_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Match.match_date <= datetime.fromisoformat(end_date))
        
        matches = query.all()
        return format_response([match.to_dict() for match in matches])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/tournaments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_tournaments():
    """Get all tournaments with optional filters"""
    try:
        sport_id = request.args.get('sport_id')
        level = request.args.get('level')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Tournament.query
        
        if sport_id:
            query = query.filter_by(sport_id=sport_id)
        if level:
            query = query.filter_by(level=level)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Tournament.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Tournament.end_date <= datetime.fromisoformat(end_date))
        
        tournaments = query.all()
        return format_response([tournament.to_dict() for tournament in tournaments])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/facilities', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_facilities():
    """Get all facilities with optional filters"""
    try:
        facility_type = request.args.get('facility_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Facility.query
        
        if facility_type:
            query = query.filter_by(facility_type=facility_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Facility.available_from >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Facility.available_until <= datetime.fromisoformat(end_date))
        
        facilities = query.all()
        return format_response([facility.to_dict() for facility in facilities])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/equipment', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_equipment():
    """Get all equipment with optional filters"""
    try:
        equipment_type = request.args.get('equipment_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Equipment.query
        
        if equipment_type:
            query = query.filter_by(equipment_type=equipment_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Equipment.acquisition_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Equipment.acquisition_date <= datetime.fromisoformat(end_date))
        
        equipment = query.all()
        return format_response([item.to_dict() for item in equipment])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/schedules', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_schedules():
    """Get all schedules with optional filters"""
    try:
        team_id = request.args.get('team_id')
        event_type = request.args.get('event_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Schedule.query
        
        if team_id:
            query = query.filter_by(team_id=team_id)
        if event_type:
            query = query.filter_by(event_type=event_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Schedule.start_time >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Schedule.end_time <= datetime.fromisoformat(end_date))
        
        schedules = query.all()
        return format_response([schedule.to_dict() for schedule in schedules])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/trainings', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_trainings():
    """Get all trainings with optional filters"""
    try:
        team_id = request.args.get('team_id')
        training_type = request.args.get('training_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Training.query
        
        if team_id:
            query = query.filter_by(team_id=team_id)
        if training_type:
            query = query.filter_by(training_type=training_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Training.start_time >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Training.end_time <= datetime.fromisoformat(end_date))
        
        trainings = query.all()
        return format_response([training.to_dict() for training in trainings])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/achievements', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_achievements():
    """Get all achievements with optional filters"""
    try:
        team_id = request.args.get('team_id')
        achievement_type = request.args.get('achievement_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Achievement.query
        
        if team_id:
            query = query.filter_by(team_id=team_id)
        if achievement_type:
            query = query.filter_by(achievement_type=achievement_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Achievement.date_achieved >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Achievement.date_achieved <= datetime.fromisoformat(end_date))
        
        achievements = query.all()
        return format_response([achievement.to_dict() for achievement in achievements])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/injuries', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_injuries():
    """Get all injuries with optional filters"""
    try:
        player_id = request.args.get('player_id')
        injury_type = request.args.get('injury_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Injury.query
        
        if player_id:
            query = query.filter_by(player_id=player_id)
        if injury_type:
            query = query.filter_by(injury_type=injury_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Injury.date_occurred >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Injury.date_occurred <= datetime.fromisoformat(end_date))
        
        injuries = query.all()
        return format_response([injury.to_dict() for injury in injuries])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/memberships', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_memberships():
    """Get all memberships with optional filters"""
    try:
        user_id = request.args.get('user_id')
        membership_type = request.args.get('membership_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Membership.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if membership_type:
            query = query.filter_by(membership_type=membership_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Membership.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Membership.end_date <= datetime.fromisoformat(end_date))
        
        memberships = query.all()
        return format_response([membership.to_dict() for membership in memberships])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/payments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_payments():
    """Get all payments with optional filters"""
    try:
        user_id = request.args.get('user_id')
        payment_type = request.args.get('payment_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Payment.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        if payment_type:
            query = query.filter_by(payment_type=payment_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Payment.payment_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Payment.payment_date <= datetime.fromisoformat(end_date))
        
        payments = query.all()
        return format_response([payment.to_dict() for payment in payments])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/events', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_events():
    """Get all events with optional filters"""
    try:
        event_type = request.args.get('event_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Event.query
        
        if event_type:
            query = query.filter_by(event_type=event_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Event.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Event.end_date <= datetime.fromisoformat(end_date))
        
        events = query.all()
        return format_response([event.to_dict() for event in events])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/staff', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_staff():
    """Get all staff with optional filters"""
    try:
        role = request.args.get('role')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Staff.query
        
        if role:
            query = query.filter_by(role=role)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Staff.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Staff.start_date <= datetime.fromisoformat(end_date))
        
        staff = query.all()
        return format_response([member.to_dict() for member in staff])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/reports', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_reports():
    """Get all reports with optional filters"""
    try:
        report_type = request.args.get('report_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Report.query
        
        if report_type:
            query = query.filter_by(report_type=report_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Report.report_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Report.report_date <= datetime.fromisoformat(end_date))
        
        reports = query.all()
        return format_response([report.to_dict() for report in reports])
    except Exception as e:
        return handle_exception(e)

@ sports_bp.route('/policies', methods=['GET'])
@jwt_required()
@role_required(['admin', 'sports_manager'])
def get_policies():
    """Get all policies with optional filters"""
    try:
        policy_type = request.args.get('policy_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Policy.query
        
        if policy_type:
            query = query.filter_by(policy_type=policy_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Policy.effective_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Policy.effective_date <= datetime.fromisoformat(end_date))
        
        policies = query.all()
        return format_response([policy.to_dict() for policy in policies])
    except Exception as e:
        return handle_exception(e) 