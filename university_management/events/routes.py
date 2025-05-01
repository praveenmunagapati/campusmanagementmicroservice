from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Event, EventRegistration, Venue, EventCategory, EventSpeaker, EventFeedback, EventResource
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

events_bp = Blueprint('events', __name__)

@events_bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    """Get all events with optional filters"""
    try:
        category_id = request.args.get('category_id')
        venue_id = request.args.get('venue_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Event.query
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        if venue_id:
            query = query.filter_by(venue_id=venue_id)
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

@events_bp.route('/events', methods=['POST'])
@jwt_required()
@role_required(['admin', 'event_manager'])
def create_event():
    """Create a new event"""
    try:
        data = request.get_json()
        new_event = Event(**data)
        db.session.add(new_event)
        db.session.commit()
        return format_response(new_event.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

@events_bp.route('/registrations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'event_manager'])
def get_registrations():
    """Get all event registrations with optional filters"""
    try:
        event_id = request.args.get('event_id')
        user_id = request.args.get('user_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = EventRegistration.query
        
        if event_id:
            query = query.filter_by(event_id=event_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(EventRegistration.registration_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(EventRegistration.registration_date <= datetime.fromisoformat(end_date))
        
        registrations = query.all()
        return format_response([registration.to_dict() for registration in registrations])
    except Exception as e:
        return handle_exception(e)

@events_bp.route('/venues', methods=['GET'])
@jwt_required()
def get_venues():
    """Get all venues with optional filters"""
    try:
        venue_type = request.args.get('venue_type')
        capacity = request.args.get('capacity')
        status = request.args.get('status')
        
        query = Venue.query
        
        if venue_type:
            query = query.filter_by(venue_type=venue_type)
        if capacity:
            query = query.filter(Venue.capacity >= int(capacity))
        if status:
            query = query.filter_by(status=status)
        
        venues = query.all()
        return format_response([venue.to_dict() for venue in venues])
    except Exception as e:
        return handle_exception(e)

@events_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all event categories"""
    try:
        categories = EventCategory.query.all()
        return format_response([category.to_dict() for category in categories])
    except Exception as e:
        return handle_exception(e)

@events_bp.route('/speakers', methods=['GET'])
@jwt_required()
def get_speakers():
    """Get all event speakers with optional filters"""
    try:
        event_id = request.args.get('event_id')
        speaker_type = request.args.get('speaker_type')
        status = request.args.get('status')
        
        query = EventSpeaker.query
        
        if event_id:
            query = query.filter_by(event_id=event_id)
        if speaker_type:
            query = query.filter_by(speaker_type=speaker_type)
        if status:
            query = query.filter_by(status=status)
        
        speakers = query.all()
        return format_response([speaker.to_dict() for speaker in speakers])
    except Exception as e:
        return handle_exception(e)

@events_bp.route('/feedback', methods=['GET'])
@jwt_required()
@role_required(['admin', 'event_manager'])
def get_feedback():
    """Get all event feedback with optional filters"""
    try:
        event_id = request.args.get('event_id')
        user_id = request.args.get('user_id')
        rating = request.args.get('rating')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = EventFeedback.query
        
        if event_id:
            query = query.filter_by(event_id=event_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if rating:
            query = query.filter_by(rating=rating)
        if start_date:
            query = query.filter(EventFeedback.feedback_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(EventFeedback.feedback_date <= datetime.fromisoformat(end_date))
        
        feedback = query.all()
        return format_response([f.to_dict() for f in feedback])
    except Exception as e:
        return handle_exception(e)

@events_bp.route('/resources', methods=['GET'])
@jwt_required()
def get_resources():
    """Get all event resources with optional filters"""
    try:
        event_id = request.args.get('event_id')
        resource_type = request.args.get('resource_type')
        status = request.args.get('status')
        
        query = EventResource.query
        
        if event_id:
            query = query.filter_by(event_id=event_id)
        if resource_type:
            query = query.filter_by(resource_type=resource_type)
        if status:
            query = query.filter_by(status=status)
        
        resources = query.all()
        return format_response([resource.to_dict() for resource in resources])
    except Exception as e:
        return handle_exception(e) 