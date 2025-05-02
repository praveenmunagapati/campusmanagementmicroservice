import os
import shutil
from pathlib import Path
from typing import Dict, List

# Define microservice-specific models, schemas, and routes
MICROSERVICE_TEMPLATES = {
    'student': {
        'models': [
            'Student', 'StudentProfile', 'StudentAcademic', 'StudentFinancial',
            'StudentDocument', 'StudentEnrollment', 'StudentAttendance',
            'StudentGrade', 'StudentAdvising', 'StudentService',
            'StudentComplaint', 'StudentFeedback', 'StudentSurvey',
            'StudentLocation', 'StudentContact', 'StudentEmergency'
        ],
        'routes': [
            'student', 'profile', 'academic', 'financial', 'documents',
            'enrollment', 'attendance', 'grades', 'advising', 'services',
            'complaints', 'feedback', 'surveys', 'location', 'contacts',
            'emergency'
        ]
    },
    'faculty': {
        'models': [
            'Faculty', 'FacultyProfile', 'FacultyAcademic', 'FacultySchedule',
            'FacultyResearch', 'FacultyPublication', 'FacultyGrant',
            'FacultyAdvising', 'FacultyEvaluation', 'FacultyDevelopment'
        ],
        'routes': [
            'faculty', 'profile', 'academic', 'schedule', 'research',
            'publications', 'grants', 'advising', 'evaluations', 'development'
        ]
    },
    'course_management': {
        'models': [
            'Course', 'CourseSection', 'CourseSchedule', 'CourseMaterial',
            'CourseAssignment', 'CourseGrade', 'CoursePrerequisite',
            'CourseEnrollment', 'CourseEvaluation'
        ],
        'routes': [
            'courses', 'sections', 'schedule', 'materials', 'assignments',
            'grades', 'prerequisites', 'enrollment', 'evaluations'
        ]
    },
    # Add more microservices as needed
}

def generate_model_code(model_name: str) -> str:
    """Generate SQLAlchemy model code."""
    return f"""
class {model_name}(BaseModel):
    \"\"\"Model for {model_name}.\"\"\"
    __tablename__ = '{model_name.lower()}s'
    
    # Add model-specific fields here
    pass
"""

def generate_schema_code(schema_name: str) -> str:
    """Generate Marshmallow schema code."""
    return f"""
class {schema_name}Schema(BaseSchema):
    \"\"\"Schema for {schema_name}.\"\"\"
    # Add schema-specific fields here
    pass
"""

def generate_route_code(route_name: str) -> str:
    """Generate Flask route code."""
    return f"""
@api_bp.route('/{route_name}', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_{route_name}():
    \"\"\"Get {route_name}.\"\"\"
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    service = {route_name.capitalize()}Service()
    result = service.get_all(page, per_page)
    
    return jsonify(format_response(
        data=result,
        message='{route_name.capitalize()} retrieved successfully'
    ))

@api_bp.route('/{route_name}/<int:id>', methods=['GET'])
@jwt_required()
@limiter.limit("100 per minute")
def get_{route_name}_by_id(id):
    \"\"\"Get {route_name} by ID.\"\"\"
    service = {route_name.capitalize()}Service()
    result = service.get_by_id(id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='{route_name.capitalize()} retrieved successfully'
    ))

@api_bp.route('/{route_name}', methods=['POST'])
@jwt_required()
@limiter.limit("50 per minute")
def create_{route_name}():
    \"\"\"Create {route_name}.\"\"\"
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = {route_name.capitalize()}Service()
    result = service.create(data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='{route_name.capitalize()} created successfully'
    )), 201

@api_bp.route('/{route_name}/<int:id>', methods=['PUT'])
@jwt_required()
@limiter.limit("50 per minute")
def update_{route_name}(id):
    \"\"\"Update {route_name}.\"\"\"
    data = request.get_json()
    user_id = get_jwt_identity()
    
    service = {route_name.capitalize()}Service()
    result = service.update(id, data, user_id)
    
    return jsonify(format_response(
        data=result.to_dict(),
        message='{route_name.capitalize()} updated successfully'
    ))

@api_bp.route('/{route_name}/<int:id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("50 per minute")
def delete_{route_name}(id):
    \"\"\"Delete {route_name}.\"\"\"
    user_id = get_jwt_identity()
    
    service = {route_name.capitalize()}Service()
    service.delete(id, user_id)
    
    return jsonify(format_response(
        data=None,
        message='{route_name.capitalize()} deleted successfully'
    ))
"""

def generate_service_code(service_name: str) -> str:
    """Generate service class code."""
    return f"""
class {service_name}Service(BaseService):
    \"\"\"Service for {service_name} operations.\"\"\"
    
    def __init__(self):
        super().__init__({service_name})
    
    # Add service-specific methods here
    pass
"""

def generate_microservice_files(microservice_name: str, templates: Dict) -> None:
    """Generate files for a specific microservice."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    service_path = os.path.join(base_path, microservice_name)
    
    # Generate models.py
    with open(os.path.join(service_path, 'models.py'), 'w') as f:
        f.write('from datetime import datetime\n')
        f.write('from . import db\n')
        f.write('from .base_models import BaseModel\n\n')
        
        for model in templates['models']:
            f.write(generate_model_code(model))
    
    # Generate schemas.py
    with open(os.path.join(service_path, 'schemas.py'), 'w') as f:
        f.write('from marshmallow import Schema, fields, validate\n')
        f.write('from .base_schemas import BaseSchema\n\n')
        
        for model in templates['models']:
            f.write(generate_schema_code(model))
    
    # Generate routes.py
    with open(os.path.join(service_path, 'routes.py'), 'w') as f:
        f.write('from flask import Blueprint, request, jsonify\n')
        f.write('from flask_jwt_extended import jwt_required, get_jwt_identity\n')
        f.write('from . import db, cache, limiter\n')
        f.write('from .utils import format_response\n')
        f.write('from .services import *\n\n')
        f.write('api_bp = Blueprint(\'api\', __name__)\n\n')
        
        for route in templates['routes']:
            f.write(generate_route_code(route))
    
    # Generate services.py
    with open(os.path.join(service_path, 'services.py'), 'w') as f:
        f.write('from .base_services import BaseService\n')
        f.write('from .models import *\n\n')
        
        for model in templates['models']:
            f.write(generate_service_code(model))

def generate_all_microservices():
    """Generate files for all microservices."""
    for microservice_name, templates in MICROSERVICE_TEMPLATES.items():
        print(f"Generating files for {microservice_name}...")
        generate_microservice_files(microservice_name, templates)
        print(f"Completed generating files for {microservice_name}")

if __name__ == '__main__':
    generate_all_microservices() 