import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Application, Document, Interview, User, Student
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestAdmissionsSecurity(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test users with different roles
        self.admin_user = User(
            username='admin',
            email='admin@example.com',
            role='admin'
        )
        self.admin_user.set_password('admin123')
        db.session.add(self.admin_user)
        
        self.admissions_staff_user = User(
            username='admissions_staff',
            email='admissions@example.com',
            role='admissions_staff'
        )
        self.admissions_staff_user.set_password('admissions123')
        db.session.add(self.admissions_staff_user)
        
        self.applicant_user = User(
            username='applicant',
            email='applicant@example.com',
            role='applicant'
        )
        self.applicant_user.set_password('applicant123')
        db.session.add(self.applicant_user)
        
        # Create a test student
        self.student = Student(
            name='Test Student',
            email='student@example.com',
            student_id='ST12345'
        )
        db.session.add(self.student)
        
        db.session.commit()
        
        # Create access tokens
        self.admin_token = create_access_token(identity={
            'id': self.admin_user.id,
            'role': self.admin_user.role
        })
        
        self.admissions_staff_token = create_access_token(identity={
            'id': self.admissions_staff_user.id,
            'role': self.admissions_staff_user.role
        })
        
        self.applicant_token = create_access_token(identity={
            'id': self.applicant_user.id,
            'role': self.applicant_user.role
        })
        
        self.client = self.app.test_client()
        self.admin_headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        self.admissions_staff_headers = {
            'Authorization': f'Bearer {self.admissions_staff_token}',
            'Content-Type': 'application/json'
        }
        self.applicant_headers = {
            'Authorization': f'Bearer {self.applicant_token}',
            'Content-Type': 'application/json'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_unauthorized_access(self):
        """Test access without authentication"""
        response = self.client.get('/api/v1/admissions/applications')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/admissions/applications', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_role_based_access(self):
        """Test role-based access control"""
        # Create an application first
        application_data = {
            'applicant_id': self.applicant_user.id,
            'program': 'Computer Science',
            'status': 'pending',
            'submission_date': '2024-01-01'
        }
        
        # Applicant should be able to create
        response = self.client.post(
            '/api/v1/admissions/applications',
            headers=self.applicant_headers,
            data=json.dumps(application_data)
        )
        self.assertEqual(response.status_code, 201)
        application_id = json.loads(response.data)['data']['id']
        
        # Admissions staff should be able to view
        response = self.client.get(
            f'/api/v1/admissions/applications/{application_id}',
            headers=self.admissions_staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Applicant should be able to view their own application
        response = self.client.get(
            f'/api/v1/admissions/applications/{application_id}',
            headers=self.applicant_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Only admissions staff should be able to update status
        response = self.client.put(
            f'/api/v1/admissions/applications/{application_id}/status',
            headers=self.admissions_staff_headers,
            data=json.dumps({'status': 'under_review'})
        )
        self.assertEqual(response.status_code, 200)
        
        # Applicant should not be able to update status
        response = self.client.put(
            f'/api/v1/admissions/applications/{application_id}/status',
            headers=self.applicant_headers,
            data=json.dumps({'status': 'accepted'})
        )
        self.assertEqual(response.status_code, 403)

    def test_document_access(self):
        """Test document access control"""
        # Create a document
        document_data = {
            'application_id': 1,
            'document_type': 'transcript',
            'file_path': '/path/to/file.pdf',
            'status': 'pending'
        }
        
        # Applicant should be able to upload
        response = self.client.post(
            '/api/v1/admissions/documents',
            headers=self.applicant_headers,
            data=json.dumps(document_data)
        )
        self.assertEqual(response.status_code, 201)
        document_id = json.loads(response.data)['data']['id']
        
        # Admissions staff should be able to view
        response = self.client.get(
            f'/api/v1/admissions/documents/{document_id}',
            headers=self.admissions_staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Applicant should be able to view their own documents
        response = self.client.get(
            f'/api/v1/admissions/documents/{document_id}',
            headers=self.applicant_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Only admissions staff should be able to verify documents
        response = self.client.put(
            f'/api/v1/admissions/documents/{document_id}/verify',
            headers=self.admissions_staff_headers,
            data=json.dumps({'status': 'verified'})
        )
        self.assertEqual(response.status_code, 200)

    def test_interview_access(self):
        """Test interview access control"""
        # Create an interview
        interview_data = {
            'application_id': 1,
            'interviewer_id': self.admissions_staff_user.id,
            'scheduled_date': '2024-02-01T10:00:00',
            'duration': 60,
            'status': 'scheduled'
        }
        
        # Admissions staff should be able to create
        response = self.client.post(
            '/api/v1/admissions/interviews',
            headers=self.admissions_staff_headers,
            data=json.dumps(interview_data)
        )
        self.assertEqual(response.status_code, 201)
        interview_id = json.loads(response.data)['data']['id']
        
        # Applicant should be able to view their interviews
        response = self.client.get(
            f'/api/v1/admissions/interviews/{interview_id}',
            headers=self.applicant_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Only admissions staff should be able to update interview results
        response = self.client.put(
            f'/api/v1/admissions/interviews/{interview_id}/results',
            headers=self.admissions_staff_headers,
            data=json.dumps({'result': 'passed', 'notes': 'Good performance'})
        )
        self.assertEqual(response.status_code, 200)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/admissions/applications?search=1; DROP TABLE applications; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in application data
        application_data = {
            'applicant_id': self.applicant_user.id,
            'program': '<script>alert("xss")</script>',
            'status': 'pending',
            'submission_date': '2024-01-01'
        }
        
        response = self.client.post(
            '/api/v1/admissions/applications',
            headers=self.applicant_headers,
            data=json.dumps(application_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # The response should have the script tags escaped
        response_data = json.loads(response.data)
        self.assertIn('&lt;script&gt;', response_data['data']['program'])

    def test_rate_limiting(self):
        """Test rate limiting"""
        # Make multiple requests in quick succession
        for _ in range(100):
            response = self.client.get(
                '/api/v1/admissions/applications',
                headers=self.admin_headers
            )
            if response.status_code == 429:
                break
        
        # Should eventually get rate limited
        self.assertEqual(response.status_code, 429)

    def test_token_expiration(self):
        """Test token expiration"""
        # Create a token with very short expiration
        expired_token = create_access_token(
            identity={
                'id': self.admin_user.id,
                'role': self.admin_user.role
            },
            expires_delta=datetime.timedelta(seconds=1)
        )
        
        headers = {
            'Authorization': f'Bearer {expired_token}',
            'Content-Type': 'application/json'
        }
        
        # Wait for token to expire
        time.sleep(2)
        
        response = self.client.get('/api/v1/admissions/applications', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 