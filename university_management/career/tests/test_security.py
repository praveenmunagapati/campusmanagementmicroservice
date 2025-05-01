import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import JobPosting, Application, Interview, User, Student
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestCareerSecurity(unittest.TestCase):
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
        
        self.career_user = User(
            username='career',
            email='career@example.com',
            role='career_staff'
        )
        self.career_user.set_password('career123')
        db.session.add(self.career_user)
        
        self.student_user = User(
            username='student',
            email='student@example.com',
            role='student'
        )
        self.student_user.set_password('student123')
        db.session.add(self.student_user)
        
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
        
        self.career_token = create_access_token(identity={
            'id': self.career_user.id,
            'role': self.career_user.role
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
        self.career_headers = {
            'Authorization': f'Bearer {self.career_token}',
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
        response = self.client.get('/api/v1/career/jobs')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/career/jobs', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_job_posting_access(self):
        """Test job posting access control"""
        # Create a job posting
        job_data = {
            'title': 'Software Engineer',
            'company': 'Tech Corp',
            'description': 'Looking for a software engineer',
            'requirements': 'Python, Flask, SQL',
            'location': 'Remote',
            'salary_range': '80000-100000',
            'deadline': datetime.utcnow().isoformat()
        }
        
        # Career staff should be able to create
        response = self.client.post(
            '/api/v1/career/jobs',
            headers=self.career_headers,
            data=json.dumps(job_data)
        )
        self.assertEqual(response.status_code, 201)
        job_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/career/jobs/{job_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            f'/api/v1/career/jobs/{job_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/career/jobs',
            headers=self.student_headers,
            data=json.dumps(job_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_application_access(self):
        """Test application access control"""
        # Create an application
        application_data = {
            'job_id': 1,
            'student_id': self.student.id,
            'resume': 'path/to/resume.pdf',
            'cover_letter': 'I am interested in this position...',
            'status': 'pending'
        }
        
        # Student should be able to create
        response = self.client.post(
            '/api/v1/career/applications',
            headers=self.student_headers,
            data=json.dumps(application_data)
        )
        self.assertEqual(response.status_code, 201)
        application_id = json.loads(response.data)['data']['id']
        
        # Career staff should be able to view and update
        response = self.client.get(
            f'/api/v1/career/applications/{application_id}',
            headers=self.career_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view their own application
        response = self.client.get(
            f'/api/v1/career/applications/{application_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to update status
        response = self.client.put(
            f'/api/v1/career/applications/{application_id}/status',
            headers=self.student_headers,
            data=json.dumps({'status': 'accepted'})
        )
        self.assertEqual(response.status_code, 403)

    def test_interview_access(self):
        """Test interview access control"""
        # Create an interview
        interview_data = {
            'application_id': 1,
            'scheduled_date': datetime.utcnow().isoformat(),
            'interviewer': 'John Doe',
            'location': 'Online',
            'status': 'scheduled'
        }
        
        # Career staff should be able to create
        response = self.client.post(
            '/api/v1/career/interviews',
            headers=self.career_headers,
            data=json.dumps(interview_data)
        )
        self.assertEqual(response.status_code, 201)
        interview_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/career/interviews/{interview_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view their interviews
        response = self.client.get(
            f'/api/v1/career/interviews/{interview_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/career/interviews',
            headers=self.student_headers,
            data=json.dumps(interview_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/career/jobs?search=1; DROP TABLE jobs; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in job data
        job_data = {
            'title': '<script>alert("xss")</script>',
            'company': 'Tech Corp',
            'description': 'Looking for a software engineer',
            'requirements': 'Python, Flask, SQL',
            'location': 'Remote',
            'salary_range': '80000-100000',
            'deadline': datetime.utcnow().isoformat()
        }
        
        response = self.client.post(
            '/api/v1/career/jobs',
            headers=self.career_headers,
            data=json.dumps(job_data)
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
                '/api/v1/career/jobs',
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
        
        response = self.client.get('/api/v1/career/jobs', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 