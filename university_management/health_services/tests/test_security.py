import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Patient, MedicalRecord, User
from app import db, create_app
from flask_jwt_extended import create_access_token
import time

class TestHealthServicesSecurity(unittest.TestCase):
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
        
        self.doctor_user = User(
            username='doctor',
            email='doctor@example.com',
            role='doctor'
        )
        self.doctor_user.set_password('doctor123')
        db.session.add(self.doctor_user)
        
        self.nurse_user = User(
            username='nurse',
            email='nurse@example.com',
            role='nurse'
        )
        self.nurse_user.set_password('nurse123')
        db.session.add(self.nurse_user)
        
        self.patient_user = User(
            username='patient',
            email='patient@example.com',
            role='patient'
        )
        self.patient_user.set_password('patient123')
        db.session.add(self.patient_user)
        
        db.session.commit()
        
        # Create access tokens
        self.admin_token = create_access_token(identity={
            'id': self.admin_user.id,
            'role': self.admin_user.role
        })
        
        self.doctor_token = create_access_token(identity={
            'id': self.doctor_user.id,
            'role': self.doctor_user.role
        })
        
        self.nurse_token = create_access_token(identity={
            'id': self.nurse_user.id,
            'role': self.nurse_user.role
        })
        
        self.patient_token = create_access_token(identity={
            'id': self.patient_user.id,
            'role': self.patient_user.role
        })
        
        self.client = self.app.test_client()
        self.admin_headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        self.doctor_headers = {
            'Authorization': f'Bearer {self.doctor_token}',
            'Content-Type': 'application/json'
        }
        self.nurse_headers = {
            'Authorization': f'Bearer {self.nurse_token}',
            'Content-Type': 'application/json'
        }
        self.patient_headers = {
            'Authorization': f'Bearer {self.patient_token}',
            'Content-Type': 'application/json'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_unauthorized_access(self):
        """Test access without authentication"""
        response = self.client.get('/api/v1/health/patients')
        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        """Test access with invalid token"""
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = self.client.get('/api/v1/health/patients', headers=headers)
        self.assertEqual(response.status_code, 422)

    def test_role_based_access(self):
        """Test role-based access control"""
        # Create a patient first
        patient_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'gender': 'Male',
            'blood_type': 'O+'
        }
        
        # Admin should be able to create
        response = self.client.post(
            '/api/v1/health/patients',
            headers=self.admin_headers,
            data=json.dumps(patient_data)
        )
        self.assertEqual(response.status_code, 201)
        patient_id = json.loads(response.data)['data']['id']
        
        # Doctor should be able to view and update
        response = self.client.get(
            f'/api/v1/health/patients/{patient_id}',
            headers=self.doctor_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Nurse should be able to view
        response = self.client.get(
            f'/api/v1/health/patients/{patient_id}',
            headers=self.nurse_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Patient should be able to view their own record
        response = self.client.get(
            f'/api/v1/health/patients/{patient_id}',
            headers=self.patient_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Nurse should not be able to create
        response = self.client.post(
            '/api/v1/health/patients',
            headers=self.nurse_headers,
            data=json.dumps(patient_data)
        )
        self.assertEqual(response.status_code, 403)
        
        # Patient should not be able to create
        response = self.client.post(
            '/api/v1/health/patients',
            headers=self.patient_headers,
            data=json.dumps(patient_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_medical_record_access_control(self):
        """Test medical record access control"""
        # Create a patient and add a medical record
        patient_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'gender': 'Male',
            'blood_type': 'O+'
        }
        
        response = self.client.post(
            '/api/v1/health/patients',
            headers=self.admin_headers,
            data=json.dumps(patient_data)
        )
        patient_id = json.loads(response.data)['data']['id']
        
        medical_record_data = {
            'diagnosis': 'Common cold',
            'treatment': 'Rest and fluids',
            'notes': 'Patient should rest for 2-3 days'
        }
        
        # Doctor should be able to add medical record
        response = self.client.post(
            f'/api/v1/health/patients/{patient_id}/medical-records',
            headers=self.doctor_headers,
            data=json.dumps(medical_record_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # Nurse should be able to view medical records
        response = self.client.get(
            f'/api/v1/health/patients/{patient_id}/medical-records',
            headers=self.nurse_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Patient should be able to view their own medical records
        response = self.client.get(
            f'/api/v1/health/patients/{patient_id}/medical-records',
            headers=self.patient_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Patient should not be able to add medical records
        response = self.client.post(
            f'/api/v1/health/patients/{patient_id}/medical-records',
            headers=self.patient_headers,
            data=json.dumps(medical_record_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_prescription_access_control(self):
        """Test prescription access control"""
        # Create a patient
        patient_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'gender': 'Male',
            'blood_type': 'O+'
        }
        
        response = self.client.post(
            '/api/v1/health/patients',
            headers=self.admin_headers,
            data=json.dumps(patient_data)
        )
        patient_id = json.loads(response.data)['data']['id']
        
        prescription_data = {
            'medication': 'Ibuprofen',
            'dosage': '200mg',
            'frequency': 'Every 6 hours',
            'duration': '3 days'
        }
        
        # Doctor should be able to prescribe
        response = self.client.post(
            f'/api/v1/health/patients/{patient_id}/prescriptions',
            headers=self.doctor_headers,
            data=json.dumps(prescription_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # Nurse should be able to view prescriptions
        response = self.client.get(
            f'/api/v1/health/patients/{patient_id}/prescriptions',
            headers=self.nurse_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Patient should be able to view their own prescriptions
        response = self.client.get(
            f'/api/v1/health/patients/{patient_id}/prescriptions',
            headers=self.patient_headers
        )
        self.assertEqual(response.status_code, 200)
        
        # Nurse should not be able to prescribe
        response = self.client.post(
            f'/api/v1/health/patients/{patient_id}/prescriptions',
            headers=self.nurse_headers,
            data=json.dumps(prescription_data)
        )
        self.assertEqual(response.status_code, 403)

    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        # Try SQL injection in search parameter
        response = self.client.get(
            '/api/v1/health/patients?search=1; DROP TABLE patients; --',
            headers=self.admin_headers
        )
        self.assertEqual(response.status_code, 200)
        # The query should be sanitized and not cause any harm

    def test_xss_prevention(self):
        """Test XSS prevention"""
        # Try XSS in patient data
        patient_data = {
            'first_name': '<script>alert("xss")</script>',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'gender': 'Male',
            'blood_type': 'O+'
        }
        
        response = self.client.post(
            '/api/v1/health/patients',
            headers=self.admin_headers,
            data=json.dumps(patient_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # The response should have the script tags escaped
        response_data = json.loads(response.data)
        self.assertIn('&lt;script&gt;', response_data['data']['first_name'])

    def test_rate_limiting(self):
        """Test rate limiting"""
        # Make multiple requests in quick succession
        for _ in range(100):
            response = self.client.get(
                '/api/v1/health/patients',
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
        
        response = self.client.get('/api/v1/health/patients', headers=headers)
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main() 