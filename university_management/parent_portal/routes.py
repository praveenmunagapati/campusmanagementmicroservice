from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    Parent, StudentParent, ParentNotification, ParentAccessLog,
    ParentMeeting, ParentFeedback, ParentDocument, ParentMessage,
    Student, Communication, Attendance, Grade, Payment, Document, Notification, Meeting, Permission
)
from .. import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

parent_bp = Blueprint('parent', __name__)
parent_portal_bp = Blueprint('parent_portal', __name__)

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

# Parent Portal Routes
@parent_portal_bp.route('/parents', methods=['GET'])
@jwt_required()
@role_required(['admin', 'parent'])
def get_parents():
    """Get all parents with optional filters"""
    try:
        parent_id = request.args.get('parent_id')
        student_id = request.args.get('student_id')
        status = request.args.get('status')
        
        query = Parent.query
        
        if parent_id:
            query = query.filter_by(id=parent_id)
        if student_id:
            query = query.join(Student).filter(Student.id == student_id)
        if status:
            query = query.filter_by(status=status)
        
        parents = query.all()
        return format_response([parent.to_dict() for parent in parents])
    except Exception as e:
        return handle_exception(e)

@parent_portal_bp.route('/students', methods=['GET'])
@jwt_required()
@role_required(['admin', 'parent'])
def get_students():
    """Get all students with optional filters"""
    try:
        parent_id = request.args.get('parent_id')
        grade_level = request.args.get('grade_level')
        status = request.args.get('status')
        
        query = Student.query
        
        if parent_id:
            query = query.join(Parent).filter(Parent.id == parent_id)
        if grade_level:
            query = query.filter_by(grade_level=grade_level)
        if status:
            query = query.filter_by(status=status)
        
        students = query.all()
        return format_response([student.to_dict() for student in students])
    except Exception as e:
        return handle_exception(e)

@parent_portal_bp.route('/communications', methods=['GET'])
@jwt_required()
@role_required(['admin', 'parent'])
def get_communications():
    """Get all communications with optional filters"""
    try:
        parent_id = request.args.get('parent_id')
        student_id = request.args.get('student_id')
        communication_type = request.args.get('communication_type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Communication.query
        
        if parent_id:
            query = query.filter_by(parent_id=parent_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if communication_type:
            query = query.filter_by(communication_type=communication_type)
        if start_date:
            query = query.filter(Communication.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Communication.date <= datetime.fromisoformat(end_date))
        
        communications = query.all()
        return format_response([comm.to_dict() for comm in communications])
    except Exception as e:
        return handle_exception(e)

@parent_portal_bp.route('/attendance', methods=['GET'])
@jwt_required()
@role_required(['admin', 'parent'])
def get_attendance():
    """Get all attendance records with optional filters"""
    try:
        student_id = request.args.get('student_id')
        attendance_type = request.args.get('attendance_type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Attendance.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if attendance_type:
            query = query.filter_by(attendance_type=attendance_type)
        if start_date:
            query = query.filter(Attendance.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Attendance.date <= datetime.fromisoformat(end_date))
        
        attendance_records = query.all()
        return format_response([record.to_dict() for record in attendance_records])
    except Exception as e:
        return handle_exception(e)

@parent_portal_bp.route('/grades', methods=['GET'])
@jwt_required()
@role_required(['admin', 'parent'])
def get_grades():
    """Get all grades with optional filters"""
    try:
        student_id = request.args.get('student_id')
        subject = request.args.get('subject')
        term = request.args.get('term')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Grade.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if subject:
            query = query.filter_by(subject=subject)
        if term:
            query = query.filter_by(term=term)
        if start_date:
            query = query.filter(Grade.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Grade.date <= datetime.fromisoformat(end_date))
        
        grades = query.all()
        return format_response([grade.to_dict() for grade in grades])
    except Exception as e:
        return handle_exception(e)

@parent_portal_bp.route('/payments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'parent'])
def get_payments():
    """Get all payments with optional filters"""
    try:
        student_id = request.args.get('student_id')
        payment_type = request.args.get('payment_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Payment.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if payment_type:
            query = query.filter_by(payment_type=payment_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Payment.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Payment.date <= datetime.fromisoformat(end_date))
        
        payments = query.all()
        return format_response([payment.to_dict() for payment in payments])
    except Exception as e:
        return handle_exception(e)

@parent_portal_bp.route('/documents', methods=['GET'])
@jwt_required()
@role_required(['admin', 'parent'])
def get_documents():
    """Get all documents with optional filters"""
    try:
        student_id = request.args.get('student_id')
        document_type = request.args.get('document_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Document.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if document_type:
            query = query.filter_by(document_type=document_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Document.upload_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Document.upload_date <= datetime.fromisoformat(end_date))
        
        documents = query.all()
        return format_response([doc.to_dict() for doc in documents])
    except Exception as e:
        return handle_exception(e)

@parent_portal_bp.route('/notifications', methods=['GET'])
@jwt_required()
@role_required(['admin', 'parent'])
def get_notifications():
    """Get all notifications with optional filters"""
    try:
        parent_id = request.args.get('parent_id')
        notification_type = request.args.get('notification_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Notification.query
        
        if parent_id:
            query = query.filter_by(parent_id=parent_id)
        if notification_type:
            query = query.filter_by(notification_type=notification_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Notification.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Notification.date <= datetime.fromisoformat(end_date))
        
        notifications = query.all()
        return format_response([notif.to_dict() for notif in notifications])
    except Exception as e:
        return handle_exception(e)

@parent_portal_bp.route('/meetings', methods=['GET'])
@jwt_required()
@role_required(['admin', 'parent'])
def get_meetings():
    """Get all meetings with optional filters"""
    try:
        parent_id = request.args.get('parent_id')
        student_id = request.args.get('student_id')
        meeting_type = request.args.get('meeting_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Meeting.query
        
        if parent_id:
            query = query.filter_by(parent_id=parent_id)
        if student_id:
            query = query.filter_by(student_id=student_id)
        if meeting_type:
            query = query.filter_by(meeting_type=meeting_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Meeting.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Meeting.date <= datetime.fromisoformat(end_date))
        
        meetings = query.all()
        return format_response([meeting.to_dict() for meeting in meetings])
    except Exception as e:
        return handle_exception(e)

@parent_portal_bp.route('/permissions', methods=['GET'])
@jwt_required()
@role_required(['admin', 'parent'])
def get_permissions():
    """Get all permissions with optional filters"""
    try:
        student_id = request.args.get('student_id')
        permission_type = request.args.get('permission_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Permission.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if permission_type:
            query = query.filter_by(permission_type=permission_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Permission.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Permission.date <= datetime.fromisoformat(end_date))
        
        permissions = query.all()
        return format_response([perm.to_dict() for perm in permissions])
    except Exception as e:
        return handle_exception(e)

# Parent Message Routes
@parent_portal_bp.route('/messages', methods=['GET'])
@jwt_required()
def get_messages():
    """Get all parent messages"""
    parent_id = request.args.get('parent_id')
    recipient_id = request.args.get('recipient_id')
    status = request.args.get('status')
    
    query = ParentMessage.query
    
    if parent_id:
        query = query.filter_by(parent_id=parent_id)
    if recipient_id:
        query = query.filter_by(recipient_id=recipient_id)
    if status:
        query = query.filter_by(status=status)
    
    messages = query.all()
    return jsonify({
        'status': 'success',
        'data': [message.to_dict() for message in messages]
    }), 200

@parent_portal_bp.route('/messages', methods=['POST'])
@jwt_required()
def create_message():
    """Create new parent message"""
    data = request.get_json()
    
    message = ParentMessage(
        parent_id=get_jwt_identity()['id'],
        recipient_id=data['recipient_id'],
        subject=data['subject'],
        message=data['message'],
        status='unread'
    )
    
    db.session.add(message)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': message.to_dict()
    }), 201

# Parent Meeting Routes
@parent_portal_bp.route('/meetings', methods=['GET'])
@jwt_required()
def get_meetings():
    """Get all parent meetings"""
    parent_id = request.args.get('parent_id')
    staff_id = request.args.get('staff_id')
    student_id = request.args.get('student_id')
    status = request.args.get('status')
    
    query = ParentMeeting.query
    
    if parent_id:
        query = query.filter_by(parent_id=parent_id)
    if staff_id:
        query = query.filter_by(staff_id=staff_id)
    if student_id:
        query = query.filter_by(student_id=student_id)
    if status:
        query = query.filter_by(status=status)
    
    meetings = query.all()
    return jsonify({
        'status': 'success',
        'data': [meeting.to_dict() for meeting in meetings]
    }), 200

@parent_portal_bp.route('/meetings', methods=['POST'])
@jwt_required()
def create_meeting():
    """Create new parent meeting"""
    data = request.get_json()
    
    meeting = ParentMeeting(
        parent_id=data['parent_id'],
        staff_id=data['staff_id'],
        student_id=data['student_id'],
        meeting_date=datetime.strptime(data['meeting_date'], '%Y-%m-%dT%H:%M:%S'),
        duration=data.get('duration'),
        purpose=data.get('purpose'),
        status='scheduled',
        notes=data.get('notes')
    )
    
    db.session.add(meeting)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': meeting.to_dict()
    }), 201

@parent_portal_bp.route('/meetings/<int:id>/complete', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'staff'])
def complete_meeting(id):
    """Mark meeting as completed"""
    meeting = ParentMeeting.query.get_or_404(id)
    meeting.status = 'completed'
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': meeting.to_dict()
    }), 200 