import unittest
import json
from datetime import datetime
from flask import url_for
from ..models import Person, User
from app import db, create_app
from flask_jwt_extended import create_access_token

class TestPersonRoutes(unittest.TestCase):
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

    def test_create_person(self):
        data = {
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
            data=json.dumps(data)
        )
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['data']['first_name'], 'John')
        self.assertEqual(response_data['data']['last_name'], 'Doe')

    def test_get_person(self):
        # Create a person first
        person = Person(
            id='test-id',
            unique_id='P20230101ABC123',
            first_name='John',
            last_name='Doe',
            date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date()
        )
        db.session.add(person)
        db.session.commit()
        
        response = self.client.get(
            f'/api/v1/people/persons/test-id',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['data']['first_name'], 'John')
        self.assertEqual(response_data['data']['last_name'], 'Doe')

    def test_list_persons(self):
        # Create multiple persons
        for i in range(3):
            person = Person(
                id=f'test-id-{i}',
                unique_id=f'P20230101ABC{i}',
                first_name=f'John{i}',
                last_name=f'Doe{i}',
                date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date()
            )
            db.session.add(person)
        db.session.commit()
        
        response = self.client.get(
            '/api/v1/people/persons',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(len(response_data['data']['items']), 3)

    def test_update_person(self):
        # Create a person first
        person = Person(
            id='test-id',
            unique_id='P20230101ABC123',
            first_name='John',
            last_name='Doe',
            date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date()
        )
        db.session.add(person)
        db.session.commit()
        
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith'
        }
        
        response = self.client.put(
            f'/api/v1/people/persons/test-id',
            headers=self.headers,
            data=json.dumps(data)
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['data']['first_name'], 'Jane')
        self.assertEqual(response_data['data']['last_name'], 'Smith')

    def test_unauthorized_access(self):
        # Create a non-admin user
        user = User(
            username='testuser2',
            email='test2@example.com',
            role='student'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # Create access token for non-admin user
        access_token = create_access_token(identity={
            'id': user.id,
            'role': user.role
        })
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = self.client.post(
            '/api/v1/people/persons',
            headers=headers,
            data=json.dumps({
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': '1990-01-01'
            })
        )
        
        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main() 