from flask import Blueprint, jsonify, request
from .models import Course, CourseSchedule, CourseMaterial
from .. import db

course_bp = Blueprint('course', __name__)

@course_bp.route('/courses', methods=['GET'])
def get_courses():
    """Get all courses"""
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses])

@course_bp.route('/courses/<int:id>', methods=['GET'])
def get_course_by_id(id):
    """Get specific course by ID"""
    course = Course.query.get_or_404(id)
    return jsonify(course.to_dict())

@course_bp.route('/courses', methods=['POST'])
def create_course():
    """Create new course"""
    data = request.get_json()
    new_course = Course(**data)
    db.session.add(new_course)
    db.session.commit()
    return jsonify(new_course.to_dict()), 201

@course_bp.route('/courses/<int:id>', methods=['PUT'])
def update_course(id):
    """Update existing course"""
    course = Course.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(course, key, value)
    db.session.commit()
    return jsonify(course.to_dict())

@course_bp.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    """Delete course"""
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return '', 204

@course_bp.route('/courses/schedule', methods=['GET'])
def get_course_schedules():
    """Get all course schedules"""
    schedules = CourseSchedule.query.all()
    return jsonify([schedule.to_dict() for schedule in schedules])

@course_bp.route('/courses/materials', methods=['GET'])
def get_course_materials():
    """Get all course materials"""
    materials = CourseMaterial.query.all()
    return jsonify([material.to_dict() for material in materials])

@course_bp.route('/courses/<int:course_id>/materials', methods=['GET'])
def get_course_materials_by_course(course_id):
    """Get materials for specific course"""
    materials = CourseMaterial.query.filter_by(course_id=course_id).all()
    return jsonify([material.to_dict() for material in materials])

@course_bp.route('/courses/prerequisites', methods=['GET'])
def get_course_prerequisites():
    """Get course prerequisites"""
    courses = Course.query.filter(Course.prerequisites != None).all()
    return jsonify([course.to_dict() for course in courses]) 