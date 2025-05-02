from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db, cache, limiter
from .utils import format_response, paginate_query
from .exceptions import (
    ValidationError, NotFoundError, UnauthorizedError,
    ForbiddenError, ConflictError
)

api_bp = Blueprint('api', __name__)

@api_bp.before_request
def before_request():
    """Common operations before each request."""
    # Add request ID to context
    request_id = request.headers.get('X-Request-ID')
    if request_id:
        request.environ['request_id'] = request_id

@api_bp.after_request
def after_request(response):
    """Common operations after each request."""
    # Add CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    
    # Add request ID to response
    request_id = request.environ.get('request_id')
    if request_id:
        response.headers['X-Request-ID'] = request_id
    
    return response

@api_bp.errorhandler(ValidationError)
def handle_validation_error(error):
    """Handle validation errors."""
    return jsonify(format_response(
        data=None,
        message=error.message,
        status_code=400
    )), 400

@api_bp.errorhandler(NotFoundError)
def handle_not_found_error(error):
    """Handle not found errors."""
    return jsonify(format_response(
        data=None,
        message=error.message,
        status_code=404
    )), 404

@api_bp.errorhandler(UnauthorizedError)
def handle_unauthorized_error(error):
    """Handle unauthorized errors."""
    return jsonify(format_response(
        data=None,
        message=error.message,
        status_code=401
    )), 401

@api_bp.errorhandler(ForbiddenError)
def handle_forbidden_error(error):
    """Handle forbidden errors."""
    return jsonify(format_response(
        data=None,
        message=error.message,
        status_code=403
    )), 403

@api_bp.errorhandler(ConflictError)
def handle_conflict_error(error):
    """Handle conflict errors."""
    return jsonify(format_response(
        data=None,
        message=error.message,
        status_code=409
    )), 409

@api_bp.route('/health', methods=['GET'])
@cache.cached(timeout=60)
def health_check():
    """Health check endpoint."""
    return jsonify(format_response(
        data={'status': 'healthy'},
        message='Service is healthy'
    ))

@api_bp.route('/version', methods=['GET'])
@cache.cached(timeout=3600)
def version():
    """Version information endpoint."""
    return jsonify(format_response(
        data={
            'version': '1.0.0',
            'name': 'Microservice API'
        },
        message='Version information'
    ))

@api_bp.route('/audit-logs', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_audit_logs():
    """Get audit logs."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = db.session.query(AuditLog)
    paginated = paginate_query(query, page, per_page)
    
    return jsonify(format_response(
        data=paginated,
        message='Audit logs retrieved successfully'
    ))

@api_bp.route('/search', methods=['GET'])
@jwt_required()
@limiter.limit("200 per minute")
def search():
    """Search endpoint."""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Implement search logic here
    results = []
    
    return jsonify(format_response(
        data={
            'results': results,
            'total': len(results),
            'page': page,
            'per_page': per_page
        },
        message='Search completed successfully'
    )) 