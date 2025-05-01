import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Message, Notification, Announcement, User
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestCommunicationSecurity(unittest.TestCase):
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
        response = self.client.get('/api/v1/communication/messages')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/communication/messages', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_message_access(self):
        """Test message access control"""
        # Create a message
        message_data = {
            'sender_id': self.student_user.id,
            'recipient_id': self.staff_user.id,
            'subject': 'Question about course',
            'content': 'I have a question about the assignment...',
            'priority': 'normal'
        }
        
        # Student should be able to send message
        response = self.client.post(
            '/api/v1/communication/messages',
            headers=self.student_headers,
            data=json.dumps(message_data)
        )
        self.assertEqual(response.status_code, 201)
        message_id = json.loads(response.data)['data']['id']
        
        # Staff should be able to view received message
        response = self.client.get(
            f'/api/v1/communication/messages/{message_id}',
            headers=self.staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Other students should not be able to view message
        other_student_token = create_access_token(identity={
            'id': 999,
            'role': 'student'
        })
        other_student_headers = {
            'Authorization': f'Bearer {other_student_token}',
            'Content-Type': 'application/json'
        }
        response = self.client.get(
            f'/api/v1/communication/messages/{message_id}',
            headers=other_student_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_notification_access(self):
        """Test notification access control"""
        # Create a notification
        notification_data = {
            'user_id': self.student_user.id,
            'title': 'Assignment Due',
            'content': 'Your assignment is due tomorrow',
            'type': 'academic',
            'priority': 'high'
        }
        
        # Staff should be able to create notification
        response = self.client.post(
            '/api/v1/communication/notifications',
            headers=self.staff_headers,
            data=json.dumps(notification_data)
        )
        self.assertEqual(response.status_code, 201)
        notification_id = json.loads(response.data)['data']['id']
        
        # Student should be able to view their notification
        response = self.client.get(
            f'/api/v1/communication/notifications/{notification_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Other students should not be able to view notification
        other_student_token = create_access_token(identity={
            'id': 999,
            'role': 'student'
        })
        other_student_headers = {
            'Authorization': f'Bearer {other_student_token}',
            'Content-Type': 'application/json'
        }
        response = self.client.get(
            f'/api/v1/communication/notifications/{notification_id}',
            headers=other_student_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_announcement_access(self):
        """Test announcement access control"""
        # Create an announcement
        announcement_data = {
            'title': 'Campus Event',
            'content': 'Join us for the annual campus event',
            'category': 'event',
            'target_audience': ['all'],
            'expiry_date': datetime.utcnow().isoformat()
        }
        
        # Admin should be able to create announcement
        response = self.client.post(
            '/api/v1/communication/announcements',
            headers=self.admin_headers,
            data=json.dumps(announcement_data)
        )
        self.assertEqual(response.status_code, 201)
        announcement_id = json.loads(response.data)['data']['id']
        
        # Staff should be able to view
        response = self.client.get(
            f'/api/v1/communication/announcements/{announcement_id}',
            headers=self.staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            f'/api/v1/communication/announcements/{announcement_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/communication/announcements',
            headers=self.student_headers,
            data=json.dumps(announcement_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/communication/messages?search=1; DROP TABLE messages; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in message data
        message_data = {
            'sender_id': self.student_user.id,
            'recipient_id': self.staff_user.id,
            'subject': '<script>alert("xss")</script>',
            'content': 'Test message content',
            'priority': 'normal'
        }
        
        response = self.client.post(
            '/api/v1/communication/messages',
            headers=self.student_headers,
            data=json.dumps(message_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # The response should have the script tags escaped
        response_data = json.loads(response.data)
        self.assertIn('&lt;script&gt;', response_data['data']['subject'])

    def test_rate_limiting(self):
        """Test rate limiting"""
        # Make multiple requests in quick succession
        for _ in range(100):
            response = self.client.get(
                '/api/v1/communication/messages',
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
        
        response = self.client.get('/api/v1/communication/messages', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 