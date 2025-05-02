from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db, cache, limiter
from .utils import format_response
from .services import *

api_bp = Blueprint('api', __name__)


@api_bp.route('/faculty', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_faculty():
    """Get faculty."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = FacultyService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Faculty retrieved successfully'
    ))

@api_bp.route('/faculty/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_faculty_by_id(id):
    """Get faculty by ID."""
    service = FacultyService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Faculty retrieved successfully'
    ))

@api_bp.route('/faculty', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_faculty():
    """Create faculty."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = FacultyService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Faculty created successfully'
    )), 201

@api_bp.route('/faculty/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_faculty(id):
    """Update faculty."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = FacultyService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Faculty updated successfully'
    ))

@api_bp.route('/faculty/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_faculty(id):
    """Delete faculty."""
    user_id = get_jwt_identity()
    
    service = FacultyService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Faculty deleted successfully'
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

@api_bp.route('/research', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_research():
    """Get research."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = ResearchService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Research retrieved successfully'
    ))

@api_bp.route('/research/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_research_by_id(id):
    """Get research by ID."""
    service = ResearchService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Research retrieved successfully'
    ))

@api_bp.route('/research', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_research():
    """Create research."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = ResearchService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Research created successfully'
    )), 201

@api_bp.route('/research/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_research(id):
    """Update research."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = ResearchService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Research updated successfully'
    ))

@api_bp.route('/research/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_research(id):
    """Delete research."""
    user_id = get_jwt_identity()
    
    service = ResearchService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Research deleted successfully'
    ))

@api_bp.route('/publications', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_publications():
    """Get publications."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = PublicationsService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Publications retrieved successfully'
    ))

@api_bp.route('/publications/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_publications_by_id(id):
    """Get publications by ID."""
    service = PublicationsService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Publications retrieved successfully'
    ))

@api_bp.route('/publications', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_publications():
    """Create publications."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = PublicationsService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Publications created successfully'
    )), 201

@api_bp.route('/publications/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_publications(id):
    """Update publications."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = PublicationsService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Publications updated successfully'
    ))

@api_bp.route('/publications/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_publications(id):
    """Delete publications."""
    user_id = get_jwt_identity()
    
    service = PublicationsService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Publications deleted successfully'
    ))

@api_bp.route('/grants', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_grants():
    """Get grants."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = GrantsService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Grants retrieved successfully'
    ))

@api_bp.route('/grants/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_grants_by_id(id):
    """Get grants by ID."""
    service = GrantsService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Grants retrieved successfully'
    ))

@api_bp.route('/grants', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_grants():
    """Create grants."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = GrantsService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Grants created successfully'
    )), 201

@api_bp.route('/grants/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_grants(id):
    """Update grants."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = GrantsService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Grants updated successfully'
    ))

@api_bp.route('/grants/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_grants(id):
    """Delete grants."""
    user_id = get_jwt_identity()
    
    service = GrantsService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Grants deleted successfully'
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

@api_bp.route('/development', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_development():
    """Get development."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = DevelopmentService()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='Development retrieved successfully'
    ))

@api_bp.route('/development/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_development_by_id(id):
    """Get development by ID."""
    service = DevelopmentService()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Development retrieved successfully'
    ))

@api_bp.route('/development', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_development():
    """Create development."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = DevelopmentService()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Development created successfully'
    )), 201

@api_bp.route('/development/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_development(id):
    """Update development."""
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = DevelopmentService()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='Development updated successfully'
    ))

@api_bp.route('/development/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_development(id):
    """Delete development."""
    user_id = get_jwt_identity()
    
    service = DevelopmentService()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='Development deleted successfully'
    ))
