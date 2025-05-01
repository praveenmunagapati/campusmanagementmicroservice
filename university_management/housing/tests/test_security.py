import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Residence, Room, RoomAssignment, User
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestHousingSecurity(unittest.TestCase):
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
        
        self.housing_staff_user = User(
            username='housing_staff',
            email='housing@example.com',
            role='housing_staff'
        )
        self.housing_staff_user.set_password('housing123')
        db.session.add(self.housing_staff_user)
        
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
        
        self.housing_staff_token = create_access_token(identity={
            'id': self.housing_staff_user.id,
            'role': self.housing_staff_user.role
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
        self.housing_staff_headers = {
            'Authorization': f'Bearer {self.housing_staff_token}',
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
        response = self.client.get('/api/v1/housing/residences')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/housing/residences', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_role_based_access(self):
        """Test role-based access control"""
        # Create a residence first
        residence_data = {
            'name': 'Test Residence',
            'address': '123 Test St',
            'capacity': 100,
            'type': 'dormitory'
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/housing/residences',
            headers=self.admin_headers,
            data=json.dumps(residence_data)
        )
        self.assertEqual(response.status_code, 201)
        residence_id = json.loads(response.data)['data']['id']
        
        # Housing staff should be able to view and update
        response = self.client.get(
            f'/api/v1/housing/residences/{residence_id}',
            headers=self.housing_staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view
        response = self.client.get(
            f'/api/v1/housing/residences/{residence_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            f'/api/v1/housing/residences/{residence_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should not be able to create
        response = self.client.post(
            '/api/v1/housing/residences',
            headers=self.faculty_headers,
            data=json.dumps(residence_data)
        )
        self.assertEqual(response.status_code, 403)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/housing/residences',
            headers=self.student_headers,
            data=json.dumps(residence_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_room_assignment_access(self):
        """Test room assignment access control"""
        # Create a residence first
        residence_data = {
            'name': 'Test Residence',
            'address': '123 Test St',
            'capacity': 100,
            'type': 'dormitory'
        }
        
        response = self.client.post(
            '/api/v1/housing/residences',
            headers=self.admin_headers,
            data=json.dumps(residence_data)
        )
        residence_id = json.loads(response.data)['data']['id']
        
        # Create a room
        room_data = {
            'residence_id': residence_id,
            'number': '101',
            'type': 'double',
            'capacity': 2
        }
        
        response = self.client.post(
            '/api/v1/housing/rooms',
            headers=self.admin_headers,
            data=json.dumps(room_data)
        )
        room_id = json.loads(response.data)['data']['id']
        
        # Create room assignment
        assignment_data = {
            'room_id': room_id,
            'student_id': str(self.student_user.id),
            'start_date': '2024-01-01',
            'end_date': '2024-12-31'
        }
        
        # Housing staff should be able to create assignment
        response = self.client.post(
            '/api/v1/housing/assignments',
            headers=self.housing_staff_headers,
            data=json.dumps(assignment_data)
        )
        self.assertEqual(response.status_code, 201)
        assignment_id = json.loads(response.data)['data']['id']
        
        # Student should be able to view their own assignment
        response = self.client.get(
            f'/api/v1/housing/students/{self.student_user.id}/assignments',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to view other students' assignments
        response = self.client.get(
            f'/api/v1/housing/students/{self.faculty_user.id}/assignments',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_maintenance_request_access(self):
        """Test maintenance request access control"""
        # Create a residence first
        residence_data = {
            'name': 'Test Residence',
            'address': '123 Test St',
            'capacity': 100,
            'type': 'dormitory'
        }
        
        response = self.client.post(
            '/api/v1/housing/residences',
            headers=self.admin_headers,
            data=json.dumps(residence_data)
        )
        residence_id = json.loads(response.data)['data']['id']
        
        # Create a room
        room_data = {
            'residence_id': residence_id,
            'number': '101',
            'type': 'double',
            'capacity': 2
        }
        
        response = self.client.post(
            '/api/v1/housing/rooms',
            headers=self.admin_headers,
            data=json.dumps(room_data)
        )
        room_id = json.loads(response.data)['data']['id']
        
        # Create maintenance request
        request_data = {
            'room_id': room_id,
            'description': 'Broken window',
            'priority': 'high'
        }
        
        # Student should be able to create request
        response = self.client.post(
            '/api/v1/housing/maintenance-requests',
            headers=self.student_headers,
            data=json.dumps(request_data)
        )
        self.assertEqual(response.status_code, 201)
        request_id = json.loads(response.data)['data']['id']
        
        # Housing staff should be able to update request
        update_data = {
            'status': 'in_progress',
            'assigned_to': str(self.housing_staff_user.id)
        }
        
        response = self.client.put(
            f'/api/v1/housing/maintenance-requests/{request_id}',
            headers=self.housing_staff_headers,
            data=json.dumps(update_data)
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to update request status
        response = self.client.put(
            f'/api/v1/housing/maintenance-requests/{request_id}',
            headers=self.student_headers,
            data=json.dumps(update_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/housing/residences?search=1; DROP TABLE residences; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in residence data
        residence_data = {
            'name': '<script>alert("xss")</script>',
            'address': '123 Test St',
            'capacity': 100,
            'type': 'dormitory'
        }
        
        response = self.client.post(
            '/api/v1/housing/residences',
            headers=self.admin_headers,
            data=json.dumps(residence_data)
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
                '/api/v1/housing/residences',
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
        
        response = self.client.get('/api/v1/housing/residences', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 