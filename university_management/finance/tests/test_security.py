import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Transaction, Budget, User
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestFinanceSecurity(unittest.TestCase):
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
        
        self.finance_staff_user = User(
            username='finance_staff',
            email='finance@example.com',
            role='finance_staff'
        )
        self.finance_staff_user.set_password('finance123')
        db.session.add(self.finance_staff_user)
        
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
        
        self.finance_staff_token = create_access_token(identity={
            'id': self.finance_staff_user.id,
            'role': self.finance_staff_user.role
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
        self.finance_staff_headers = {
            'Authorization': f'Bearer {self.finance_staff_token}',
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
        response = self.client.get('/api/v1/finance/transactions')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/finance/transactions', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_role_based_access(self):
        """Test role-based access control"""
        # Create a transaction first
        transaction_data = {
            'amount': 1000.00,
            'type': 'income',
            'description': 'Test Transaction',
            'category': 'tuition'
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/finance/transactions',
            headers=self.admin_headers,
            data=json.dumps(transaction_data)
        )
        self.assertEqual(response.status_code, 201)
        transaction_id = json.loads(response.data)['data']['id']
        
        # Finance staff should be able to view and update
        response = self.client.get(
            f'/api/v1/finance/transactions/{transaction_id}',
            headers=self.finance_staff_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view
        response = self.client.get(
            f'/api/v1/finance/transactions/{transaction_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to view
        response = self.client.get(
            f'/api/v1/finance/transactions/{transaction_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 403)
        
        # Faculty should not be able to create
        response = self.client.post(
            '/api/v1/finance/transactions',
            headers=self.faculty_headers,
            data=json.dumps(transaction_data)
        )
        self.assertEqual(response.status_code, 403)
        
        # Student should not be able to create
        response = self.client.post(
            '/api/v1/finance/transactions',
            headers=self.student_headers,
            data=json.dumps(transaction_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_budget_management_access(self):
        """Test budget management access control"""
        # Create a budget
        budget_data = {
            'department': 'Computer Science',
            'fiscal_year': '2024',
            'amount': 100000.00,
            'category': 'operating'
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/finance/budgets',
            headers=self.admin_headers,
            data=json.dumps(budget_data)
        )
        self.assertEqual(response.status_code, 201)
        budget_id = json.loads(response.data)['data']['id']
        
        # Finance staff should be able to update
        update_data = {
            'amount': 120000.00,
            'notes': 'Increased budget'
        }
        
        response = self.client.put(
            f'/api/v1/finance/budgets/{budget_id}',
            headers=self.finance_staff_headers,
            data=json.dumps(update_data)
        )
        self.assertEqual(response.status_code, 200)
        
        # Faculty should be able to view
        response = self.client.get(
            f'/api/v1/finance/budgets/{budget_id}',
            headers=self.faculty_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to view
        response = self.client.get(
            f'/api/v1/finance/budgets/{budget_id}',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_student_financial_access(self):
        """Test student financial access control"""
        # Create a student transaction
        transaction_data = {
            'amount': 5000.00,
            'type': 'tuition',
            'description': 'Fall 2024 Tuition',
            'category': 'tuition',
            'student_id': str(self.student_user.id)
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/finance/transactions',
            headers=self.admin_headers,
            data=json.dumps(transaction_data)
        )
        self.assertEqual(response.status_code, 201)
        transaction_id = json.loads(response.data)['data']['id']
        
        # Student should be able to view their own transactions
        response = self.client.get(
            f'/api/v1/finance/students/{self.student_user.id}/transactions',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Student should not be able to view other students' transactions
        response = self.client.get(
            f'/api/v1/finance/students/{self.faculty_user.id}/transactions',
            headers=self.student_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/finance/transactions?search=1; DROP TABLE transactions; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in transaction data
        transaction_data = {
            'amount': 1000.00,
            'type': 'income',
            'description': '<script>alert("xss")</script>',
            'category': 'tuition'
        }
        
        response = self.client.post(
            '/api/v1/finance/transactions',
            headers=self.admin_headers,
            data=json.dumps(transaction_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # The response should have the script tags escaped
        response_data = json.loads(response.data)
        self.assertIn('&lt;script&gt;', response_data['data']['description'])

    def test_rate_limiting(self):
        """Test rate limiting"""
        # Make multiple requests in quick succession
        for _ in range(100):
            response = self.client.get(
                '/api/v1/finance/transactions',
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
        
        response = self.client.get('/api/v1/finance/transactions', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 