import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Report, Dashboard, DataSource, User
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestAnalyticsSecurity(unittest.TestCase):
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
        
        self.analyst_user = User(
            username='analyst',
            email='analyst@example.com',
            role='analyst'
        )
        self.analyst_user.set_password('analyst123')
        db.session.add(self.analyst_user)
        
        self.faculty_user = User(
            username='faculty',
            email='faculty@example.com',
            role='faculty'
        )
        self.faculty_user.set_password('faculty123')
        db.session.add(self.faculty_user)
        
        db.session.commit()
        
        # Create access tokens
        self.admin_token = create_access_token(identity={
            'id': self.admin_user.id,
            'role': self.admin_user.role
        })
        
        self.analyst_token = create_access_token(identity={
            'id': self.analyst_user.id,
            'role': self.analyst_user.role
        })
        
        self.faculty_token = create_access_token(identity={
            'id': self.faculty_user.id,
            'role': self.faculty_user.role
        })
        
        self.client = self.app.test_client()
        self.admin_headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        self.analyst_headers = {
            'Authorization': f'Bearer {self.analyst_token}',
            'Content-Type': 'application/json'
        }
        self.faculty_headers = {
            'Authorization': f'Bearer {self.faculty_token}',
            'Content-Type': 'application/json'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_unauthorized_access(self):
        """Test access without authentication"""
        response = self.client.get('/api/v1/analytics/reports')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/analytics/reports', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_report_access(self):
        """Test report access control"""
        # Create a report
        report_data = {
            'title': 'Student Performance Report',
            'description': 'Analysis of student academic performance',
            'type': 'academic',
            'data_source': 'student_records',
            'access_level': 'restricted'
        }
        
        # Analyst should be able to create
        response = self.client.post(
            '/api/v1/analytics/reports',
            headers=self.analyst_headers,
            data=json.dumps(report_data)
        )
        self.assertEqual(response.status_code, 201)
        report_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/analytics/reports/{report_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view
        response = self.client.get(
            f'/api/v1/analytics/reports/{report_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should not be able to create
        response = self.client.post(
            '/api/v1/analytics/reports',
            headers=self.faculty_headers,
            data=json.dumps(report_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_dashboard_access(self):
        """Test dashboard access control"""
        # Create a dashboard
        dashboard_data = {
            'title': 'Academic Dashboard',
            'description': 'Overview of academic metrics',
            'layout': 'grid',
            'access_level': 'restricted'
        }
        
        # Analyst should be able to create
        response = self.client.post(
            '/api/v1/analytics/dashboards',
            headers=self.analyst_headers,
            data=json.dumps(dashboard_data)
        )
        self.assertEqual(response.status_code, 201)
        dashboard_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/analytics/dashboards/{dashboard_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view
        response = self.client.get(
            f'/api/v1/analytics/dashboards/{dashboard_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should not be able to create
        response = self.client.post(
            '/api/v1/analytics/dashboards',
            headers=self.faculty_headers,
            data=json.dumps(dashboard_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_data_source_access(self):
        """Test data source access control"""
        # Create a data source
        data_source_data = {
            'name': 'Student Records',
            'type': 'database',
            'connection_string': 'postgresql://user:pass@localhost:5432/student_records',
            'access_level': 'restricted'
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/analytics/data-sources',
            headers=self.admin_headers,
            data=json.dumps(data_source_data)
        )
        self.assertEqual(response.status_code, 201)
        data_source_id = json.loads(response.data)['data']['id']
        
        # Analyst should be able to view
        response = self.client.get(
            f'/api/v1/analytics/data-sources/{data_source_id}',
            headers=self.analyst_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should not be able to view
        response = self.client.get(
            f'/api/v1/analytics/data-sources/{data_source_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/analytics/reports?search=1; DROP TABLE reports; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in report data
        report_data = {
            'title': '<script>alert("xss")</script>',
            'description': 'Analysis of student academic performance',
            'type': 'academic',
            'data_source': 'student_records',
            'access_level': 'restricted'
        }
        
        response = self.client.post(
            '/api/v1/analytics/reports',
            headers=self.analyst_headers,
            data=json.dumps(report_data)
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
                '/api/v1/analytics/reports',
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
        
        response = self.client.get('/api/v1/analytics/reports', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 