from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Employee, LeaveRequest, PerformanceReview, TrainingProgram
from .. import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

hr_bp = Blueprint('hr', __name__)

# Employee Routes
@hr_bp.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    """Get all employees"""
    employees = Employee.query.all()
    return jsonify([employee.to_dict() for employee in employees])

@hr_bp.route('/employees/<int:id>', methods=['GET'])
@jwt_required()
def get_employee_by_id(id):
    """Get specific employee by ID"""
    employee = Employee.query.get_or_404(id)
    return jsonify(employee.to_dict())

@hr_bp.route('/employees', methods=['POST'])
@jwt_required()
@role_required(['admin', 'hr'])
def create_employee():
    """Create new employee"""
    data = request.get_json()
    new_employee = Employee(**data)
    db.session.add(new_employee)
    db.session.commit()
    return jsonify(new_employee.to_dict()), 201

@hr_bp.route('/employees/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'hr'])
def update_employee(id):
    """Update existing employee"""
    employee = Employee.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(employee, key, value)
    db.session.commit()
    return jsonify(employee.to_dict())

@hr_bp.route('/employees/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'hr'])
def delete_employee(id):
    """Delete employee"""
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return '', 204

# Leave Request Routes
@hr_bp.route('/leaves', methods=['GET'])
@jwt_required()
def get_leave_requests():
    """Get all leave requests"""
    leaves = LeaveRequest.query.all()
    return jsonify([leave.to_dict() for leave in leaves])

@hr_bp.route('/leaves', methods=['POST'])
@jwt_required()
def create_leave_request():
    """Create new leave request"""
    data = request.get_json()
    new_leave = LeaveRequest(**data)
    db.session.add(new_leave)
    db.session.commit()
    return jsonify(new_leave.to_dict()), 201

@hr_bp.route('/employees/<int:employee_id>/leaves', methods=['GET'])
@jwt_required()
def get_employee_leave_requests(employee_id):
    """Get leave requests for specific employee"""
    leaves = LeaveRequest.query.filter_by(employee_id=employee_id).all()
    return jsonify([leave.to_dict() for leave in leaves])

@hr_bp.route('/leaves/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'hr'])
def update_leave_request(id):
    """Update existing leave request"""
    leave = LeaveRequest.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(leave, key, value)
    db.session.commit()
    return jsonify(leave.to_dict())

@hr_bp.route('/leaves/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'hr'])
def delete_leave_request(id):
    """Delete leave request"""
    leave = LeaveRequest.query.get_or_404(id)
    db.session.delete(leave)
    db.session.commit()
    return '', 204

# Performance Review Routes
@hr_bp.route('/performance-reviews', methods=['GET'])
@jwt_required()
def get_performance_reviews():
    """Get all performance reviews"""
    reviews = PerformanceReview.query.all()
    return jsonify([review.to_dict() for review in reviews])

@hr_bp.route('/performance-reviews', methods=['POST'])
@jwt_required()
@role_required(['admin', 'hr'])
def create_performance_review():
    """Create new performance review"""
    data = request.get_json()
    new_review = PerformanceReview(**data)
    db.session.add(new_review)
    db.session.commit()
    return jsonify(new_review.to_dict()), 201

@hr_bp.route('/employees/<int:employee_id>/performance-reviews', methods=['GET'])
@jwt_required()
def get_employee_performance_reviews(employee_id):
    """Get performance reviews for specific employee"""
    reviews = PerformanceReview.query.filter_by(employee_id=employee_id).all()
    return jsonify([review.to_dict() for review in reviews])

@hr_bp.route('/performance-reviews/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'hr'])
def update_performance_review(id):
    """Update existing performance review"""
    review = PerformanceReview.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(review, key, value)
    db.session.commit()
    return jsonify(review.to_dict())

@hr_bp.route('/performance-reviews/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'hr'])
def delete_performance_review(id):
    """Delete performance review"""
    review = PerformanceReview.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return '', 204

@hr_bp.route('/reviewers/<int:reviewer_id>/performance-reviews', methods=['GET'])
@jwt_required()
def get_reviewer_performance_reviews(reviewer_id):
    """Get performance reviews given by specific reviewer"""
    reviews = PerformanceReview.query.filter_by(reviewer_id=reviewer_id).all()
    return jsonify([review.to_dict() for review in reviews])

# Training Program Routes
@hr_bp.route('/training-programs', methods=['GET'])
@jwt_required()
def get_training_programs():
    """Get all training programs"""
    programs = TrainingProgram.query.all()
    return jsonify([program.to_dict() for program in programs])

@hr_bp.route('/training-programs', methods=['POST'])
@jwt_required()
@role_required(['admin', 'hr'])
def create_training_program():
    """Create new training program"""
    data = request.get_json()
    new_program = TrainingProgram(**data)
    db.session.add(new_program)
    db.session.commit()
    return jsonify(new_program.to_dict()), 201

@hr_bp.route('/training-programs/<int:id>', methods=['GET'])
@jwt_required()
def get_training_program_by_id(id):
    """Get specific training program by ID"""
    program = TrainingProgram.query.get_or_404(id)
    return jsonify(program.to_dict())

@hr_bp.route('/training-programs/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'hr'])
def update_training_program(id):
    """Update existing training program"""
    program = TrainingProgram.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(program, key, value)
    db.session.commit()
    return jsonify(program.to_dict())

@hr_bp.route('/training-programs/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'hr'])
def delete_training_program(id):
    """Delete training program"""
    program = TrainingProgram.query.get_or_404(id)
    db.session.delete(program)
    db.session.commit()
    return '', 204 