from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db, cache, limiter
from .utils import format_response, paginate_query
from .exceptions import (
    ValidationError, NotFoundError, UnauthorizedError,
    ForbiddenError, ConflictError
)
from .services import (
    StudentService, StudentProfileService, StudentAcademicService,
    StudentFinancialService, StudentDocumentService, StudentEnrollmentService,
    StudentAttendanceService, StudentGradeService, StudentAdvisingService,
    StudentServiceService, StudentComplaintService, StudentFeedbackService,
    StudentSurveyService, StudentLocationService, StudentContactService,
    StudentEmergencyService
)

api_bp = Blueprint('api', __name__)

# Student routes
@api_bp.route('/students', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_students():
    """Get all students."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = StudentService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Students retrieved successfully'
    ))

@api_bp.route('/students/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student(id):
    """Get student by ID."""
    service = StudentService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student retrieved successfully'
    ))

@api_bp.route('/students', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student():
    """Create a new student."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student created successfully'
    )), 201

@api_bp.route('/students/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student(id):
    """Update a student."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student updated successfully'
    ))

@api_bp.route('/students/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_student(id):
    """Delete a student."""
    user_id = get_jwt_identity()
    
    service = StudentService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Student deleted successfully'
    ))

# Student Profile routes
@api_bp.route('/students/<int:student_id>/profile', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_profile(student_id):
    """Get student profile."""
    service = StudentProfileService()
    result = service.get_by_student_id(student_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student profile retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/profile', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_profile(student_id):
    """Create student profile."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentProfileService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student profile created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/profile', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_profile(student_id):
    """Update student profile."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentProfileService()
    result = service.update(student_id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student profile updated successfully'
    ))

# Student Academic routes
@api_bp.route('/students/<int:student_id>/academic', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_academic(student_id):
    """Get student academic record."""
    service = StudentAcademicService()
    result = service.get_by_student_id(student_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student academic record retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/academic', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_academic(student_id):
    """Create student academic record."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentAcademicService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student academic record created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/academic', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_academic(student_id):
    """Update student academic record."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentAcademicService()
    result = service.update(student_id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student academic record updated successfully'
    ))

# Student Financial routes
@api_bp.route('/students/<int:student_id>/financial', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_financial(student_id):
    """Get student financial record."""
    service = StudentFinancialService()
    result = service.get_by_student_id(student_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student financial record retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/financial', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_financial(student_id):
    """Create student financial record."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentFinancialService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student financial record created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/financial', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_financial(student_id):
    """Update student financial record."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentFinancialService()
    result = service.update(student_id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student financial record updated successfully'
    ))

# Student Document routes
@api_bp.route('/students/<int:student_id>/documents', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_documents(student_id):
    """Get student documents."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = StudentDocumentService()
    result = service.get_by_student_id(student_id, page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Student documents retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/documents', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_document(student_id):
    """Create student document."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentDocumentService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student document created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/documents/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_document(student_id, id):
    """Update student document."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentDocumentService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student document updated successfully'
    ))

@api_bp.route('/students/<int:student_id>/documents/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_student_document(student_id, id):
    """Delete student document."""
    user_id = get_jwt_identity()
    
    service = StudentDocumentService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Student document deleted successfully'
    ))

# Student Enrollment routes
@api_bp.route('/students/<int:student_id>/enrollments', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_enrollments(student_id):
    """Get student enrollments."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = StudentEnrollmentService()
    result = service.get_by_student_id(student_id, page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Student enrollments retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/enrollments', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_enrollment(student_id):
    """Create student enrollment."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentEnrollmentService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student enrollment created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/enrollments/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_enrollment(student_id, id):
    """Update student enrollment."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentEnrollmentService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student enrollment updated successfully'
    ))

@api_bp.route('/students/<int:student_id>/enrollments/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_student_enrollment(student_id, id):
    """Delete student enrollment."""
    user_id = get_jwt_identity()
    
    service = StudentEnrollmentService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Student enrollment deleted successfully'
    ))

# Student Attendance routes
@api_bp.route('/students/<int:student_id>/attendance', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_attendance(student_id):
    """Get student attendance records."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = StudentAttendanceService()
    result = service.get_by_student_id(student_id, page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Student attendance records retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/attendance', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_attendance(student_id):
    """Create student attendance record."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentAttendanceService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student attendance record created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/attendance/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_attendance(student_id, id):
    """Update student attendance record."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentAttendanceService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student attendance record updated successfully'
    ))

# Student Grade routes
@api_bp.route('/students/<int:student_id>/grades', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_grades(student_id):
    """Get student grades."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = StudentGradeService()
    result = service.get_by_student_id(student_id, page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Student grades retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/grades', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_grade(student_id):
    """Create student grade."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentGradeService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student grade created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/grades/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_grade(student_id, id):
    """Update student grade."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentGradeService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student grade updated successfully'
    ))

# Student Advising routes
@api_bp.route('/students/<int:student_id>/advising', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_advising(student_id):
    """Get student advising records."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = StudentAdvisingService()
    result = service.get_by_student_id(student_id, page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Student advising records retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/advising', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_advising(student_id):
    """Create student advising record."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentAdvisingService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student advising record created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/advising/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_advising(student_id, id):
    """Update student advising record."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentAdvisingService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student advising record updated successfully'
    ))

# Student Service routes
@api_bp.route('/students/<int:student_id>/services', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_services(student_id):
    """Get student services."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = StudentServiceService()
    result = service.get_by_student_id(student_id, page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Student services retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/services', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_service(student_id):
    """Create student service record."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentServiceService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student service record created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/services/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_service(student_id, id):
    """Update student service record."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentServiceService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student service record updated successfully'
    ))

# Student Complaint routes
@api_bp.route('/students/<int:student_id>/complaints', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_complaints(student_id):
    """Get student complaints."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = StudentComplaintService()
    result = service.get_by_student_id(student_id, page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Student complaints retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/complaints', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_complaint(student_id):
    """Create student complaint."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentComplaintService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student complaint created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/complaints/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_complaint(student_id, id):
    """Update student complaint."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentComplaintService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student complaint updated successfully'
    ))

# Student Feedback routes
@api_bp.route('/students/<int:student_id>/feedback', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_feedback(student_id):
    """Get student feedback."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = StudentFeedbackService()
    result = service.get_by_student_id(student_id, page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Student feedback retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/feedback', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_feedback(student_id):
    """Create student feedback."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentFeedbackService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student feedback created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/feedback/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_feedback(student_id, id):
    """Update student feedback."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentFeedbackService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student feedback updated successfully'
    ))

# Student Survey routes
@api_bp.route('/students/<int:student_id>/surveys', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_surveys(student_id):
    """Get student surveys."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = StudentSurveyService()
    result = service.get_by_student_id(student_id, page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Student surveys retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/surveys', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_survey(student_id):
    """Create student survey response."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentSurveyService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student survey response created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/surveys/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_survey(student_id, id):
    """Update student survey response."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentSurveyService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student survey response updated successfully'
    ))

# Student Location routes
@api_bp.route('/students/<int:student_id>/locations', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_locations(student_id):
    """Get student locations."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = StudentLocationService()
    result = service.get_by_student_id(student_id, page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Student locations retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/locations', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_location(student_id):
    """Create student location record."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentLocationService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student location record created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/locations/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_location(student_id, id):
    """Update student location record."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentLocationService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student location record updated successfully'
    ))

# Student Contact routes
@api_bp.route('/students/<int:student_id>/contacts', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_contacts(student_id):
    """Get student contacts."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = StudentContactService()
    result = service.get_by_student_id(student_id, page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Student contacts retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/contacts', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_contact(student_id):
    """Create student contact."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentContactService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student contact created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/contacts/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_contact(student_id, id):
    """Update student contact."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentContactService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student contact updated successfully'
    ))

@api_bp.route('/students/<int:student_id>/contacts/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_student_contact(student_id, id):
    """Delete student contact."""
    user_id = get_jwt_identity()
    
    service = StudentContactService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Student contact deleted successfully'
    ))

# Student Emergency Contact routes
@api_bp.route('/students/<int:student_id>/emergency-contacts', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_emergency_contacts(student_id):
    """Get student emergency contacts."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = StudentEmergencyService()
    result = service.get_by_student_id(student_id, page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Student emergency contacts retrieved successfully'
    ))

@api_bp.route('/students/<int:student_id>/emergency-contacts', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student_emergency_contact(student_id):
    """Create student emergency contact."""
    data = request.get_json()
    data['student_id'] = student_id
    user_id = get_jwt_identity()
    
    service = StudentEmergencyService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student emergency contact created successfully'
    )), 201

@api_bp.route('/students/<int:student_id>/emergency-contacts/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student_emergency_contact(student_id, id):
    """Update student emergency contact."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentEmergencyService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student emergency contact updated successfully'
    ))

@api_bp.route('/students/<int:student_id>/emergency-contacts/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_student_emergency_contact(student_id, id):
    """Delete student emergency contact."""
    user_id = get_jwt_identity()
    
    service = StudentEmergencyService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Student emergency contact deleted successfully'
    ))
