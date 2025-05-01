import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Parent, ParentMessage, ParentMeeting, User, Student
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestParentPortalSecurity(unittest.TestCase):
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
        
        self.parent_user = User(
            username='parent',
            email='parent@example.com',
            role='parent'
        )
        self.parent_user.set_password('parent123')
        db.session.add(self.parent_user)
        
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
        
        self.parent_token = create_access_token(identity={
            'id': self.parent_user.id,
            'role': self.parent_user.role
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
        self.parent_headers = {
            'Authorization': f'Bearer {self.parent_token}',
            'Content-Type': 'application/json'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_unauthorized_access(self):
        """Test access without authentication"""
        response = self.client.get('/api/v1/parent-portal/parents')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/parent-portal/parents', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_role_based_access(self):
        """Test role-based access control"""
        # Create a parent profile first
        parent_data = {
            'user_id': self.parent_user.id,
            'student_id': self.student.id,
            'relationship': 'mother',
            'is_primary': True,
            'can_view_grades': True,
            'can_view_attendance': True,
            'can_view_discipline': True
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/parent-portal/parents',
            headers=self.admin_headers,
            data=json.dumps(parent_data)
        )
        self.assertEqual(response.status_code, 201)
        parent_id = json.loads(response.data)['data']['id']
        
        # Staff should be able to view
        response = self.client.get(
            f'/api/v1/parent-portal/parents/{parent_id}',
            headers=self.staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Parent should be able to view their own profile
        response = self.client.get(
            f'/api/v1/parent-portal/parents/{parent_id}',
            headers=self.parent_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Parent should not be able to create another parent profile
        response = self.client.post(
            '/api/v1/parent-portal/parents',
            headers=self.parent_headers,
            data=json.dumps(parent_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_message_access(self):
        """Test parent message access control"""
        # Create a parent profile first
        parent_data = {
            'user_id': self.parent_user.id,
            'student_id': self.student.id,
            'relationship': 'mother',
            'is_primary': True
        }
        
        response = self.client.post(
            '/api/v1/parent-portal/parents',
            headers=self.admin_headers,
            data=json.dumps(parent_data)
        )
        parent_id = json.loads(response.data)['data']['id']
        
        # Create a message
        message_data = {
            'parent_id': parent_id,
            'recipient_id': self.staff_user.id,
            'subject': 'Test Message',
            'message': 'Test Content'
        }
        
        # Parent should be able to create message
        response = self.client.post(
            '/api/v1/parent-portal/messages',
            headers=self.parent_headers,
            data=json.dumps(message_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # Staff should be able to view messages
        response = self.client.get(
            '/api/v1/parent-portal/messages',
            headers=self.staff_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_meeting_access(self):
        """Test parent meeting access control"""
        # Create a parent profile first
        parent_data = {
            'user_id': self.parent_user.id,
            'student_id': self.student.id,
            'relationship': 'mother',
            'is_primary': True
        }
        
        response = self.client.post(
            '/api/v1/parent-portal/parents',
            headers=self.admin_headers,
            data=json.dumps(parent_data)
        )
        parent_id = json.loads(response.data)['data']['id']
        
        # Create a meeting
        meeting_data = {
            'parent_id': parent_id,
            'staff_id': self.staff_user.id,
            'student_id': self.student.id,
            'meeting_date': '2024-01-01T10:00:00',
            'duration': 60,
            'purpose': 'Test Meeting'
        }
        
        # Staff should be able to create meeting
        response = self.client.post(
            '/api/v1/parent-portal/meetings',
            headers=self.staff_headers,
            data=json.dumps(meeting_data)
        )
        self.assertEqual(response.status_code, 201)
        meeting_id = json.loads(response.data)['data']['id']
        
        # Parent should be able to view their meetings
        response = self.client.get(
            '/api/v1/parent-portal/meetings',
            headers=self.parent_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Only staff should be able to mark meetings as completed
        response = self.client.put(
            f'/api/v1/parent-portal/meetings/{meeting_id}/complete',
            headers=self.staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Parent should not be able to mark meetings as completed
        response = self.client.put(
            f'/api/v1/parent-portal/meetings/{meeting_id}/complete',
            headers=self.parent_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/parent-portal/parents?search=1; DROP TABLE parents; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in parent data
        parent_data = {
            'user_id': self.parent_user.id,
            'student_id': self.student.id,
            'relationship': '<script>alert("xss")</script>',
            'is_primary': True
        }
        
        response = self.client.post(
            '/api/v1/parent-portal/parents',
            headers=self.admin_headers,
            data=json.dumps(parent_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # The response should have the script tags escaped
        response_data = json.loads(response.data)
        self.assertIn('&lt;script&gt;', response_data['data']['relationship'])

    def test_rate_limiting(self):
        """Test rate limiting"""
        # Make multiple requests in quick succession
        for _ in range(100):
            response = self.client.get(
                '/api/v1/parent-portal/parents',
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
        
        response = self.client.get('/api/v1/parent-portal/parents', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 