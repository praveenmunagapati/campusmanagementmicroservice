import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Accommodation, Room, RoomAssignment, MaintenanceRequest, User, Student
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestAccommodationSecurity(unittest.TestCase):
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
        
        self.staff_user = User(
            username='staff',
            email='staff@example.com',
            role='staff'
        )
        self.staff_user.set_password('staff123')
        db.session.add(self.staff_user)
        
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
        
        self.staff_token = create_access_token(identity={
            'id': self.staff_user.id,
            'role': self.staff_user.role
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
        self.staff_headers = {
            'Authorization': f'Bearer {self.staff_token}',
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
        response = self.client.get('/api/v1/accommodation/accommodations')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/accommodation/accommodations', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_role_based_access(self):
        """Test role-based access control"""
        # Create an accommodation first
        accommodation_data = {
            'name': 'Test Dorm',
            'type': 'dorm',
            'capacity': 100,
            'location': 'Campus A',
            'description': 'Test Description',
            'amenities': ['wifi', 'laundry'],
            'monthly_rent': 500.00
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/accommodation/accommodations',
            headers=self.admin_headers,
            data=json.dumps(accommodation_data)
        )
        self.assertEqual(response.status_code, 201)
        accommodation_id = json.loads(response.data)['data']['id']
        
        # Staff should be able to view
        response = self.client.get(
            f'/api/v1/accommodation/accommodations/{accommodation_id}',
            headers=self.staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            f'/api/v1/accommodation/accommodations/{accommodation_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/accommodation/accommodations',
            headers=self.student_headers,
            data=json.dumps(accommodation_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_room_access(self):
        """Test room access control"""
        # Create a room
        room_data = {
            'accommodation_id': 1,
            'room_number': '101',
            'room_type': 'single',
            'capacity': 1
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/accommodation/rooms',
            headers=self.admin_headers,
            data=json.dumps(room_data)
        )
        self.assertEqual(response.status_code, 201)
        room_id = json.loads(response.data)['data']['id']
        
        # Staff should be able to view
        response = self.client.get(
            f'/api/v1/accommodation/rooms/{room_id}',
            headers=self.staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            f'/api/v1/accommodation/rooms/{room_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/accommodation/rooms',
            headers=self.student_headers,
            data=json.dumps(room_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_maintenance_access(self):
        """Test maintenance request access control"""
        # Create a maintenance request
        maintenance_data = {
            'room_id': 1,
            'student_id': self.student.id,
            'request_type': 'plumbing',
            'description': 'Leaking faucet',
            'priority': 'medium'
        }
        
        # Student should be able to create
        response = self.client.post(
            '/api/v1/accommodation/maintenance',
            headers=self.student_headers,
            data=json.dumps(maintenance_data)
        )
        self.assertEqual(response.status_code, 201)
        maintenance_id = json.loads(response.data)['data']['id']
        
        # Staff should be able to view and update
        response = self.client.get(
            f'/api/v1/accommodation/maintenance/{maintenance_id}',
            headers=self.staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view their own requests
        response = self.client.get(
            f'/api/v1/accommodation/maintenance/{maintenance_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to update status
        response = self.client.put(
            f'/api/v1/accommodation/maintenance/{maintenance_id}/status',
            headers=self.student_headers,
            data=json.dumps({'status': 'completed'})
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/accommodation/accommodations?search=1; DROP TABLE accommodations; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in accommodation data
        accommodation_data = {
            'name': '<script>alert("xss")</script>',
            'type': 'dorm',
            'capacity': 100,
            'location': 'Campus A',
            'description': 'Test Description',
            'amenities': ['wifi', 'laundry'],
            'monthly_rent': 500.00
        }
        
        response = self.client.post(
            '/api/v1/accommodation/accommodations',
            headers=self.admin_headers,
            data=json.dumps(accommodation_data)
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
                '/api/v1/accommodation/accommodations',
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
        
        response = self.client.get('/api/v1/accommodation/accommodations', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 