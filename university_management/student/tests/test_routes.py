import pytest
from datetime import datetime, timedelta
from flask import jsonify
from .. import models
from ..routes import student_bp

def test_get_students(client, auth_headers, student_data):
    """Test GET /students route"""
    response = client.get('/students', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student(client, auth_headers, student_data):
    """Test GET /students/<student_id> route"""
    response = client.get('/students/ST001', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_profile(client, auth_headers, student_profile_data):
    """Test GET /students/<student_id>/profile route"""
    response = client.get('/students/ST001/profile', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_academic(client, auth_headers, student_academic_data):
    """Test GET /students/<student_id>/academic route"""
    response = client.get('/students/ST001/academic', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_financial(client, auth_headers, student_financial_data):
    """Test GET /students/<student_id>/financial route"""
    response = client.get('/students/ST001/financial', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_documents(client, auth_headers, student_document_data):
    """Test GET /students/<student_id>/documents route"""
    response = client.get('/students/ST001/documents', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_enrollments(client, auth_headers, student_enrollment_data):
    """Test GET /students/<student_id>/enrollments route"""
    response = client.get('/students/ST001/enrollments', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_attendance(client, auth_headers, student_attendance_data):
    """Test GET /students/<student_id>/attendance route"""
    response = client.get('/students/ST001/attendance', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_grades(client, auth_headers, student_grade_data):
    """Test GET /students/<student_id>/grades route"""
    response = client.get('/students/ST001/grades', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_advising(client, auth_headers, student_advising_data):
    """Test GET /students/<student_id>/advising route"""
    response = client.get('/students/ST001/advising', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_services(client, auth_headers, student_service_data):
    """Test GET /students/<student_id>/services route"""
    response = client.get('/students/ST001/services', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_complaints(client, auth_headers, student_complaint_data):
    """Test GET /students/<student_id>/complaints route"""
    response = client.get('/students/ST001/complaints', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_feedback(client, auth_headers, student_feedback_data):
    """Test GET /students/<student_id>/feedback route"""
    response = client.get('/students/ST001/feedback', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_surveys(client, auth_headers, student_survey_data):
    """Test GET /students/<student_id>/surveys route"""
    response = client.get('/students/ST001/surves', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_locations(client, auth_headers, student_location_data):
    """Test GET /students/<student_id>/locations route"""
    response = client.get('/students/ST001/locations', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_contacts(client, auth_headers, student_contact_data):
    """Test GET /students/<student_id>/contacts route"""
    response = client.get('/students/ST001/contacts', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_get_student_emergencies(client, auth_headers, student_emergency_data):
    """Test GET /students/<student_id>/emergencies route"""
    response = client.get('/students/ST001/emergencies', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'message' in data
    assert data['message'] == 'Success'

def test_unauthorized_access(client):
    """Test unauthorized access to protected routes"""
    response = client.get('/students')
    assert response.status_code == 401

def test_invalid_role_access(client, auth_headers):
    """Test access with invalid role"""
    response = client.get('/students', headers=auth_headers)
    assert response.status_code == 403

def test_invalid_student_id(client, auth_headers):
    """Test access with invalid student ID"""
    response = client.get('/students/INVALID', headers=auth_headers)
    assert response.status_code == 404

def test_invalid_date_format(client, auth_headers):
    """Test access with invalid date format"""
    response = client.get('/students?start_date=invalid', headers=auth_headers)
    assert response.status_code == 400

def test_pagination(client, auth_headers):
    """Test pagination functionality"""
    response = client.get('/students?page=1&per_page=10', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert 'pagination' in data
    assert 'total' in data['pagination']
    assert 'pages' in data['pagination']
    assert 'current_page' in data['pagination']

def test_filtering(client, auth_headers):
    """Test filtering functionality"""
    response = client.get('/students?status=active&student_type=undergraduate', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert all(item['status'] == 'active' for item in data['data'])
    assert all(item['student_type'] == 'undergraduate' for item in data['data'])

def test_date_range_filtering(client, auth_headers):
    """Test date range filtering"""
    start_date = (datetime.now() - timedelta(days=30)).isoformat()
    end_date = datetime.now().isoformat()
    response = client.get(f'/students?start_date={start_date}&end_date={end_date}', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert all(
        start_date <= item['enrollment_date'] <= end_date
        for item in data['data']
    ) 