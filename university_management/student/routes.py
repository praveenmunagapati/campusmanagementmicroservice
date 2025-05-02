from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    Student, StudentProfile, StudentAcademic,
    StudentFinancial, StudentDocument,
    StudentEnrollment, StudentAttendance,
    StudentGrade, StudentAdvising,
    StudentService, StudentComplaint,
    StudentFeedback, StudentSurvey,
    StudentLocation, StudentContact,
    StudentEmergency
)
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

student_bp = Blueprint('student', __name__)

@student_bp.route('/students', methods=['GET'])
@jwt_required()
@role_required(['admin', 'student_manager'])
def get_students():
    """Get all students with optional filters"""
    try:
        student_type = request.args.get('student_type')
        program = request.args.get('program')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Student.query
        
        if student_type:
            query = query.filter_by(student_type=student_type)
        if program:
            query = query.filter_by(program=program)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Student.enrollment_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Student.enrollment_date <= datetime.fromisoformat(end_date))
        
        students = query.all()
        return format_response([student.to_dict() for student in students])
    except Exception as e:
        return handle_exception(e)

@student_bp.route('/profiles', methods=['GET'])
@jwt_required()
@role_required(['admin', 'student_manager'])
def get_profiles():
    """Get all student profiles with optional filters"""
    try:
        student_id = request.args.get('student_id')
        nationality = request.args.get('nationality')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = StudentProfile.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if nationality:
            query = query.filter_by(nationality=nationality)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(StudentProfile.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(StudentProfile.created_at <= datetime.fromisoformat(end_date))
        
        profiles = query.all()
        return format_response([profile.to_dict() for profile in profiles])
    except Exception as e:
        return handle_exception(e)

@student_bp.route('/academic', methods=['GET'])
@jwt_required()
@role_required(['admin', 'student_manager'])
def get_academic():
    """Get all student academic records with optional filters"""
    try:
        student_id = request.args.get('student_id')
        program = request.args.get('program')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = StudentAcademic.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if program:
            query = query.filter_by(program=program)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(StudentAcademic.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(StudentAcademic.end_date <= datetime.fromisoformat(end_date))
        
        records = query.all()
        return format_response([record.to_dict() for record in records])
    except Exception as e:
        return handle_exception(e)

@student_bp.route('/financial', methods=['GET'])
@jwt_required()
@role_required(['admin', 'student_manager'])
def get_financial():
    """Get all student financial records with optional filters"""
    try:
        student_id = request.args.get('student_id')
        payment_type = request.args.get('payment_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = StudentFinancial.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if payment_type:
            query = query.filter_by(payment_type=payment_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(StudentFinancial.payment_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(StudentFinancial.payment_date <= datetime.fromisoformat(end_date))
        
        records = query.all()
        return format_response([record.to_dict() for record in records])
    except Exception as e:
        return handle_exception(e)

@student_bp.route('/documents', methods=['GET'])
@jwt_required()
@role_required(['admin', 'student_manager'])
def get_documents():
    """Get all student documents with optional filters"""
    try:
        student_id = request.args.get('student_id')
        document_type = request.args.get('document_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = StudentDocument.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if document_type:
            query = query.filter_by(document_type=document_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(StudentDocument.upload_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(StudentDocument.upload_date <= datetime.fromisoformat(end_date))
        
        documents = query.all()
        return format_response([document.to_dict() for document in documents])
    except Exception as e:
        return handle_exception(e)

@student_bp.route('/enrollments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'student_manager'])
def get_enrollments():
    """Get all student enrollments with optional filters"""
    try:
        student_id = request.args.get('student_id')
        course = request.args.get('course')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = StudentEnrollment.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if course:
            query = query.filter_by(course=course)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(StudentEnrollment.enrollment_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(StudentEnrollment.enrollment_date <= datetime.fromisoformat(end_date))
        
        enrollments = query.all()
        return format_response([enrollment.to_dict() for enrollment in enrollments])
    except Exception as e:
        return handle_exception(e)

@student_bp.route('/attendance', methods=['GET'])
@jwt_required()
@role_required(['admin', 'student_manager'])
def get_attendance():
    """Get all student attendance records with optional filters"""
    try:
        student_id = request.args.get('student_id')
        course = request.args.get('course')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = StudentAttendance.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if course:
            query = query.filter_by(course=course)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(StudentAttendance.attendance_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(StudentAttendance.attendance_date <= datetime.fromisoformat(end_date))
        
        records = query.all()
        return format_response([record.to_dict() for record in records])
    except Exception as e:
        return handle_exception(e)

@student_bp.route('/grades', methods=['GET'])
@jwt_required()
@role_required(['admin', 'student_manager'])
def get_grades():
    """Get all student grades with optional filters"""
    try:
        student_id = request.args.get('student_id')
        course = request.args.get('course')
        grade_type = request.args.get('grade_type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = StudentGrade.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if course:
            query = query.filter_by(course=course)
        if grade_type:
            query = query.filter_by(grade_type=grade_type)
        if start_date:
            query = query.filter(StudentGrade.grade_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(StudentGrade.grade_date <= datetime.fromisoformat(end_date))
        
        grades = query.all()
        return format_response([grade.to_dict() for grade in grades])
    except Exception as e:
        return handle_exception(e)

@student_bp.route('/advising', methods=['GET'])
@jwt_required()
@role_required(['admin', 'student_manager'])
def get_advising():
    """Get all student advising records with optional filters"""
    try:
        student_id = request.args.get('student_id')
        advisor_id = request.args.get('advisor_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = StudentAdvising.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if advisor_id:
            query = query.filter_by(advisor_id=advisor_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(StudentAdvising.advising_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(StudentAdvising.advising_date <= datetime.fromisoformat(end_date))
        
        records = query.all()
        return format_response([record.to_dict() for record in records])
    except Exception as e:
        return handle_exception(e)

@student_bp.route('/services', methods=['GET'])
@jwt_required()
@role_required(['admin', 'student_manager'])
def get_services():
    """Get all student services with optional filters"""
    try:
        student_id = request.args.get('student_id')
        service_type = request.args.get('service_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = StudentService.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if service_type:
            query = query.filter_by(service_type=service_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(StudentService.service_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(StudentService.service_date <= datetime.fromisoformat(end_date))
        
        services = query.all()
        return format_response([service.to_dict() for service in services])
    except Exception as e:
        return handle_exception(e)

@student_bp.route('/complaints', methods=['GET'])
@jwt_required()
@role_required(['admin', 'student_manager'])
def get_complaints():
    """Get all student complaints with optional filters"""
    try:
        student_id = request.args.get('student_id')
        complaint_type = request.args.get('complaint_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = StudentComplaint.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if complaint_type:
            query = query.filter_by(complaint_type=complaint_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(StudentComplaint.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(StudentComplaint.created_at <= datetime.fromisoformat(end_date))
        
        complaints = query.all()
        return format_response([complaint.to_dict() for complaint in complaints])
    except Exception as e:
        return handle_exception(e)

@student_bp.route('/feedback', methods=['GET'])
@jwt_required()
@role_required(['admin', 'student_manager'])
def get_feedback():
    """Get all student feedback with optional filters"""
    try:
        student_id = request.args.get('student_id')
        feedback_type = request.args.get('feedback_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = StudentFeedback.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if feedback_type:
            query = query.filter_by(feedback_type=feedback_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(StudentFeedback.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(StudentFeedback.created_at <= datetime.fromisoformat(end_date))
        
        feedback = query.all()
        return format_response([item.to_dict() for item in feedback])
    except Exception as e:
        return handle_exception(e)

@student_bp.route('/surveys', methods=['GET'])
@jwt_required()
@role_required(['admin', 'student_manager'])
def get_surveys():
    """Get all student surveys with optional filters"""
    try:
        student_id = request.args.get('student_id')
        survey_type = request.args.get('survey_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = StudentSurvey.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        if survey_type:
            query = query.filter_by(survey_type=survey_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(StudentSurvey.created_at >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(StudentSurvey.created_at <= datetime.fromisoformat(end_date))
        
        surveys = query.all()
        return format_response([survey.to_dict() for survey in surveys])
    except Exception as e:
        return handle_exception(e) 