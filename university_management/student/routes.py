from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db, cache, limiter
from .utils import format_response
from .services import *

api_bp = Blueprint('api', __name__)


@api_bp.route('/student', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student():
    """Get student."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = StudentService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Student retrieved successfully'
    ))

@api_bp.route('/student/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_student_by_id(id):
    """Get student by ID."""
    service = StudentService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student retrieved successfully'
    ))

@api_bp.route('/student', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_student():
    """Create student."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student created successfully'
    )), 201

@api_bp.route('/student/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_student(id):
    """Update student."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = StudentService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Student updated successfully'
    ))

@api_bp.route('/student/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_student(id):
    """Delete student."""
    user_id = get_jwt_identity()
    
    service = StudentService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Student deleted successfully'
    ))

@api_bp.route('/profile', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_profile():
    """Get profile."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = ProfileService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Profile retrieved successfully'
    ))

@api_bp.route('/profile/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_profile_by_id(id):
    """Get profile by ID."""
    service = ProfileService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Profile retrieved successfully'
    ))

@api_bp.route('/profile', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_profile():
    """Create profile."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = ProfileService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Profile created successfully'
    )), 201

@api_bp.route('/profile/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_profile(id):
    """Update profile."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = ProfileService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Profile updated successfully'
    ))

@api_bp.route('/profile/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_profile(id):
    """Delete profile."""
    user_id = get_jwt_identity()
    
    service = ProfileService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Profile deleted successfully'
    ))

@api_bp.route('/academic', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_academic():
    """Get academic."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = AcademicService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Academic retrieved successfully'
    ))

@api_bp.route('/academic/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_academic_by_id(id):
    """Get academic by ID."""
    service = AcademicService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Academic retrieved successfully'
    ))

@api_bp.route('/academic', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_academic():
    """Create academic."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = AcademicService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Academic created successfully'
    )), 201

@api_bp.route('/academic/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_academic(id):
    """Update academic."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = AcademicService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Academic updated successfully'
    ))

@api_bp.route('/academic/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_academic(id):
    """Delete academic."""
    user_id = get_jwt_identity()
    
    service = AcademicService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Academic deleted successfully'
    ))

@api_bp.route('/financial', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_financial():
    """Get financial."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = FinancialService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Financial retrieved successfully'
    ))

@api_bp.route('/financial/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_financial_by_id(id):
    """Get financial by ID."""
    service = FinancialService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Financial retrieved successfully'
    ))

@api_bp.route('/financial', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_financial():
    """Create financial."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = FinancialService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Financial created successfully'
    )), 201

@api_bp.route('/financial/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_financial(id):
    """Update financial."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = FinancialService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Financial updated successfully'
    ))

@api_bp.route('/financial/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_financial(id):
    """Delete financial."""
    user_id = get_jwt_identity()
    
    service = FinancialService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Financial deleted successfully'
    ))

@api_bp.route('/documents', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_documents():
    """Get documents."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = DocumentsService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Documents retrieved successfully'
    ))

@api_bp.route('/documents/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_documents_by_id(id):
    """Get documents by ID."""
    service = DocumentsService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Documents retrieved successfully'
    ))

@api_bp.route('/documents', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_documents():
    """Create documents."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = DocumentsService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Documents created successfully'
    )), 201

@api_bp.route('/documents/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_documents(id):
    """Update documents."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = DocumentsService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Documents updated successfully'
    ))

@api_bp.route('/documents/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_documents(id):
    """Delete documents."""
    user_id = get_jwt_identity()
    
    service = DocumentsService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Documents deleted successfully'
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

@api_bp.route('/attendance', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_attendance():
    """Get attendance."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = AttendanceService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Attendance retrieved successfully'
    ))

@api_bp.route('/attendance/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_attendance_by_id(id):
    """Get attendance by ID."""
    service = AttendanceService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Attendance retrieved successfully'
    ))

@api_bp.route('/attendance', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_attendance():
    """Create attendance."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = AttendanceService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Attendance created successfully'
    )), 201

@api_bp.route('/attendance/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_attendance(id):
    """Update attendance."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = AttendanceService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Attendance updated successfully'
    ))

@api_bp.route('/attendance/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_attendance(id):
    """Delete attendance."""
    user_id = get_jwt_identity()
    
    service = AttendanceService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Attendance deleted successfully'
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

@api_bp.route('/advising', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_advising():
    """Get advising."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = AdvisingService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Advising retrieved successfully'
    ))

@api_bp.route('/advising/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_advising_by_id(id):
    """Get advising by ID."""
    service = AdvisingService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Advising retrieved successfully'
    ))

@api_bp.route('/advising', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_advising():
    """Create advising."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = AdvisingService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Advising created successfully'
    )), 201

@api_bp.route('/advising/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_advising(id):
    """Update advising."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = AdvisingService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Advising updated successfully'
    ))

@api_bp.route('/advising/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_advising(id):
    """Delete advising."""
    user_id = get_jwt_identity()
    
    service = AdvisingService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Advising deleted successfully'
    ))

@api_bp.route('/services', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_services():
    """Get services."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = ServicesService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Services retrieved successfully'
    ))

@api_bp.route('/services/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_services_by_id(id):
    """Get services by ID."""
    service = ServicesService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Services retrieved successfully'
    ))

@api_bp.route('/services', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_services():
    """Create services."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = ServicesService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Services created successfully'
    )), 201

@api_bp.route('/services/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_services(id):
    """Update services."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = ServicesService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Services updated successfully'
    ))

@api_bp.route('/services/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_services(id):
    """Delete services."""
    user_id = get_jwt_identity()
    
    service = ServicesService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Services deleted successfully'
    ))

@api_bp.route('/complaints', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_complaints():
    """Get complaints."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = ComplaintsService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Complaints retrieved successfully'
    ))

@api_bp.route('/complaints/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_complaints_by_id(id):
    """Get complaints by ID."""
    service = ComplaintsService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Complaints retrieved successfully'
    ))

@api_bp.route('/complaints', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_complaints():
    """Create complaints."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = ComplaintsService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Complaints created successfully'
    )), 201

@api_bp.route('/complaints/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_complaints(id):
    """Update complaints."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = ComplaintsService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Complaints updated successfully'
    ))

@api_bp.route('/complaints/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_complaints(id):
    """Delete complaints."""
    user_id = get_jwt_identity()
    
    service = ComplaintsService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Complaints deleted successfully'
    ))

@api_bp.route('/feedback', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_feedback():
    """Get feedback."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = FeedbackService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Feedback retrieved successfully'
    ))

@api_bp.route('/feedback/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_feedback_by_id(id):
    """Get feedback by ID."""
    service = FeedbackService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Feedback retrieved successfully'
    ))

@api_bp.route('/feedback', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_feedback():
    """Create feedback."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = FeedbackService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Feedback created successfully'
    )), 201

@api_bp.route('/feedback/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_feedback(id):
    """Update feedback."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = FeedbackService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Feedback updated successfully'
    ))

@api_bp.route('/feedback/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_feedback(id):
    """Delete feedback."""
    user_id = get_jwt_identity()
    
    service = FeedbackService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Feedback deleted successfully'
    ))

@api_bp.route('/surveys', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_surveys():
    """Get surveys."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = SurveysService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Surveys retrieved successfully'
    ))

@api_bp.route('/surveys/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_surveys_by_id(id):
    """Get surveys by ID."""
    service = SurveysService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Surveys retrieved successfully'
    ))

@api_bp.route('/surveys', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_surveys():
    """Create surveys."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = SurveysService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Surveys created successfully'
    )), 201

@api_bp.route('/surveys/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_surveys(id):
    """Update surveys."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = SurveysService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Surveys updated successfully'
    ))

@api_bp.route('/surveys/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_surveys(id):
    """Delete surveys."""
    user_id = get_jwt_identity()
    
    service = SurveysService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Surveys deleted successfully'
    ))

@api_bp.route('/location', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_location():
    """Get location."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = LocationService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Location retrieved successfully'
    ))

@api_bp.route('/location/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_location_by_id(id):
    """Get location by ID."""
    service = LocationService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Location retrieved successfully'
    ))

@api_bp.route('/location', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_location():
    """Create location."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = LocationService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Location created successfully'
    )), 201

@api_bp.route('/location/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_location(id):
    """Update location."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = LocationService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Location updated successfully'
    ))

@api_bp.route('/location/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_location(id):
    """Delete location."""
    user_id = get_jwt_identity()
    
    service = LocationService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Location deleted successfully'
    ))

@api_bp.route('/contacts', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_contacts():
    """Get contacts."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = ContactsService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Contacts retrieved successfully'
    ))

@api_bp.route('/contacts/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_contacts_by_id(id):
    """Get contacts by ID."""
    service = ContactsService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Contacts retrieved successfully'
    ))

@api_bp.route('/contacts', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_contacts():
    """Create contacts."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = ContactsService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Contacts created successfully'
    )), 201

@api_bp.route('/contacts/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_contacts(id):
    """Update contacts."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = ContactsService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Contacts updated successfully'
    ))

@api_bp.route('/contacts/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_contacts(id):
    """Delete contacts."""
    user_id = get_jwt_identity()
    
    service = ContactsService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Contacts deleted successfully'
    ))

@api_bp.route('/emergency', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_emergency():
    """Get emergency."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = EmergencyService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Emergency retrieved successfully'
    ))

@api_bp.route('/emergency/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_emergency_by_id(id):
    """Get emergency by ID."""
    service = EmergencyService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Emergency retrieved successfully'
    ))

@api_bp.route('/emergency', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_emergency():
    """Create emergency."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = EmergencyService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Emergency created successfully'
    )), 201

@api_bp.route('/emergency/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_emergency(id):
    """Update emergency."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = EmergencyService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Emergency updated successfully'
    ))

@api_bp.route('/emergency/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_emergency(id):
    """Delete emergency."""
    user_id = get_jwt_identity()
    
    service = EmergencyService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Emergency deleted successfully'
    ))
