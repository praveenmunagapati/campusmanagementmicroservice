import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta
import os

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    # Initialize extensions
    db = SQLAlchemy(app)
    jwt = JWTManager(app)

    # Create tables
    with app.app_context():
        db.create_all()

    yield app

    # Clean up
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def db(app):
    """Database fixture."""
    from flask_sqlalchemy import SQLAlchemy
    return SQLAlchemy(app)

@pytest.fixture
def student_data():
    """Sample student data for testing."""
    return {
        'student_id': 'ST001',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'student_type': 'undergraduate',
        'program': 'Computer Science',
        'enrollment_date': datetime.now(),
        'status': 'active'
    }

@pytest.fixture
def student_profile_data():
    """Sample student profile data for testing."""
    return {
        'nationality': 'American',
        'date_of_birth': datetime(1995, 1, 1),
        'gender': 'male',
        'address': '123 Main St',
        'city': 'New York',
        'state': 'NY',
        'zip_code': '10001',
        'country': 'USA',
        'status': 'active'
    }

@pytest.fixture
def student_academic_data():
    """Sample student academic data for testing."""
    return {
        'program': 'Computer Science',
        'major': 'Software Engineering',
        'minor': 'Mathematics',
        'start_date': datetime.now(),
        'expected_graduation': datetime.now() + timedelta(days=365),
        'gpa': 3.5,
        'status': 'active'
    }

@pytest.fixture
def student_financial_data():
    """Sample student financial data for testing."""
    return {
        'payment_type': 'tuition',
        'amount': 5000.00,
        'payment_date': datetime.now(),
        'status': 'paid'
    }

@pytest.fixture
def student_document_data():
    """Sample student document data for testing."""
    return {
        'document_type': 'transcript',
        'file_name': 'transcript.pdf',
        'file_path': '/documents/transcript.pdf',
        'upload_date': datetime.now(),
        'status': 'verified'
    }

@pytest.fixture
def student_enrollment_data():
    """Sample student enrollment data for testing."""
    return {
        'course': 'CS101',
        'section': 'A',
        'semester': 'Fall 2023',
        'enrollment_date': datetime.now(),
        'status': 'enrolled'
    }

@pytest.fixture
def student_attendance_data():
    """Sample student attendance data for testing."""
    return {
        'course': 'CS101',
        'attendance_date': datetime.now(),
        'status': 'present'
    }

@pytest.fixture
def student_grade_data():
    """Sample student grade data for testing."""
    return {
        'course': 'CS101',
        'grade': 'A',
        'grade_points': 4.0,
        'grade_date': datetime.now()
    }

@pytest.fixture
def student_advising_data():
    """Sample student advising data for testing."""
    return {
        'advisor_id': 'AD001',
        'advising_date': datetime.now(),
        'notes': 'Regular academic advising session',
        'status': 'completed'
    }

@pytest.fixture
def student_service_data():
    """Sample student service data for testing."""
    return {
        'service_type': 'counseling',
        'service_date': datetime.now(),
        'notes': 'Career counseling session',
        'status': 'completed'
    }

@pytest.fixture
def student_complaint_data():
    """Sample student complaint data for testing."""
    return {
        'complaint_type': 'academic',
        'description': 'Issue with course grading',
        'status': 'pending'
    }

@pytest.fixture
def student_feedback_data():
    """Sample student feedback data for testing."""
    return {
        'feedback_type': 'course',
        'rating': 4,
        'comments': 'Great course content and instructor'
    }

@pytest.fixture
def student_survey_data():
    """Sample student survey data for testing."""
    return {
        'survey_type': 'course_evaluation',
        'responses': {
            'q1': 'Excellent',
            'q2': 'Good',
            'q3': 'Very Good'
        }
    }

@pytest.fixture
def student_location_data():
    """Sample student location data for testing."""
    return {
        'location_type': 'residence',
        'building': 'Dorm A',
        'room': '101',
        'status': 'active'
    }

@pytest.fixture
def student_contact_data():
    """Sample student contact data for testing."""
    return {
        'contact_type': 'emergency',
        'name': 'Jane Doe',
        'relationship': 'Parent',
        'phone': '0987654321',
        'email': 'jane.doe@example.com'
    }

@pytest.fixture
def student_emergency_data():
    """Sample student emergency data for testing."""
    return {
        'emergency_type': 'medical',
        'description': 'Student reported feeling unwell',
        'occurred_at': datetime.now(),
        'status': 'active'
    }

@pytest.fixture
def auth_headers():
    """Generate authentication headers for testing."""
    return {
        'Authorization': 'Bearer test-token'
    } 