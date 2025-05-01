from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    Parent, StudentParent, ParentNotification, ParentAccessLog,
    ParentMeeting, ParentFeedback, ParentDocument
)
from .. import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

parent_bp = Blueprint('parent', __name__)

# Parent Routes
@parent_bp.route('/parents', methods=['GET'])
@jwt_required()
def get_parents():
    """Get all parents"""
    parents = Parent.query.all()
    return jsonify([parent.to_dict() for parent in parents])

@parent_bp.route('/parents/<int:id>', methods=['GET'])
@jwt_required()
def get_parent_by_id(id):
    """Get specific parent by ID"""
    parent = Parent.query.get_or_404(id)
    return jsonify(parent.to_dict())

@parent_bp.route('/parents', methods=['POST'])
@jwt_required()
@role_required(['admin', 'registrar'])
def create_parent():
    """Create new parent record"""
    data = request.get_json()
    new_parent = Parent(**data)
    db.session.add(new_parent)
    db.session.commit()
    return jsonify(new_parent.to_dict()), 201

@parent_bp.route('/parents/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'registrar'])
def update_parent(id):
    """Update existing parent record"""
    parent = Parent.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(parent, key, value)
    db.session.commit()
    return jsonify(parent.to_dict())

@parent_bp.route('/parents/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_parent(id):
    """Delete parent record"""
    parent = Parent.query.get_or_404(id)
    db.session.delete(parent)
    db.session.commit()
    return '', 204

# Student-Parent Relationship Routes
@parent_bp.route('/parents/<int:parent_id>/students', methods=['GET'])
@jwt_required()
def get_parent_students(parent_id):
    """Get students associated with a parent"""
    relationships = StudentParent.query.filter_by(parent_id=parent_id).all()
    return jsonify([rel.to_dict() for rel in relationships])

@parent_bp.route('/parents/<int:parent_id>/students', methods=['POST'])
@jwt_required()
@role_required(['admin', 'registrar'])
def add_student_to_parent(parent_id):
    """Add student to parent"""
    data = request.get_json()
    data['parent_id'] = parent_id
    new_relationship = StudentParent(**data)
    db.session.add(new_relationship)
    db.session.commit()
    return jsonify(new_relationship.to_dict()), 201

@parent_bp.route('/parents/students/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'registrar'])
def update_student_parent_relationship(id):
    """Update student-parent relationship"""
    relationship = StudentParent.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(relationship, key, value)
    db.session.commit()
    return jsonify(relationship.to_dict())

@parent_bp.route('/parents/students/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def remove_student_from_parent(id):
    """Remove student from parent"""
    relationship = StudentParent.query.get_or_404(id)
    db.session.delete(relationship)
    db.session.commit()
    return '', 204

# Parent Notification Routes
@parent_bp.route('/parents/<int:parent_id>/notifications', methods=['GET'])
@jwt_required()
def get_parent_notifications(parent_id):
    """Get notifications for parent"""
    notifications = ParentNotification.query.filter_by(parent_id=parent_id).all()
    return jsonify([notification.to_dict() for notification in notifications])

@parent_bp.route('/parents/<int:parent_id>/notifications', methods=['POST'])
@jwt_required()
@role_required(['admin', 'teacher', 'staff'])
def create_parent_notification(parent_id):
    """Create new notification for parent"""
    data = request.get_json()
    data['parent_id'] = parent_id
    new_notification = ParentNotification(**data)
    db.session.add(new_notification)
    db.session.commit()
    return jsonify(new_notification.to_dict()), 201

@parent_bp.route('/parents/notifications/<int:id>', methods=['PUT'])
@jwt_required()
def update_notification(id):
    """Update notification (e.g., mark as read)"""
    notification = ParentNotification.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(notification, key, value)
    db.session.commit()
    return jsonify(notification.to_dict())

# Parent Access Log Routes
@parent_bp.route('/parents/<int:parent_id>/access-logs', methods=['GET'])
@jwt_required()
@role_required(['admin', 'security'])
def get_parent_access_logs(parent_id):
    """Get access logs for parent"""
    logs = ParentAccessLog.query.filter_by(parent_id=parent_id).all()
    return jsonify([log.to_dict() for log in logs])

@parent_bp.route('/parents/<int:parent_id>/access-logs', methods=['POST'])
@jwt_required()
def create_access_log(parent_id):
    """Create new access log entry"""
    data = request.get_json()
    data['parent_id'] = parent_id
    new_log = ParentAccessLog(**data)
    db.session.add(new_log)
    db.session.commit()
    return jsonify(new_log.to_dict()), 201

# Parent Meeting Routes
@parent_bp.route('/parents/<int:parent_id>/meetings', methods=['GET'])
@jwt_required()
def get_parent_meetings(parent_id):
    """Get meetings for parent"""
    meetings = ParentMeeting.query.filter_by(parent_id=parent_id).all()
    return jsonify([meeting.to_dict() for meeting in meetings])

@parent_bp.route('/parents/<int:parent_id>/meetings', methods=['POST'])
@jwt_required()
@role_required(['admin', 'teacher', 'staff'])
def schedule_parent_meeting(parent_id):
    """Schedule new meeting with parent"""
    data = request.get_json()
    data['parent_id'] = parent_id
    new_meeting = ParentMeeting(**data)
    db.session.add(new_meeting)
    db.session.commit()
    return jsonify(new_meeting.to_dict()), 201

@parent_bp.route('/parents/meetings/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'teacher', 'staff'])
def update_meeting(id):
    """Update meeting details"""
    meeting = ParentMeeting.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(meeting, key, value)
    db.session.commit()
    return jsonify(meeting.to_dict())

@parent_bp.route('/parents/meetings/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'teacher', 'staff'])
def cancel_meeting(id):
    """Cancel meeting"""
    meeting = ParentMeeting.query.get_or_404(id)
    db.session.delete(meeting)
    db.session.commit()
    return '', 204

# Parent Feedback Routes
@parent_bp.route('/parents/<int:parent_id>/feedback', methods=['GET'])
@jwt_required()
def get_parent_feedback(parent_id):
    """Get feedback from parent"""
    feedback = ParentFeedback.query.filter_by(parent_id=parent_id).all()
    return jsonify([f.to_dict() for f in feedback])

@parent_bp.route('/parents/<int:parent_id>/feedback', methods=['POST'])
@jwt_required()
def submit_parent_feedback(parent_id):
    """Submit new feedback from parent"""
    data = request.get_json()
    data['parent_id'] = parent_id
    new_feedback = ParentFeedback(**data)
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify(new_feedback.to_dict()), 201

@parent_bp.route('/parents/feedback/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'staff'])
def update_feedback(id):
    """Update feedback status or resolution"""
    feedback = ParentFeedback.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(feedback, key, value)
    db.session.commit()
    return jsonify(feedback.to_dict())

# Parent Document Routes
@parent_bp.route('/parents/<int:parent_id>/documents', methods=['GET'])
@jwt_required()
def get_parent_documents(parent_id):
    """Get documents for parent"""
    documents = ParentDocument.query.filter_by(parent_id=parent_id).all()
    return jsonify([doc.to_dict() for doc in documents])

@parent_bp.route('/parents/<int:parent_id>/documents', methods=['POST'])
@jwt_required()
@role_required(['admin', 'registrar'])
def upload_parent_document(parent_id):
    """Upload new document for parent"""
    data = request.get_json()
    data['parent_id'] = parent_id
    new_document = ParentDocument(**data)
    db.session.add(new_document)
    db.session.commit()
    return jsonify(new_document.to_dict()), 201

@parent_bp.route('/parents/documents/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'registrar'])
def update_document(id):
    """Update document details"""
    document = ParentDocument.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(document, key, value)
    db.session.commit()
    return jsonify(document.to_dict())

@parent_bp.route('/parents/documents/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_document(id):
    """Delete document"""
    document = ParentDocument.query.get_or_404(id)
    db.session.delete(document)
    db.session.commit()
    return '', 204 