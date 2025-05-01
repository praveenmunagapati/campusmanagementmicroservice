import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Ticket, User, Device
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestITSupportSecurity(unittest.TestCase):
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
        
        self.it_staff_user = User(
            username='it_staff',
            email='it_staff@example.com',
            role='it_staff'
        )
        self.it_staff_user.set_password('it_staff123')
        db.session.add(self.it_staff_user)
        
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
        
        self.it_staff_token = create_access_token(identity={
            'id': self.it_staff_user.id,
            'role': self.it_staff_user.role
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
        self.it_staff_headers = {
            'Authorization': f'Bearer {self.it_staff_token}',
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
        response = self.client.get('/api/v1/it-support/tickets')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/it-support/tickets', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_role_based_access(self):
        """Test role-based access control"""
        # Create a ticket first
        ticket_data = {
            'title': 'Test Ticket',
            'description': 'Test Description',
            'category': 'hardware',
            'priority': 'medium'
        }
        
        # Student should be able to create ticket
        response = self.client.post(
            '/api/v1/it-support/tickets',
            headers=self.student_headers,
            data=json.dumps(ticket_data)
        )
        self.assertEqual(response.status_code, 201)
        ticket_id = json.loads(response.data)['data']['id']
        
        # IT Staff should be able to view and update
        response = self.client.get(
            f'/api/v1/it-support/tickets/{ticket_id}',
            headers=self.it_staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view
        response = self.client.get(
            f'/api/v1/it-support/tickets/{ticket_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view their own ticket
        response = self.client.get(
            f'/api/v1/it-support/tickets/{ticket_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to view other users' tickets
        response = self.client.get(
            f'/api/v1/it-support/users/{self.faculty_user.id}/tickets',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_ticket_management_access(self):
        """Test ticket management access control"""
        # Create a ticket
        ticket_data = {
            'title': 'Test Ticket',
            'description': 'Test Description',
            'category': 'hardware',
            'priority': 'medium'
        }
        
        response = self.client.post(
            '/api/v1/it-support/tickets',
            headers=self.student_headers,
            data=json.dumps(ticket_data)
        )
        ticket_id = json.loads(response.data)['data']['id']
        
        update_data = {
            'status': 'in_progress',
            'assigned_to': str(self.it_staff_user.id)
        }
        
        # IT Staff should be able to update ticket
        response = self.client.put(
            f'/api/v1/it-support/tickets/{ticket_id}',
            headers=self.it_staff_headers,
            data=json.dumps(update_data)
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to update ticket status
        response = self.client.put(
            f'/api/v1/it-support/tickets/{ticket_id}',
            headers=self.student_headers,
            data=json.dumps(update_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_device_management_access(self):
        """Test device management access control"""
        # Create a device
        device_data = {
            'name': 'Test Device',
            'type': 'laptop',
            'serial_number': '123456',
            'status': 'available'
        }
        
        # IT Staff should be able to create device
        response = self.client.post(
            '/api/v1/it-support/devices',
            headers=self.it_staff_headers,
            data=json.dumps(device_data)
        )
        self.assertEqual(response.status_code, 201)
        device_id = json.loads(response.data)['data']['id']
        
        # Student should be able to view devices
        response = self.client.get(
            f'/api/v1/it-support/devices/{device_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to create device
        response = self.client.post(
            '/api/v1/it-support/devices',
            headers=self.student_headers,
            data=json.dumps(device_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/it-support/tickets?search=1; DROP TABLE tickets; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in ticket data
        ticket_data = {
            'title': '<script>alert("xss")</script>',
            'description': 'Test Description',
            'category': 'hardware',
            'priority': 'medium'
        }
        
        response = self.client.post(
            '/api/v1/it-support/tickets',
            headers=self.student_headers,
            data=json.dumps(ticket_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # The response should have the script tags escaped
        response_data = json.loads(response.data)
        self.assertIn('&lt;script&gt;', response_data['data']['title'])

    def test_rate_limiting(self):
        """Test rate limiting"""
        # Make multiple requests in quick succession
        for _ in range(100):
            response = self.client.get(
                '/api/v1/it-support/tickets',
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
        
        response = self.client.get('/api/v1/it-support/tickets', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 