from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Employee, Department, Position, Leave, Attendance, Payroll, Training, Performance, Recruitment, Document, Benefit
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

hr_bp = Blueprint('hr', __name__)

@hr_bp.route('/employees', methods=['GET'])
@jwt_required()
@role_required(['admin', 'hr_staff'])
def get_employees():
    """Get all employees with optional filters"""
    try:
        department_id = request.args.get('department_id')
        position_id = request.args.get('position_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Employee.query
        
        if department_id:
            query = query.filter_by(department_id=department_id)
        if position_id:
            query = query.filter_by(position_id=position_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Employee.hire_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Employee.hire_date <= datetime.fromisoformat(end_date))
        
        employees = query.all()
        return format_response([employee.to_dict() for employee in employees])
    except Exception as e:
        return handle_exception(e)

@hr_bp.route('/departments', methods=['GET'])
@jwt_required()
@role_required(['admin', 'hr_staff'])
def get_departments():
    """Get all departments with optional filters"""
    try:
        department_type = request.args.get('department_type')
        status = request.args.get('status')
        
        query = Department.query
        
        if department_type:
            query = query.filter_by(department_type=department_type)
        if status:
            query = query.filter_by(status=status)
        
        departments = query.all()
        return format_response([dept.to_dict() for dept in departments])
    except Exception as e:
        return handle_exception(e)

@hr_bp.route('/positions', methods=['GET'])
@jwt_required()
@role_required(['admin', 'hr_staff'])
def get_positions():
    """Get all positions with optional filters"""
    try:
        department_id = request.args.get('department_id')
        position_type = request.args.get('position_type')
        status = request.args.get('status')
        
        query = Position.query
        
        if department_id:
            query = query.filter_by(department_id=department_id)
        if position_type:
            query = query.filter_by(position_type=position_type)
        if status:
            query = query.filter_by(status=status)
        
        positions = query.all()
        return format_response([position.to_dict() for position in positions])
    except Exception as e:
        return handle_exception(e)

@hr_bp.route('/leaves', methods=['GET'])
@jwt_required()
@role_required(['admin', 'hr_staff'])
def get_leaves():
    """Get all leave records with optional filters"""
    try:
        employee_id = request.args.get('employee_id')
        leave_type = request.args.get('leave_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Leave.query
        
        if employee_id:
            query = query.filter_by(employee_id=employee_id)
        if leave_type:
            query = query.filter_by(leave_type=leave_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Leave.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Leave.end_date <= datetime.fromisoformat(end_date))
        
        leaves = query.all()
        return format_response([leave.to_dict() for leave in leaves])
    except Exception as e:
        return handle_exception(e)

@hr_bp.route('/attendance', methods=['GET'])
@jwt_required()
@role_required(['admin', 'hr_staff'])
def get_attendance():
    """Get all attendance records with optional filters"""
    try:
        employee_id = request.args.get('employee_id')
        attendance_type = request.args.get('attendance_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Attendance.query
        
        if employee_id:
            query = query.filter_by(employee_id=employee_id)
        if attendance_type:
            query = query.filter_by(attendance_type=attendance_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Attendance.date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Attendance.date <= datetime.fromisoformat(end_date))
        
        attendance_records = query.all()
        return format_response([record.to_dict() for record in attendance_records])
    except Exception as e:
        return handle_exception(e)

@hr_bp.route('/payroll', methods=['GET'])
@jwt_required()
@role_required(['admin', 'hr_staff'])
def get_payroll():
    """Get all payroll records with optional filters"""
    try:
        employee_id = request.args.get('employee_id')
        payroll_type = request.args.get('payroll_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Payroll.query
        
        if employee_id:
            query = query.filter_by(employee_id=employee_id)
        if payroll_type:
            query = query.filter_by(payroll_type=payroll_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Payroll.pay_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Payroll.pay_date <= datetime.fromisoformat(end_date))
        
        payroll_records = query.all()
        return format_response([record.to_dict() for record in payroll_records])
    except Exception as e:
        return handle_exception(e)

@hr_bp.route('/training', methods=['GET'])
@jwt_required()
@role_required(['admin', 'hr_staff'])
def get_training():
    """Get all training records with optional filters"""
    try:
        employee_id = request.args.get('employee_id')
        training_type = request.args.get('training_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Training.query
        
        if employee_id:
            query = query.filter_by(employee_id=employee_id)
        if training_type:
            query = query.filter_by(training_type=training_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Training.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Training.end_date <= datetime.fromisoformat(end_date))
        
        training_records = query.all()
        return format_response([record.to_dict() for record in training_records])
    except Exception as e:
        return handle_exception(e)

@hr_bp.route('/performance', methods=['GET'])
@jwt_required()
@role_required(['admin', 'hr_staff'])
def get_performance():
    """Get all performance records with optional filters"""
    try:
        employee_id = request.args.get('employee_id')
        review_type = request.args.get('review_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Performance.query
        
        if employee_id:
            query = query.filter_by(employee_id=employee_id)
        if review_type:
            query = query.filter_by(review_type=review_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Performance.review_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Performance.review_date <= datetime.fromisoformat(end_date))
        
        performance_records = query.all()
        return format_response([record.to_dict() for record in performance_records])
    except Exception as e:
        return handle_exception(e)

@hr_bp.route('/recruitment', methods=['GET'])
@jwt_required()
@role_required(['admin', 'hr_staff'])
def get_recruitment():
    """Get all recruitment records with optional filters"""
    try:
        position_id = request.args.get('position_id')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Recruitment.query
        
        if position_id:
            query = query.filter_by(position_id=position_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Recruitment.application_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Recruitment.application_date <= datetime.fromisoformat(end_date))
        
        recruitment_records = query.all()
        return format_response([record.to_dict() for record in recruitment_records])
    except Exception as e:
        return handle_exception(e)

@hr_bp.route('/documents', methods=['GET'])
@jwt_required()
@role_required(['admin', 'hr_staff'])
def get_documents():
    """Get all HR documents with optional filters"""
    try:
        employee_id = request.args.get('employee_id')
        document_type = request.args.get('document_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Document.query
        
        if employee_id:
            query = query.filter_by(employee_id=employee_id)
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

@hr_bp.route('/benefits', methods=['GET'])
@jwt_required()
@role_required(['admin', 'hr_staff'])
def get_benefits():
    """Get all benefits with optional filters"""
    try:
        employee_id = request.args.get('employee_id')
        benefit_type = request.args.get('benefit_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = Benefit.query
        
        if employee_id:
            query = query.filter_by(employee_id=employee_id)
        if benefit_type:
            query = query.filter_by(benefit_type=benefit_type)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            query = query.filter(Benefit.start_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Benefit.end_date <= datetime.fromisoformat(end_date))
        
        benefits = query.all()
        return format_response([benefit.to_dict() for benefit in benefits])
    except Exception as e:
        return handle_exception(e) 