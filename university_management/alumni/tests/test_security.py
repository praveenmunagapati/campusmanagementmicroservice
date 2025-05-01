import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Alumni, Donation, Event, User
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestAlumniSecurity(unittest.TestCase):
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
        
        self.alumni_user = User(
            username='alumni',
            email='alumni@example.com',
            role='alumni'
        )
        self.alumni_user.set_password('alumni123')
        db.session.add(self.alumni_user)
        
        self.staff_user = User(
            username='staff',
            email='staff@example.com',
            role='staff'
        )
        self.staff_user.set_password('staff123')
        db.session.add(self.staff_user)
        
        # Create a test alumni
        self.alumni = Alumni(
            name='Test Alumni',
            email='alumni@example.com',
            graduation_year=2020,
            degree='BSc Computer Science',
            current_employer='Test Company'
        )
        db.session.add(self.alumni)
        
        db.session.commit()
        
        # Create access tokens
        self.admin_token = create_access_token(identity={
            'id': self.admin_user.id,
            'role': self.admin_user.role
        })
        
        self.alumni_token = create_access_token(identity={
            'id': self.alumni_user.id,
            'role': self.alumni_user.role
        })
        
        self.staff_token = create_access_token(identity={
            'id': self.staff_user.id,
            'role': self.staff_user.role
        })
        
        self.client = self.app.test_client()
        self.admin_headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        self.alumni_headers = {
            'Authorization': f'Bearer {self.alumni_token}',
            'Content-Type': 'application/json'
        }
        self.staff_headers = {
            'Authorization': f'Bearer {self.staff_token}',
            'Content-Type': 'application/json'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_unauthorized_access(self):
        """Test access without authentication"""
        response = self.client.get('/api/v1/alumni')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/alumni', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_alumni_access(self):
        """Test alumni access control"""
        # Create an alumni profile
        alumni_data = {
            'name': 'New Alumni',
            'email': 'new@example.com',
            'graduation_year': 2021,
            'degree': 'BSc Engineering',
            'current_employer': 'New Company'
        }
        
        # Alumni should be able to create their profile
        response = self.client.post(
            '/api/v1/alumni',
            headers=self.alumni_headers,
            data=json.dumps(alumni_data)
        )
        self.assertEqual(response.status_code, 201)
        alumni_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/alumni/{alumni_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Staff should be able to view
        response = self.client.get(
            f'/api/v1/alumni/{alumni_id}',
            headers=self.staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Staff should not be able to create
        response = self.client.post(
            '/api/v1/alumni',
            headers=self.staff_headers,
            data=json.dumps(alumni_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_donation_access(self):
        """Test donation access control"""
        # Create a donation
        donation_data = {
            'alumni_id': self.alumni.id,
            'amount': 1000.00,
            'date': datetime.utcnow().isoformat(),
            'purpose': 'Scholarship Fund',
            'payment_method': 'credit_card'
        }
        
        # Alumni should be able to make donations
        response = self.client.post(
            '/api/v1/alumni/donations',
            headers=self.alumni_headers,
            data=json.dumps(donation_data)
        )
        self.assertEqual(response.status_code, 201)
        donation_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/alumni/donations/{donation_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Staff should be able to view
        response = self.client.get(
            f'/api/v1/alumni/donations/{donation_id}',
            headers=self.staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Staff should not be able to create
        response = self.client.post(
            '/api/v1/alumni/donations',
            headers=self.staff_headers,
            data=json.dumps(donation_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_event_access(self):
        """Test event access control"""
        # Create an event
        event_data = {
            'title': 'Alumni Reunion',
            'description': 'Annual alumni reunion event',
            'date': datetime.utcnow().isoformat(),
            'location': 'Main Campus',
            'capacity': 100
        }
        
        # Staff should be able to create
        response = self.client.post(
            '/api/v1/alumni/events',
            headers=self.staff_headers,
            data=json.dumps(event_data)
        )
        self.assertEqual(response.status_code, 201)
        event_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/alumni/events/{event_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Alumni should be able to view
        response = self.client.get(
            f'/api/v1/alumni/events/{event_id}',
            headers=self.alumni_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Alumni should not be able to create
        response = self.client.post(
            '/api/v1/alumni/events',
            headers=self.alumni_headers,
            data=json.dumps(event_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/alumni?search=1; DROP TABLE alumni; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in alumni data
        alumni_data = {
            'name': '<script>alert("xss")</script>',
            'email': 'new@example.com',
            'graduation_year': 2021,
            'degree': 'BSc Engineering',
            'current_employer': 'New Company'
        }
        
        response = self.client.post(
            '/api/v1/alumni',
            headers=self.alumni_headers,
            data=json.dumps(alumni_data)
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
                '/api/v1/alumni',
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
        
        response = self.client.get('/api/v1/alumni', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 