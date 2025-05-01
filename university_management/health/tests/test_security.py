import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import HealthRecord, Immunization, HealthAppointment, User, Student
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestHealthSecurity(unittest.TestCase):
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
        
        self.health_staff_user = User(
            username='health_staff',
            email='health@example.com',
            role='health_staff'
        )
        self.health_staff_user.set_password('health123')
        db.session.add(self.health_staff_user)
        
        self.student_user = User(
            username='student',
            email='student@example.com',
            role='student'
        )
        self.student_user.set_password('student123')
        db.session.add(self.student_user)
        
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
        
        self.health_staff_token = create_access_token(identity={
            'id': self.health_staff_user.id,
            'role': self.health_staff_user.role
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
        self.health_staff_headers = {
            'Authorization': f'Bearer {self.health_staff_token}',
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
        response = self.client.get('/api/v1/health/records')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/health/records', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_role_based_access(self):
        """Test role-based access control"""
        # Create a health record first
        record_data = {
            'student_id': self.student.id,
            'record_type': 'medical',
            'date': '2024-01-01',
            'description': 'Test Description',
            'diagnosis': 'Test Diagnosis',
            'treatment': 'Test Treatment',
            'medication': 'Test Medication'
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/health/records',
            headers=self.admin_headers,
            data=json.dumps(record_data)
        )
        self.assertEqual(response.status_code, 201)
        record_id = json.loads(response.data)['data']['id']
        
        # Health staff should be able to view
        response = self.client.get(
            f'/api/v1/health/records/{record_id}',
            headers=self.health_staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view their own records
        response = self.client.get(
            f'/api/v1/health/records/{record_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to create records
        response = self.client.post(
            '/api/v1/health/records',
            headers=self.student_headers,
            data=json.dumps(record_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_immunization_access(self):
        """Test immunization access control"""
        # Create an immunization record
        immunization_data = {
            'student_id': self.student.id,
            'vaccine_name': 'Test Vaccine',
            'date_administered': '2024-01-01',
            'next_due_date': '2025-01-01',
            'provider': 'Test Provider',
            'batch_number': 'BATCH123'
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/health/immunizations',
            headers=self.admin_headers,
            data=json.dumps(immunization_data)
        )
        self.assertEqual(response.status_code, 201)
        immunization_id = json.loads(response.data)['data']['id']
        
        # Health staff should be able to view
        response = self.client.get(
            f'/api/v1/health/immunizations/{immunization_id}',
            headers=self.health_staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view their own immunizations
        response = self.client.get(
            f'/api/v1/health/immunizations/{immunization_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to create immunizations
        response = self.client.post(
            '/api/v1/health/immunizations',
            headers=self.student_headers,
            data=json.dumps(immunization_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_appointment_access(self):
        """Test health appointment access control"""
        # Create an appointment
        appointment_data = {
            'student_id': self.student.id,
            'staff_id': self.health_staff_user.id,
            'appointment_type': 'checkup',
            'appointment_date': '2024-01-01T10:00:00',
            'duration': 30,
            'reason': 'Test Reason'
        }
        
        # Health staff should be able to create
        response = self.client.post(
            '/api/v1/health/appointments',
            headers=self.health_staff_headers,
            data=json.dumps(appointment_data)
        )
        self.assertEqual(response.status_code, 201)
        appointment_id = json.loads(response.data)['data']['id']
        
        # Student should be able to view their appointments
        response = self.client.get(
            '/api/v1/health/appointments',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Only health staff should be able to mark appointments as completed
        response = self.client.put(
            f'/api/v1/health/appointments/{appointment_id}/complete',
            headers=self.health_staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to mark appointments as completed
        response = self.client.put(
            f'/api/v1/health/appointments/{appointment_id}/complete',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/health/records?search=1; DROP TABLE health_records; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in health record data
        record_data = {
            'student_id': self.student.id,
            'record_type': 'medical',
            'date': '2024-01-01',
            'description': '<script>alert("xss")</script>',
            'diagnosis': 'Test Diagnosis',
            'treatment': 'Test Treatment'
        }
        
        response = self.client.post(
            '/api/v1/health/records',
            headers=self.admin_headers,
            data=json.dumps(record_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # The response should have the script tags escaped
        response_data = json.loads(response.data)
        self.assertIn('&lt;script&gt;', response_data['data']['description'])

    def test_rate_limiting(self):
        """Test rate limiting"""
        # Make multiple requests in quick succession
        for _ in range(100):
            response = self.client.get(
                '/api/v1/health/records',
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
        
        response = self.client.get('/api/v1/health/records', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 