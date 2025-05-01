import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Vehicle, Route, Schedule, User
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestTransportationSecurity(unittest.TestCase):
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
        
        self.transport_user = User(
            username='transport',
            email='transport@example.com',
            role='transport_staff'
        )
        self.transport_user.set_password('transport123')
        db.session.add(self.transport_user)
        
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
        
        self.transport_token = create_access_token(identity={
            'id': self.transport_user.id,
            'role': self.transport_user.role
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
        self.transport_headers = {
            'Authorization': f'Bearer {self.transport_token}',
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
        response = self.client.get('/api/v1/transportation/vehicles')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/transportation/vehicles', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_vehicle_access(self):
        """Test vehicle access control"""
        # Create a vehicle first
        vehicle_data = {
            'name': 'Bus 1',
            'type': 'bus',
            'capacity': 50,
            'registration_number': 'BUS123',
            'status': 'active'
        }
        
        # Transport staff should be able to create
        response = self.client.post(
            '/api/v1/transportation/vehicles',
            headers=self.transport_headers,
            data=json.dumps(vehicle_data)
        )
        self.assertEqual(response.status_code, 201)
        vehicle_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/transportation/vehicles/{vehicle_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            f'/api/v1/transportation/vehicles/{vehicle_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/transportation/vehicles',
            headers=self.student_headers,
            data=json.dumps(vehicle_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_route_access(self):
        """Test route access control"""
        # Create a route
        route_data = {
            'name': 'Campus Loop',
            'description': 'Main campus circular route',
            'stops': ['Stop A', 'Stop B', 'Stop C'],
            'estimated_duration': 30,
            'status': 'active'
        }
        
        # Transport staff should be able to create
        response = self.client.post(
            '/api/v1/transportation/routes',
            headers=self.transport_headers,
            data=json.dumps(route_data)
        )
        self.assertEqual(response.status_code, 201)
        route_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/transportation/routes/{route_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            f'/api/v1/transportation/routes/{route_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/transportation/routes',
            headers=self.student_headers,
            data=json.dumps(route_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_schedule_access(self):
        """Test schedule access control"""
        # Create a schedule
        schedule_data = {
            'route_id': 1,
            'vehicle_id': 1,
            'departure_time': datetime.utcnow().isoformat(),
            'arrival_time': datetime.utcnow().isoformat(),
            'status': 'scheduled'
        }
        
        # Transport staff should be able to create
        response = self.client.post(
            '/api/v1/transportation/schedules',
            headers=self.transport_headers,
            data=json.dumps(schedule_data)
        )
        self.assertEqual(response.status_code, 201)
        schedule_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/transportation/schedules/{schedule_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            f'/api/v1/transportation/schedules/{schedule_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/transportation/schedules',
            headers=self.student_headers,
            data=json.dumps(schedule_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/transportation/vehicles?search=1; DROP TABLE vehicles; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in vehicle data
        vehicle_data = {
            'name': '<script>alert("xss")</script>',
            'type': 'bus',
            'capacity': 50,
            'registration_number': 'BUS123',
            'status': 'active'
        }
        
        response = self.client.post(
            '/api/v1/transportation/vehicles',
            headers=self.transport_headers,
            data=json.dumps(vehicle_data)
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
                '/api/v1/transportation/vehicles',
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
        
        response = self.client.get('/api/v1/transportation/vehicles', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 