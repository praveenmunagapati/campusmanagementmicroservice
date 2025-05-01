import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import ResearchProject, Publication, Grant, User
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestResearchSecurity(unittest.TestCase):
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
        response = self.client.get('/api/v1/research/projects')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/research/projects', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_project_access(self):
        """Test project access control"""
        # Create a project first
        project_data = {
            'title': 'Test Project',
            'description': 'Test project description',
            'start_date': datetime.utcnow().isoformat(),
            'end_date': datetime.utcnow().isoformat(),
            'status': 'active',
            'principal_investigator_id': self.faculty_user.id
        }
        
        # Faculty should be able to create
        response = self.client.post(
            '/api/v1/research/projects',
            headers=self.faculty_headers,
            data=json.dumps(project_data)
        )
        self.assertEqual(response.status_code, 201)
        project_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/research/projects/{project_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view public projects
        response = self.client.get(
            f'/api/v1/research/projects/{project_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/research/projects',
            headers=self.student_headers,
            data=json.dumps(project_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_publication_access(self):
        """Test publication access control"""
        # Create a publication
        publication_data = {
            'title': 'Test Publication',
            'authors': ['John Doe', 'Jane Smith'],
            'journal': 'Test Journal',
            'publication_date': datetime.utcnow().isoformat(),
            'doi': '10.1234/test',
            'project_id': 1
        }
        
        # Faculty should be able to create
        response = self.client.post(
            '/api/v1/research/publications',
            headers=self.faculty_headers,
            data=json.dumps(publication_data)
        )
        self.assertEqual(response.status_code, 201)
        publication_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/research/publications/{publication_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            f'/api/v1/research/publications/{publication_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/research/publications',
            headers=self.student_headers,
            data=json.dumps(publication_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_grant_access(self):
        """Test grant access control"""
        # Create a grant
        grant_data = {
            'title': 'Test Grant',
            'funding_agency': 'Test Agency',
            'amount': 100000.00,
            'start_date': datetime.utcnow().isoformat(),
            'end_date': datetime.utcnow().isoformat(),
            'status': 'pending',
            'project_id': 1
        }
        
        # Faculty should be able to create
        response = self.client.post(
            '/api/v1/research/grants',
            headers=self.faculty_headers,
            data=json.dumps(grant_data)
        )
        self.assertEqual(response.status_code, 201)
        grant_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view and approve
        response = self.client.put(
            f'/api/v1/research/grants/{grant_id}/approve',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view their grants
        response = self.client.get(
            f'/api/v1/research/grants/{grant_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to view grants
        response = self.client.get(
            f'/api/v1/research/grants/{grant_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/research/projects?search=1; DROP TABLE projects; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in project data
        project_data = {
            'title': '<script>alert("xss")</script>',
            'description': 'Test project description',
            'start_date': datetime.utcnow().isoformat(),
            'end_date': datetime.utcnow().isoformat(),
            'status': 'active',
            'principal_investigator_id': self.faculty_user.id
        }
        
        response = self.client.post(
            '/api/v1/research/projects',
            headers=self.faculty_headers,
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
                '/api/v1/research/projects',
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
        
        response = self.client.get('/api/v1/research/projects', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 