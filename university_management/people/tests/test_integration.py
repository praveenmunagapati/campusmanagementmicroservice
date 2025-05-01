import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Person, ContactInfo, User
from app import db, create_app
from flask_jwt_extended import create_access_token

class TestPersonIntegration(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user
        self.user = User(
            username='testuser',
            email='test@example.com',
            role='admin'
        )
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()
        
        # Create access token
        self.access_token = create_access_token(identity={
            'id': self.user.id,
            'role': self.user.role
        })
        
        self.client = self.app.test_client()
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_person_contact_info_flow(self):
        # Create a person
        person_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'gender_identity': 'Male',
            'pronouns': 'he/him',
            'nationality': 'US'
        }
        
        response = self.client.post(
            '/api/v1/people/persons',
            headers=self.headers,
            data=json.dumps(person_data)
        )
        self.assertEqual(response.status_code, 201)
        person_id = json.loads(response.data)['data']['id']
        
        # Add contact info
        contact_data = {
            'contact_type': 'email',
            'value': 'john@example.com',
            'is_primary': True
        }
        
        response = self.client.post(
            f'/api/v1/people/persons/{person_id}/contact-info',
            headers=self.headers,
            data=json.dumps(contact_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # Get person with contact info
        response = self.client.get(
            f'/api/v1/people/persons/{person_id}',
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(len(response_data['data']['contact_info']), 1)
        self.assertEqual(response_data['data']['contact_info'][0]['value'], 'john@example.com')

    def test_person_relationship_flow(self):
        # Create two persons
        person1_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01'
        }
        
        person2_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'date_of_birth': '1992-01-01'
        }
        
        response = self.client.post(
            '/api/v1/people/persons',
            headers=self.headers,
            data=json.dumps(person1_data)
        )
        self.assertEqual(response.status_code, 201)
        person1_id = json.loads(response.data)['data']['id']
        
        response = self.client.post(
            '/api/v1/people/persons',
            headers=self.headers,
            data=json.dumps(person2_data)
        )
        self.assertEqual(response.status_code, 201)
        person2_id = json.loads(response.data)['data']['id']
        
        # Create relationship
        relationship_data = {
            'person_id_b': person2_id,
            'relationship_type': 'spouse',
            'is_emergency_contact': True
        }
        
        response = self.client.post(
            f'/api/v1/people/persons/{person1_id}/relationships',
            headers=self.headers,
            data=json.dumps(relationship_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # Get person with relationships
        response = self.client.get(
            f'/api/v1/people/persons/{person1_id}',
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(len(response_data['data']['relationships']), 1)
        self.assertEqual(response_data['data']['relationships'][0]['relationship_type'], 'spouse')

    def test_person_document_flow(self):
        # Create a person
        person_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01'
        }
        
        response = self.client.post(
            '/api/v1/people/persons',
            headers=self.headers,
            data=json.dumps(person_data)
        )
        self.assertEqual(response.status_code, 201)
        person_id = json.loads(response.data)['data']['id']
        
        # Add document
        document_data = {
            'document_type': 'passport',
            'document_number': 'P123456789',
            'expiry_date': '2025-01-01',
            'issue_date': '2020-01-01',
            'issuing_authority': 'US Department of State'
        }
        
        response = self.client.post(
            f'/api/v1/people/persons/{person_id}/documents',
            headers=self.headers,
            data=json.dumps(document_data)
        )
        self.assertEqual(response.status_code, 201)
        
        # Get person with documents
        response = self.client.get(
            f'/api/v1/people/persons/{person_id}',
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(len(response_data['data']['identification_documents']), 1)
        self.assertEqual(response_data['data']['identification_documents'][0]['document_type'], 'passport')

if __name__ == '__main__':
    unittest.main() 