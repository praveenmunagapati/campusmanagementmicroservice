import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Policy, Meeting, Resolution, User
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestGovernanceSecurity(unittest.TestCase):
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
        
        self.governance_user = User(
            username='governance',
            email='governance@example.com',
            role='governance_staff'
        )
        self.governance_user.set_password('governance123')
        db.session.add(self.governance_user)
        
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
        
        self.governance_token = create_access_token(identity={
            'id': self.governance_user.id,
            'role': self.governance_user.role
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
        self.governance_headers = {
            'Authorization': f'Bearer {self.governance_token}',
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
        response = self.client.get('/api/v1/governance/policies')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/governance/policies', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_policy_access(self):
        """Test policy access control"""
        # Create a policy first
        policy_data = {
            'title': 'Test Policy',
            'description': 'Test policy description',
            'category': 'academic',
            'status': 'draft',
            'effective_date': datetime.utcnow().isoformat()
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/governance/policies',
            headers=self.admin_headers,
            data=json.dumps(policy_data)
        )
        self.assertEqual(response.status_code, 201)
        policy_id = json.loads(response.data)['data']['id']
        
        # Governance staff should be able to view
        response = self.client.get(
            f'/api/v1/governance/policies/{policy_id}',
            headers=self.governance_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view
        response = self.client.get(
            f'/api/v1/governance/policies/{policy_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should not be able to create
        response = self.client.post(
            '/api/v1/governance/policies',
            headers=self.faculty_headers,
            data=json.dumps(policy_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_meeting_access(self):
        """Test meeting access control"""
        # Create a meeting
        meeting_data = {
            'title': 'Board Meeting',
            'date': datetime.utcnow().isoformat(),
            'location': 'Conference Room A',
            'agenda': 'Discuss policies',
            'status': 'scheduled'
        }
        
        # Governance staff should be able to create
        response = self.client.post(
            '/api/v1/governance/meetings',
            headers=self.governance_headers,
            data=json.dumps(meeting_data)
        )
        self.assertEqual(response.status_code, 201)
        meeting_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/governance/meetings/{meeting_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should not be able to view
        response = self.client.get(
            f'/api/v1/governance/meetings/{meeting_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_resolution_access(self):
        """Test resolution access control"""
        # Create a resolution
        resolution_data = {
            'title': 'Test Resolution',
            'description': 'Test resolution description',
            'meeting_id': 1,
            'status': 'draft'
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/governance/resolutions',
            headers=self.admin_headers,
            data=json.dumps(resolution_data)
        )
        self.assertEqual(response.status_code, 201)
        resolution_id = json.loads(response.data)['data']['id']
        
        # Governance staff should be able to view
        response = self.client.get(
            f'/api/v1/governance/resolutions/{resolution_id}',
            headers=self.governance_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should not be able to view draft resolutions
        response = self.client.get(
            f'/api/v1/governance/resolutions/{resolution_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/governance/policies?search=1; DROP TABLE policies; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in policy data
        policy_data = {
            'title': '<script>alert("xss")</script>',
            'description': 'Test policy description',
            'category': 'academic',
            'status': 'draft',
            'effective_date': datetime.utcnow().isoformat()
        }
        
        response = self.client.post(
            '/api/v1/governance/policies',
            headers=self.admin_headers,
            data=json.dumps(policy_data)
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
                '/api/v1/governance/policies',
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
        
        response = self.client.get('/api/v1/governance/policies', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 