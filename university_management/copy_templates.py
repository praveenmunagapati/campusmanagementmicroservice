import os
import shutil
from pathlib import Path

def copy_template_files(source_dir: str, target_dir: str) -> None:
    """Copy template files from source to target directory."""
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # List of files to copy
    files_to_copy = [
        '__init__.py',
        'config.py',
        'utils.py',
        'tests/conftest.py'
    ]
    
    # Copy each file
    for file in files_to_copy:
        source_path = os.path.join(source_dir, file)
        target_path = os.path.join(target_dir, file)
        
        # Create target directory if needed
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        # Copy file if it doesn't exist in target
        if not os.path.exists(target_path):
            shutil.copy2(source_path, target_path)
            print(f"Copied {file} to {target_dir}")

def copy_templates_to_all_microservices():
    """Copy template files to all microservices."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(base_path, 'templates', 'microservice_template')
    
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
            print(f"Copying templates to {service}...")
            copy_template_files(template_dir, service_path)
            print(f"Completed copying templates to {service}")

if __name__ == '__main__':
    copy_templates_to_all_microservices() 