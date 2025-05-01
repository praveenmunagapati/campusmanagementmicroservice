import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import (
    SustainabilityProject, EnergyConsumption, WasteManagement,
    SustainabilityEvent, GreenBuilding, User
)
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestSustainabilitySecurity(unittest.TestCase):
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
        
        self.sustainability_staff_user = User(
            username='sustainability_staff',
            email='sustainability@example.com',
            role='sustainability_staff'
        )
        self.sustainability_staff_user.set_password('sustainability123')
        db.session.add(self.sustainability_staff_user)
        
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
        
        self.sustainability_staff_token = create_access_token(identity={
            'id': self.sustainability_staff_user.id,
            'role': self.sustainability_staff_user.role
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
        self.sustainability_staff_headers = {
            'Authorization': f'Bearer {self.sustainability_staff_token}',
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
        response = self.client.get('/api/v1/sustainability/projects')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/sustainability/projects', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_role_based_access(self):
        """Test role-based access control"""
        # Create a sustainability project first
        project_data = {
            'title': 'Test Project',
            'description': 'Test Description',
            'start_date': '2024-01-01',
            'category': 'energy',
            'impact_metrics': {'co2_reduction': 100},
            'budget': 10000
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/sustainability/projects',
            headers=self.admin_headers,
            data=json.dumps(project_data)
        )
        self.assertEqual(response.status_code, 201)
        project_id = json.loads(response.data)['data']['id']
        
        # Sustainability staff should be able to view and update
        response = self.client.get(
            f'/api/v1/sustainability/projects/{project_id}',
            headers=self.sustainability_staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view
        response = self.client.get(
            f'/api/v1/sustainability/projects/{project_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            f'/api/v1/sustainability/projects/{project_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should not be able to create
        response = self.client.post(
            '/api/v1/sustainability/projects',
            headers=self.faculty_headers,
            data=json.dumps(project_data)
        )
        self.assertEqual(response.status_code, 403)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/sustainability/projects',
            headers=self.student_headers,
            data=json.dumps(project_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_energy_consumption_access(self):
        """Test energy consumption access control"""
        # Create an energy consumption record
        energy_data = {
            'building_id': 1,
            'date': '2024-01-01',
            'electricity_usage': 1000,
            'gas_usage': 500,
            'water_usage': 200
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/sustainability/energy',
            headers=self.admin_headers,
            data=json.dumps(energy_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # Sustainability staff should be able to view
        response = self.client.get(
            '/api/v1/sustainability/energy',
            headers=self.sustainability_staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view
        response = self.client.get(
            '/api/v1/sustainability/energy',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            '/api/v1/sustainability/energy',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_waste_management_access(self):
        """Test waste management access control"""
        # Create a waste management record
        waste_data = {
            'building_id': 1,
            'date': '2024-01-01',
            'waste_type': 'recyclable',
            'amount': 100,
            'disposal_method': 'recycling'
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/sustainability/waste',
            headers=self.admin_headers,
            data=json.dumps(waste_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # Sustainability staff should be able to view
        response = self.client.get(
            '/api/v1/sustainability/waste',
            headers=self.sustainability_staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view
        response = self.client.get(
            '/api/v1/sustainability/waste',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            '/api/v1/sustainability/waste',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/sustainability/projects?search=1; DROP TABLE projects; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in project data
        project_data = {
            'title': '<script>alert("xss")</script>',
            'description': 'Test Description',
            'start_date': '2024-01-01',
            'category': 'energy',
            'impact_metrics': {'co2_reduction': 100},
            'budget': 10000
        }
        
        response = self.client.post(
            '/api/v1/sustainability/projects',
            headers=self.admin_headers,
            data=json.dumps(project_data)
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
                '/api/v1/sustainability/projects',
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
        
        response = self.client.get('/api/v1/sustainability/projects', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 