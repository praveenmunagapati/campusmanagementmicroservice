import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Book, User, Loan
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestLibrarySecurity(unittest.TestCase):
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
        
        self.librarian_user = User(
            username='librarian',
            email='librarian@example.com',
            role='librarian'
        )
        self.librarian_user.set_password('librarian123')
        db.session.add(self.librarian_user)
        
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
        
        self.librarian_token = create_access_token(identity={
            'id': self.librarian_user.id,
            'role': self.librarian_user.role
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
        self.librarian_headers = {
            'Authorization': f'Bearer {self.librarian_token}',
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
        response = self.client.get('/api/v1/library/books')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/library/books', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_role_based_access(self):
        """Test role-based access control"""
        # Create a book first
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'category': 'Fiction',
            'status': 'available'
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/library/books',
            headers=self.admin_headers,
            data=json.dumps(book_data)
        )
        self.assertEqual(response.status_code, 201)
        book_id = json.loads(response.data)['data']['id']
        
        # Librarian should be able to view and update
        response = self.client.get(
            f'/api/v1/library/books/{book_id}',
            headers=self.librarian_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view
        response = self.client.get(
            f'/api/v1/library/books/{book_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should be able to view
        response = self.client.get(
            f'/api/v1/library/books/{book_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should not be able to create
        response = self.client.post(
            '/api/v1/library/books',
            headers=self.faculty_headers,
            data=json.dumps(book_data)
        )
        self.assertEqual(response.status_code, 403)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/library/books',
            headers=self.student_headers,
            data=json.dumps(book_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_loan_access_control(self):
        """Test loan access control"""
        # Create a book first
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'category': 'Fiction',
            'status': 'available'
        }
        
        response = self.client.post(
            '/api/v1/library/books',
            headers=self.admin_headers,
            data=json.dumps(book_data)
        )
        book_id = json.loads(response.data)['data']['id']
        
        loan_data = {
            'user_id': str(self.student_user.id),
            'due_date': '2024-01-01'
        }
        
        # Librarian should be able to create loan
        response = self.client.post(
            f'/api/v1/library/books/{book_id}/loans',
            headers=self.librarian_headers,
            data=json.dumps(loan_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # Student should be able to view their own loans
        response = self.client.get(
            f'/api/v1/library/users/{self.student_user.id}/loans',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to create loan
        response = self.client.post(
            f'/api/v1/library/books/{book_id}/loans',
            headers=self.student_headers,
            data=json.dumps(loan_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_reservation_access_control(self):
        """Test reservation access control"""
        # Create a book first
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'category': 'Fiction',
            'status': 'available'
        }
        
        response = self.client.post(
            '/api/v1/library/books',
            headers=self.admin_headers,
            data=json.dumps(book_data)
        )
        book_id = json.loads(response.data)['data']['id']
        
        reservation_data = {
            'user_id': str(self.student_user.id)
        }
        
        # Student should be able to create reservation
        response = self.client.post(
            f'/api/v1/library/books/{book_id}/reservations',
            headers=self.student_headers,
            data=json.dumps(reservation_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # Student should be able to view their own reservations
        response = self.client.get(
            f'/api/v1/library/users/{self.student_user.id}/reservations',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to view other users' reservations
        response = self.client.get(
            f'/api/v1/library/users/{self.faculty_user.id}/reservations',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/library/books?search=1; DROP TABLE books; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in book data
        book_data = {
            'title': '<script>alert("xss")</script>',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'category': 'Fiction',
            'status': 'available'
        }
        
        response = self.client.post(
            '/api/v1/library/books',
            headers=self.admin_headers,
            data=json.dumps(book_data)
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
                '/api/v1/library/books',
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
        
        response = self.client.get('/api/v1/library/books', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 