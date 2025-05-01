import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Resource, ResourceBooking, ResourceMaintenance, User
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestResourcesSecurity(unittest.TestCase):
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
        
        self.resource_manager_user = User(
            username='resource_manager',
            email='resource@example.com',
            role='resource_manager'
        )
        self.resource_manager_user.set_password('resource123')
        db.session.add(self.resource_manager_user)
        
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
        
        self.resource_manager_token = create_access_token(identity={
            'id': self.resource_manager_user.id,
            'role': self.resource_manager_user.role
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
        self.resource_manager_headers = {
            'Authorization': f'Bearer {self.resource_manager_token}',
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
        response = self.client.get('/api/v1/resources/resources')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/resources/resources', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_role_based_access(self):
        """Test role-based access control"""
        # Create a resource first
        resource_data = {
            'name': 'Test Resource',
            'description': 'Test Description',
            'category': 'equipment',
            'quantity': 1,
            'location': 'Room 101'
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/resources/resources',
            headers=self.admin_headers,
            data=json.dumps(resource_data)
        )
        self.assertEqual(response.status_code, 201)
        resource_id = json.loads(response.data)['data']['id']
        
        # Resource manager should be able to view and update
        response = self.client.get(
            f'/api/v1/resources/resources/{resource_id}',
            headers=self.resource_manager_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view
        response = self.client.get(
            f'/api/v1/resources/resources/{resource_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            f'/api/v1/resources/resources/{resource_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should not be able to create
        response = self.client.post(
            '/api/v1/resources/resources',
            headers=self.faculty_headers,
            data=json.dumps(resource_data)
        )
        self.assertEqual(response.status_code, 403)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/resources/resources',
            headers=self.student_headers,
            data=json.dumps(resource_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_booking_access(self):
        """Test resource booking access control"""
        # Create a resource first
        resource_data = {
            'name': 'Test Resource',
            'description': 'Test Description',
            'category': 'equipment',
            'quantity': 1,
            'location': 'Room 101'
        }
        
        response = self.client.post(
            '/api/v1/resources/resources',
            headers=self.admin_headers,
            data=json.dumps(resource_data)
        )
        resource_id = json.loads(response.data)['data']['id']
        
        # Create a booking
        booking_data = {
            'resource_id': resource_id,
            'start_time': '2024-01-01T10:00:00',
            'end_time': '2024-01-01T11:00:00',
            'purpose': 'Test Purpose'
        }
        
        # Faculty should be able to create booking
        response = self.client.post(
            '/api/v1/resources/bookings',
            headers=self.faculty_headers,
            data=json.dumps(booking_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # Student should be able to create booking
        response = self.client.post(
            '/api/v1/resources/bookings',
            headers=self.student_headers,
            data=json.dumps(booking_data)
        )
        self.assertEqual(response.status_code, 201)

    def test_maintenance_access(self):
        """Test maintenance access control"""
        # Create a resource first
        resource_data = {
            'name': 'Test Resource',
            'description': 'Test Description',
            'category': 'equipment',
            'quantity': 1,
            'location': 'Room 101'
        }
        
        response = self.client.post(
            '/api/v1/resources/resources',
            headers=self.admin_headers,
            data=json.dumps(resource_data)
        )
        resource_id = json.loads(response.data)['data']['id']
        
        # Create maintenance record
        maintenance_data = {
            'resource_id': resource_id,
            'maintenance_type': 'repair',
            'description': 'Test Maintenance',
            'start_date': '2024-01-01T10:00:00',
            'end_date': '2024-01-01T11:00:00',
            'cost': 100.00,
            'technician': 'John Doe'
        }
        
        # Admin should be able to create maintenance
        response = self.client.post(
            '/api/v1/resources/maintenance',
            headers=self.admin_headers,
            data=json.dumps(maintenance_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # Resource manager should be able to create maintenance
        response = self.client.post(
            '/api/v1/resources/maintenance',
            headers=self.resource_manager_headers,
            data=json.dumps(maintenance_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # Faculty should not be able to create maintenance
        response = self.client.post(
            '/api/v1/resources/maintenance',
            headers=self.faculty_headers,
            data=json.dumps(maintenance_data)
        )
        self.assertEqual(response.status_code, 403)
        
        # Student should not be able to create maintenance
        response = self.client.post(
            '/api/v1/resources/maintenance',
            headers=self.student_headers,
            data=json.dumps(maintenance_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/resources/resources?search=1; DROP TABLE resources; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in resource data
        resource_data = {
            'name': '<script>alert("xss")</script>',
            'description': 'Test Description',
            'category': 'equipment',
            'quantity': 1,
            'location': 'Room 101'
        }
        
        response = self.client.post(
            '/api/v1/resources/resources',
            headers=self.admin_headers,
            data=json.dumps(resource_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # The response should have the script tags escaped
        response_data = json.loads(response.data)
        self.assertIn('&lt;script&gt;', response_data['data']['name'])

    def test_rate_limiting(self):
        """Test rate limiting"""
        # Make multiple requests in quick succession
        for _ in range(100):
            response = self.client.get(
                '/api/v1/resources/resources',
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
        
        response = self.client.get('/api/v1/resources/resources', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 