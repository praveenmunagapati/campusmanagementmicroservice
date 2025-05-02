import os
import shutil
from pathlib import Path

def create_standard_structure(microservice_path):
    """Create standard directory structure for a microservice."""
    # Create main directories
    os.makedirs(os.path.join(microservice_path, 'tests'), exist_ok=True)
    os.makedirs(os.path.join(microservice_path, 'migrations', 'versions'), exist_ok=True)
    
    # Create empty files
    files_to_create = [
        '__init__.py',
        'config.py',
        'models.py',
        'schemas.py',
        'routes.py',
        'services.py',
        'utils.py',
        'exceptions.py',
        'requirements.txt',
        'README.md',
        'tests/__init__.py',
        'tests/conftest.py',
        'tests/test_models.py',
        'tests/test_schemas.py',
        'tests/test_routes.py',
        'tests/test_services.py',
        'migrations/env.py',
        'migrations/script.py.mako'
    ]
    
    for file in files_to_create:
        file_path = os.path.join(microservice_path, file)
        if not os.path.exists(file_path):
            Path(file_path).touch()

def standardize_all_microservices():
    """Standardize structure for all microservices."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    microservices = [
        'student', 'faculty', 'counseling', 'career_services', 'sports',
        'housing', 'security', 'alumni', 'transportation', 'research',
        'hr', 'governance', 'events', 'course_management', 'communication',
        'career', 'analytics', 'admissions', 'accommodation', 'health',
        'parent_portal', 'resources', 'sustainability', 'international',
        'finance', 'facilities', 'it_support', 'library', 'health_services',
        'student_records', 'academic', 'people'
    ]
    
    for service in microservices:
        service_path = os.path.join(base_path, service)
        if os.path.exists(service_path):
            print(f"Standardizing {service}...")
            create_standard_structure(service_path)
            print(f"Completed standardizing {service}")

if __name__ == '__main__':
    standardize_all_microservices() 