import unittest
import json
import time
from datetime import datetime
from flask import url_for
from ..models import Person, User
from app import db, create_app
from flask_jwt_extended import create_access_token

class TestPersonPerformance(unittest.TestCase):
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

    def test_bulk_person_creation(self):
        """Test performance of creating multiple persons"""
        start_time = time.time()
        
        for i in range(100):
            data = {
                'first_name': f'John{i}',
                'last_name': f'Doe{i}',
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
        
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Time to create 100 persons: {total_time:.2f} seconds")
        self.assertLess(total_time, 10.0)  # Should take less than 10 seconds

    def test_person_listing_performance(self):
        """Test performance of listing persons with pagination"""
        # Create 1000 persons first
        for i in range(1000):
            person = Person(
                id=f'test-id-{i}',
                unique_id=f'P20230101ABC{i}',
                first_name=f'John{i}',
                last_name=f'Doe{i}',
                date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date()
            )
            db.session.add(person)
        db.session.commit()
        
        start_time = time.time()
        
        response = self.client.get(
            '/api/v1/people/persons?page=1&per_page=100',
            headers=self.headers
        )
        
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Time to list 100 persons: {total_time:.2f} seconds")
        self.assertLess(total_time, 1.0)  # Should take less than 1 second
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(len(response_data['data']['items']), 100)

    def test_person_search_performance(self):
        """Test performance of searching persons"""
        # Create 1000 persons first
        for i in range(1000):
            person = Person(
                id=f'test-id-{i}',
                unique_id=f'P20230101ABC{i}',
                first_name=f'John{i}',
                last_name=f'Doe{i}',
                date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date()
            )
            db.session.add(person)
        db.session.commit()
        
        start_time = time.time()
        
        response = self.client.get(
            '/api/v1/people/persons?search=John1',
            headers=self.headers
        )
        
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Time to search persons: {total_time:.2f} seconds")
        self.assertLess(total_time, 1.0)  # Should take less than 1 second
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertGreater(len(response_data['data']['items']), 0)

    def test_concurrent_requests(self):
        """Test performance under concurrent requests"""
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request():
            data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': '1990-01-01'
            }
            
            start_time = time.time()
            response = self.client.post(
                '/api/v1/people/persons',
                headers=self.headers,
                data=json.dumps(data)
            )
            end_time = time.time()
            
            results.put({
                'status_code': response.status_code,
                'time': end_time - start_time
            })
        
        # Create 10 threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Collect results
        total_time = 0
        success_count = 0
        while not results.empty():
            result = results.get()
            total_time += result['time']
            if result['status_code'] == 201:
                success_count += 1
        
        avg_time = total_time / 10
        print(f"Average time per concurrent request: {avg_time:.2f} seconds")
        self.assertLess(avg_time, 1.0)  # Average should be less than 1 second
        self.assertEqual(success_count, 10)  # All requests should succeed

if __name__ == '__main__':
    unittest.main() 