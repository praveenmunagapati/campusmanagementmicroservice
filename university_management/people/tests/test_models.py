import unittest
from datetime import datetime
from ..models import Person, ContactInfo, Relationship, User
from app import db, create_app

class TestPersonModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_person(self):
        person = Person(
            id='test-id',
            unique_id='P20230101ABC123',
            first_name='John',
            last_name='Doe',
            date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
            gender_identity='Male',
            pronouns='he/him',
            nationality='US'
        )
        db.session.add(person)
        db.session.commit()

        saved_person = Person.query.get('test-id')
        self.assertIsNotNone(saved_person)
        self.assertEqual(saved_person.first_name, 'John')
        self.assertEqual(saved_person.last_name, 'Doe')
        self.assertEqual(saved_person.gender_identity, 'Male')

    def test_person_relationships(self):
        person = Person(
            id='test-id',
            unique_id='P20230101ABC123',
            first_name='John',
            last_name='Doe',
            date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date()
        )
        db.session.add(person)

        contact = ContactInfo(
            id='contact-id',
            person_id='test-id',
            contact_type='email',
            value='john@example.com',
            is_primary=True
        )
        db.session.add(contact)
        db.session.commit()

        saved_person = Person.query.get('test-id')
        self.assertEqual(len(saved_person.contact_info), 1)
        self.assertEqual(saved_person.contact_info[0].value, 'john@example.com')

class TestContactInfoModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_contact_info(self):
        person = Person(
            id='test-id',
            unique_id='P20230101ABC123',
            first_name='John',
            last_name='Doe',
            date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d').date()
        )
        db.session.add(person)

        contact = ContactInfo(
            id='contact-id',
            person_id='test-id',
            contact_type='phone',
            value='+1234567890',
            is_primary=True
        )
        db.session.add(contact)
        db.session.commit()

        saved_contact = ContactInfo.query.get('contact-id')
        self.assertIsNotNone(saved_contact)
        self.assertEqual(saved_contact.contact_type, 'phone')
        self.assertEqual(saved_contact.value, '+1234567890')
        self.assertTrue(saved_contact.is_primary)

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        user = User(
            username='testuser',
            email='test@example.com',
            role='student'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

        saved_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, 'test@example.com')
        self.assertEqual(saved_user.role, 'student')
        self.assertTrue(saved_user.check_password('password123'))

if __name__ == '__main__':
    unittest.main() 