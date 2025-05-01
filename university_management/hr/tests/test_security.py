import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Employee, Position, LeaveRequest, User
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestHRSecurity(unittest.TestCase):
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
        
        self.hr_user = User(
            username='hr',
            email='hr@example.com',
            role='hr_staff'
        )
        self.hr_user.set_password('hr123')
        db.session.add(self.hr_user)
        
        self.employee_user = User(
            username='employee',
            email='employee@example.com',
            role='employee'
        )
        self.employee_user.set_password('employee123')
        db.session.add(self.employee_user)
        
        # Create a test employee
        self.employee = Employee(
            name='Test Employee',
            email='employee@example.com',
            employee_id='EMP12345'
        )
        db.session.add(self.employee)
        
        db.session.commit()
        
        # Create access tokens
        self.admin_token = create_access_token(identity={
            'id': self.admin_user.id,
            'role': self.admin_user.role
        })
        
        self.hr_token = create_access_token(identity={
            'id': self.hr_user.id,
            'role': self.hr_user.role
        })
        
        self.employee_token = create_access_token(identity={
            'id': self.employee_user.id,
            'role': self.employee_user.role
        })
        
        self.client = self.app.test_client()
        self.admin_headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        self.hr_headers = {
            'Authorization': f'Bearer {self.hr_token}',
            'Content-Type': 'application/json'
        }
        self.employee_headers = {
            'Authorization': f'Bearer {self.employee_token}',
            'Content-Type': 'application/json'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_unauthorized_access(self):
        """Test access without authentication"""
        response = self.client.get('/api/v1/hr/employees')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/hr/employees', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_employee_access(self):
        """Test employee access control"""
        # Create an employee first
        employee_data = {
            'name': 'New Employee',
            'email': 'new@example.com',
            'employee_id': 'EMP67890',
            'department': 'IT',
            'position': 'Developer',
            'hire_date': datetime.utcnow().isoformat()
        }
        
        # HR staff should be able to create
        response = self.client.post(
            '/api/v1/hr/employees',
            headers=self.hr_headers,
            data=json.dumps(employee_data)
        )
        self.assertEqual(response.status_code, 201)
        employee_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/hr/employees/{employee_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Employee should be able to view their own record
        response = self.client.get(
            f'/api/v1/hr/employees/{self.employee.id}',
            headers=self.employee_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Employee should not be able to create
        response = self.client.post(
            '/api/v1/hr/employees',
            headers=self.employee_headers,
            data=json.dumps(employee_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_position_access(self):
        """Test position access control"""
        # Create a position
        position_data = {
            'title': 'Senior Developer',
            'department': 'IT',
            'description': 'Senior software developer position',
            'requirements': 'Bachelor degree, 5 years experience',
            'salary_range': '80000-100000'
        }
        
        # HR staff should be able to create
        response = self.client.post(
            '/api/v1/hr/positions',
            headers=self.hr_headers,
            data=json.dumps(position_data)
        )
        self.assertEqual(response.status_code, 201)
        position_id = json.loads(response.data)['data']['id']
        
        # Admin should be able to view
        response = self.client.get(
            f'/api/v1/hr/positions/{position_id}',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Employee should be able to view
        response = self.client.get(
            f'/api/v1/hr/positions/{position_id}',
            headers=self.employee_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Employee should not be able to create
        response = self.client.post(
            '/api/v1/hr/positions',
            headers=self.employee_headers,
            data=json.dumps(position_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_leave_request_access(self):
        """Test leave request access control"""
        # Create a leave request
        leave_data = {
            'employee_id': self.employee.id,
            'start_date': datetime.utcnow().isoformat(),
            'end_date': datetime.utcnow().isoformat(),
            'leave_type': 'vacation',
            'reason': 'Annual vacation',
            'status': 'pending'
        }
        
        # Employee should be able to create
        response = self.client.post(
            '/api/v1/hr/leave-requests',
            headers=self.employee_headers,
            data=json.dumps(leave_data)
        )
        self.assertEqual(response.status_code, 201)
        leave_id = json.loads(response.data)['data']['id']
        
        # HR staff should be able to view and approve
        response = self.client.put(
            f'/api/v1/hr/leave-requests/{leave_id}/approve',
            headers=self.hr_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Employee should be able to view their own request
        response = self.client.get(
            f'/api/v1/hr/leave-requests/{leave_id}',
            headers=self.employee_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Employee should not be able to approve
        response = self.client.put(
            f'/api/v1/hr/leave-requests/{leave_id}/approve',
            headers=self.employee_headers
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/hr/employees?search=1; DROP TABLE employees; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in employee data
        employee_data = {
            'name': '<script>alert("xss")</script>',
            'email': 'new@example.com',
            'employee_id': 'EMP67890',
            'department': 'IT',
            'position': 'Developer',
            'hire_date': datetime.utcnow().isoformat()
        }
        
        response = self.client.post(
            '/api/v1/hr/employees',
            headers=self.hr_headers,
            data=json.dumps(employee_data)
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
                '/api/v1/hr/employees',
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
        
        response = self.client.get('/api/v1/hr/employees', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 