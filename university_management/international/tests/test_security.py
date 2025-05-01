import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import InternationalStudent, ExchangeProgram, ExchangeApplication, InternationalEvent, User
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestInternationalSecurity(unittest.TestCase):
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
        
        self.international_staff_user = User(
            username='international_staff',
            email='international@example.com',
            role='international_staff'
        )
        self.international_staff_user.set_password('international123')
        db.session.add(self.international_staff_user)
        
        self.faculty_user = User(
            username='faculty',
            email='faculty@example.com',
            role='faculty'
        )
        self.faculty_user.set_password('faculty123')
        db.session.add(self.faculty_user)
        
        self.student_user = User(
            username='student',
            email='student@example.com',
            role='student'
        )
        self.student_user.set_password('student123')
        db.session.add(self.student_user)
        
        db.session.commit()
        
        # Create access tokens
        self.admin_token = create_access_token(identity={
            'id': self.admin_user.id,
            'role': self.admin_user.role
        })
        
        self.international_staff_token = create_access_token(identity={
            'id': self.international_staff_user.id,
            'role': self.international_staff_user.role
        })
        
        self.faculty_token = create_access_token(identity={
            'id': self.faculty_user.id,
            'role': self.faculty_user.role
        })
        
        self.student_token = create_access_token(identity={
            'id': self.student_user.id,
            'role': self.student_user.role
        })
        
        self.client = self.app.test_client()
        self.admin_headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        self.international_staff_headers = {
            'Authorization': f'Bearer {self.international_staff_token}',
            'Content-Type': 'application/json'
        }
        self.faculty_headers = {
            'Authorization': f'Bearer {self.faculty_token}',
            'Content-Type': 'application/json'
        }
        self.student_headers = {
            'Authorization': f'Bearer {self.student_token}',
            'Content-Type': 'application/json'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_unauthorized_access(self):
        """Test access without authentication"""
        response = self.client.get('/api/v1/international/students')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/international/students', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_role_based_access(self):
        """Test role-based access control"""
        # Create an international student first
        student_data = {
            'student_id': str(self.student_user.id),
            'passport_number': 'P123456',
            'visa_type': 'F-1',
            'visa_expiry_date': '2024-12-31',
            'country_of_origin': 'Test Country',
            'arrival_date': '2024-01-01'
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/international/students',
            headers=self.admin_headers,
            data=json.dumps(student_data)
        )
        self.assertEqual(response.status_code, 201)
        student_id = json.loads(response.data)['data']['id']
        
        # International staff should be able to view and update
        response = self.client.get(
            f'/api/v1/international/students/{student_id}',
            headers=self.international_staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view
        response = self.client.get(
            f'/api/v1/international/students/{student_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view their own record
        response = self.client.get(
            f'/api/v1/international/students/{student_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should not be able to create
        response = self.client.post(
            '/api/v1/international/students',
            headers=self.faculty_headers,
            data=json.dumps(student_data)
        )
        self.assertEqual(response.status_code, 403)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/international/students',
            headers=self.student_headers,
            data=json.dumps(student_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_exchange_program_access(self):
        """Test exchange program access control"""
        # Create an exchange program
        program_data = {
            'name': 'Test Exchange Program',
            'partner_institution': 'Test University',
            'country': 'Test Country',
            'start_date': '2024-09-01',
            'end_date': '2025-05-31',
            'capacity': 10
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/international/programs',
            headers=self.admin_headers,
            data=json.dumps(program_data)
        )
        self.assertEqual(response.status_code, 201)
        program_id = json.loads(response.data)['data']['id']
        
        # International staff should be able to view
        response = self.client.get(
            f'/api/v1/international/programs/{program_id}',
            headers=self.international_staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view
        response = self.client.get(
            f'/api/v1/international/programs/{program_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            f'/api/v1/international/programs/{program_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_exchange_application_access(self):
        """Test exchange application access control"""
        # Create an exchange program first
        program_data = {
            'name': 'Test Exchange Program',
            'partner_institution': 'Test University',
            'country': 'Test Country',
            'start_date': '2024-09-01',
            'end_date': '2025-05-31',
            'capacity': 10
        }
        
        response = self.client.post(
            '/api/v1/international/programs',
            headers=self.admin_headers,
            data=json.dumps(program_data)
        )
        program_id = json.loads(response.data)['data']['id']
        
        # Create an application
        application_data = {
            'student_id': str(self.student_user.id),
            'program_id': program_id,
            'application_date': '2024-01-01',
            'documents': ['transcript.pdf', 'recommendation.pdf']
        }
        
        # Student should be able to create application
        response = self.client.post(
            '/api/v1/international/applications',
            headers=self.student_headers,
            data=json.dumps(application_data)
        )
        self.assertEqual(response.status_code, 201)
        application_id = json.loads(response.data)['data']['id']
        
        # International staff should be able to view
        response = self.client.get(
            f'/api/v1/international/applications/{application_id}',
            headers=self.international_staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view their own application
        response = self.client.get(
            f'/api/v1/international/applications/{application_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to view other students' applications
        response = self.client.get(
            f'/api/v1/international/applications/{application_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/international/students?search=1; DROP TABLE students; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in student data
        student_data = {
            'student_id': str(self.student_user.id),
            'passport_number': 'P123456',
            'visa_type': 'F-1',
            'visa_expiry_date': '2024-12-31',
            'country_of_origin': '<script>alert("xss")</script>',
            'arrival_date': '2024-01-01'
        }
        
        response = self.client.post(
            '/api/v1/international/students',
            headers=self.admin_headers,
            data=json.dumps(student_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # The response should have the script tags escaped
        response_data = json.loads(response.data)
        self.assertIn('&lt;script&gt;', response_data['data']['country_of_origin'])

    def test_rate_limiting(self):
        """Test rate limiting"""
        # Make multiple requests in quick succession
        for _ in range(100):
            response = self.client.get(
                '/api/v1/international/students',
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
        
        response = self.client.get('/api/v1/international/students', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 