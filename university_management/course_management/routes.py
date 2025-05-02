from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db, cache, limiter
from .utils import format_response
from .services import *

api_bp = Blueprint('api', __name__)


@api_bp.route('/courses', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_courses():
    """Get courses."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = CoursesService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Courses retrieved successfully'
    ))

@api_bp.route('/courses/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_courses_by_id(id):
    """Get courses by ID."""
    service = CoursesService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Courses retrieved successfully'
    ))

@api_bp.route('/courses', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_courses():
    """Create courses."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = CoursesService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Courses created successfully'
    )), 201

@api_bp.route('/courses/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_courses(id):
    """Update courses."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = CoursesService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Courses updated successfully'
    ))

@api_bp.route('/courses/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_courses(id):
    """Delete courses."""
    user_id = get_jwt_identity()
    
    service = CoursesService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Courses deleted successfully'
    ))

@api_bp.route('/sections', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_sections():
    """Get sections."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = SectionsService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Sections retrieved successfully'
    ))

@api_bp.route('/sections/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_sections_by_id(id):
    """Get sections by ID."""
    service = SectionsService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Sections retrieved successfully'
    ))

@api_bp.route('/sections', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_sections():
    """Create sections."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = SectionsService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Sections created successfully'
    )), 201

@api_bp.route('/sections/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_sections(id):
    """Update sections."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = SectionsService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Sections updated successfully'
    ))

@api_bp.route('/sections/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_sections(id):
    """Delete sections."""
    user_id = get_jwt_identity()
    
    service = SectionsService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Sections deleted successfully'
    ))

@api_bp.route('/schedule', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_schedule():
    """Get schedule."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = ScheduleService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Schedule retrieved successfully'
    ))

@api_bp.route('/schedule/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_schedule_by_id(id):
    """Get schedule by ID."""
    service = ScheduleService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Schedule retrieved successfully'
    ))

@api_bp.route('/schedule', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_schedule():
    """Create schedule."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = ScheduleService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Schedule created successfully'
    )), 201

@api_bp.route('/schedule/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_schedule(id):
    """Update schedule."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = ScheduleService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Schedule updated successfully'
    ))

@api_bp.route('/schedule/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_schedule(id):
    """Delete schedule."""
    user_id = get_jwt_identity()
    
    service = ScheduleService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Schedule deleted successfully'
    ))

@api_bp.route('/materials', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_materials():
    """Get materials."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = MaterialsService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Materials retrieved successfully'
    ))

@api_bp.route('/materials/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_materials_by_id(id):
    """Get materials by ID."""
    service = MaterialsService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Materials retrieved successfully'
    ))

@api_bp.route('/materials', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_materials():
    """Create materials."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = MaterialsService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Materials created successfully'
    )), 201

@api_bp.route('/materials/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_materials(id):
    """Update materials."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = MaterialsService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Materials updated successfully'
    ))

@api_bp.route('/materials/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_materials(id):
    """Delete materials."""
    user_id = get_jwt_identity()
    
    service = MaterialsService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Materials deleted successfully'
    ))

@api_bp.route('/assignments', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_assignments():
    """Get assignments."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = AssignmentsService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Assignments retrieved successfully'
    ))

@api_bp.route('/assignments/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_assignments_by_id(id):
    """Get assignments by ID."""
    service = AssignmentsService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Assignments retrieved successfully'
    ))

@api_bp.route('/assignments', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_assignments():
    """Create assignments."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = AssignmentsService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Assignments created successfully'
    )), 201

@api_bp.route('/assignments/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_assignments(id):
    """Update assignments."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = AssignmentsService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Assignments updated successfully'
    ))

@api_bp.route('/assignments/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_assignments(id):
    """Delete assignments."""
    user_id = get_jwt_identity()
    
    service = AssignmentsService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Assignments deleted successfully'
    ))

@api_bp.route('/grades', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_grades():
    """Get grades."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = GradesService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Grades retrieved successfully'
    ))

@api_bp.route('/grades/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_grades_by_id(id):
    """Get grades by ID."""
    service = GradesService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Grades retrieved successfully'
    ))

@api_bp.route('/grades', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_grades():
    """Create grades."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = GradesService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Grades created successfully'
    )), 201

@api_bp.route('/grades/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_grades(id):
    """Update grades."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = GradesService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Grades updated successfully'
    ))

@api_bp.route('/grades/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_grades(id):
    """Delete grades."""
    user_id = get_jwt_identity()
    
    service = GradesService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Grades deleted successfully'
    ))

@api_bp.route('/prerequisites', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_prerequisites():
    """Get prerequisites."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = PrerequisitesService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Prerequisites retrieved successfully'
    ))

@api_bp.route('/prerequisites/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_prerequisites_by_id(id):
    """Get prerequisites by ID."""
    service = PrerequisitesService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Prerequisites retrieved successfully'
    ))

@api_bp.route('/prerequisites', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_prerequisites():
    """Create prerequisites."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = PrerequisitesService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Prerequisites created successfully'
    )), 201

@api_bp.route('/prerequisites/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_prerequisites(id):
    """Update prerequisites."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = PrerequisitesService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Prerequisites updated successfully'
    ))

@api_bp.route('/prerequisites/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_prerequisites(id):
    """Delete prerequisites."""
    user_id = get_jwt_identity()
    
    service = PrerequisitesService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Prerequisites deleted successfully'
    ))

@api_bp.route('/enrollment', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_enrollment():
    """Get enrollment."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = EnrollmentService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Enrollment retrieved successfully'
    ))

@api_bp.route('/enrollment/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_enrollment_by_id(id):
    """Get enrollment by ID."""
    service = EnrollmentService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Enrollment retrieved successfully'
    ))

@api_bp.route('/enrollment', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_enrollment():
    """Create enrollment."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = EnrollmentService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Enrollment created successfully'
    )), 201

@api_bp.route('/enrollment/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_enrollment(id):
    """Update enrollment."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = EnrollmentService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Enrollment updated successfully'
    ))

@api_bp.route('/enrollment/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_enrollment(id):
    """Delete enrollment."""
    user_id = get_jwt_identity()
    
    service = EnrollmentService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Enrollment deleted successfully'
    ))

@api_bp.route('/evaluations', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_evaluations():
    """Get evaluations."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = EvaluationsService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Evaluations retrieved successfully'
    ))

@api_bp.route('/evaluations/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_evaluations_by_id(id):
    """Get evaluations by ID."""
    service = EvaluationsService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Evaluations retrieved successfully'
    ))

@api_bp.route('/evaluations', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_evaluations():
    """Create evaluations."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = EvaluationsService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Evaluations created successfully'
    )), 201

@api_bp.route('/evaluations/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_evaluations(id):
    """Update evaluations."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = EvaluationsService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Evaluations updated successfully'
    ))

@api_bp.route('/evaluations/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_evaluations(id):
    """Delete evaluations."""
    user_id = get_jwt_identity()
    
    service = EvaluationsService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Evaluations deleted successfully'
    ))
