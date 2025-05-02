import pytest
from datetime import datetime
from ..models import (
    Student, StudentProfile, StudentAcademic,
    StudentFinancial, StudentDocument,
    StudentEnrollment, StudentAttendance,
    StudentGrade, StudentAdvising,
    StudentService, StudentComplaint,
    StudentFeedback, StudentSurvey,
    StudentLocation, StudentContact,
    StudentEmergency
)
from .. import db

@pytest.fixture
def student_data():
    return {
        'student_id': 'STU001',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'student_type': 'undergraduate',
        'program': 'Computer Science',
        'enrollment_date': datetime.now(),
        'status': 'active'
    }

@pytest.fixture
def student_profile_data():
    return {
        'nationality': 'US',
        'date_of_birth': datetime(2000, 1, 1),
        'gender': 'Male',
        'address': '123 Main St',
        'city': 'New York',
        'state': 'NY',
        'zip_code': '10001',
        'country': 'USA',
        'status': 'active'
    }

@pytest.fixture
def student_academic_data():
    return {
        'program': 'Computer Science',
        'major': 'Software Engineering',
        'minor': 'Mathematics',
        'start_date': datetime.now(),
        'expected_graduation': datetime(2024, 5, 1),
        'gpa': 3.5,
        'status': 'active'
    }

@pytest.fixture
def student_financial_data():
    return {
        'payment_type': 'tuition',
        'amount': 5000.00,
        'payment_date': datetime.now(),
        'status': 'paid'
    }

@pytest.fixture
def student_document_data():
    return {
        'document_type': 'transcript',
        'file_name': 'transcript.pdf',
        'upload_date': datetime.now(),
        'status': 'verified'
    }

@pytest.fixture
def student_enrollment_data():
    return {
        'course': 'CS101',
        'section': 'A',
        'semester': 'Fall 2023',
        'enrollment_date': datetime.now(),
        'status': 'enrolled'
    }

@pytest.fixture
def student_attendance_data():
    return {
        'course': 'CS101',
        'attendance_date': datetime.now(),
        'status': 'present'
    }

@pytest.fixture
def student_grade_data():
    return {
        'course': 'CS101',
        'grade': 'A',
        'grade_points': 4.0,
        'grade_date': datetime.now()
    }

@pytest.fixture
def student_advising_data():
    return {
        'advisor_id': 'ADV001',
        'advising_date': datetime.now(),
        'notes': 'Course planning',
        'status': 'completed'
    }

@pytest.fixture
def student_service_data():
    return {
        'service_type': 'counseling',
        'service_date': datetime.now(),
        'notes': 'Academic counseling',
        'status': 'completed'
    }

@pytest.fixture
def student_complaint_data():
    return {
        'complaint_type': 'academic',
        'description': 'Grade dispute',
        'created_at': datetime.now(),
        'status': 'pending'
    }

@pytest.fixture
def student_feedback_data():
    return {
        'feedback_type': 'course',
        'rating': 4,
        'comments': 'Great course',
        'created_at': datetime.now()
    }

@pytest.fixture
def student_survey_data():
    return {
        'survey_type': 'course_evaluation',
        'responses': {'q1': 'A', 'q2': 'B'},
        'created_at': datetime.now()
    }

@pytest.fixture
def student_location_data():
    return {
        'location_type': 'residence',
        'building': 'Dorm A',
        'room': '101',
        'status': 'active'
    }

@pytest.fixture
def student_contact_data():
    return {
        'contact_type': 'emergency',
        'name': 'Jane Doe',
        'relationship': 'parent',
        'phone': '9876543210',
        'email': 'jane.doe@example.com'
    }

@pytest.fixture
def student_emergency_data():
    return {
        'emergency_type': 'medical',
        'description': 'Allergic reaction',
        'occurred_at': datetime.now(),
        'status': 'resolved'
    }

def test_student_creation(student_data):
    student = Student(**student_data)
    assert student.student_id == student_data['student_id']
    assert student.first_name == student_data['first_name']
    assert student.last_name == student_data['last_name']
    assert student.email == student_data['email']
    assert student.phone == student_data['phone']
    assert student.student_type == student_data['student_type']
    assert student.program == student_data['program']
    assert student.status == student_data['status']

def test_student_profile_creation(student_data, student_profile_data):
    student = Student(**student_data)
    profile = StudentProfile(**student_profile_data)
    student.profile = profile
    assert profile.student == student
    assert profile.nationality == student_profile_data['nationality']
    assert profile.date_of_birth == student_profile_data['date_of_birth']
    assert profile.gender == student_profile_data['gender']
    assert profile.address == student_profile_data['address']

def test_student_academic_creation(student_data, student_academic_data):
    student = Student(**student_data)
    academic = StudentAcademic(**student_academic_data)
    student.academic_records.append(academic)
    assert academic.student == student
    assert academic.program == student_academic_data['program']
    assert academic.major == student_academic_data['major']
    assert academic.minor == student_academic_data['minor']
    assert academic.gpa == student_academic_data['gpa']

def test_student_financial_creation(student_data, student_financial_data):
    student = Student(**student_data)
    financial = StudentFinancial(**student_financial_data)
    student.financial_records.append(financial)
    assert financial.student == student
    assert financial.payment_type == student_financial_data['payment_type']
    assert financial.amount == student_financial_data['amount']
    assert financial.status == student_financial_data['status']

def test_student_document_creation(student_data, student_document_data):
    student = Student(**student_data)
    document = StudentDocument(**student_document_data)
    student.documents.append(document)
    assert document.student == student
    assert document.document_type == student_document_data['document_type']
    assert document.file_name == student_document_data['file_name']
    assert document.status == student_document_data['status']

def test_student_enrollment_creation(student_data, student_enrollment_data):
    student = Student(**student_data)
    enrollment = StudentEnrollment(**student_enrollment_data)
    student.enrollments.append(enrollment)
    assert enrollment.student == student
    assert enrollment.course == student_enrollment_data['course']
    assert enrollment.section == student_enrollment_data['section']
    assert enrollment.semester == student_enrollment_data['semester']
    assert enrollment.status == student_enrollment_data['status']

def test_student_attendance_creation(student_data, student_attendance_data):
    student = Student(**student_data)
    attendance = StudentAttendance(**student_attendance_data)
    student.attendance_records.append(attendance)
    assert attendance.student == student
    assert attendance.course == student_attendance_data['course']
    assert attendance.status == student_attendance_data['status']

def test_student_grade_creation(student_data, student_grade_data):
    student = Student(**student_data)
    grade = StudentGrade(**student_grade_data)
    student.grades.append(grade)
    assert grade.student == student
    assert grade.course == student_grade_data['course']
    assert grade.grade == student_grade_data['grade']
    assert grade.grade_points == student_grade_data['grade_points']

def test_student_advising_creation(student_data, student_advising_data):
    student = Student(**student_data)
    advising = StudentAdvising(**student_advising_data)
    student.advising_records.append(advising)
    assert advising.student == student
    assert advising.advisor_id == student_advising_data['advisor_id']
    assert advising.notes == student_advising_data['notes']
    assert advising.status == student_advising_data['status']

def test_student_service_creation(student_data, student_service_data):
    student = Student(**student_data)
    service = StudentService(**student_service_data)
    student.services.append(service)
    assert service.student == student
    assert service.service_type == student_service_data['service_type']
    assert service.notes == student_service_data['notes']
    assert service.status == student_service_data['status']

def test_student_complaint_creation(student_data, student_complaint_data):
    student = Student(**student_data)
    complaint = StudentComplaint(**student_complaint_data)
    student.complaints.append(complaint)
    assert complaint.student == student
    assert complaint.complaint_type == student_complaint_data['complaint_type']
    assert complaint.description == student_complaint_data['description']
    assert complaint.status == student_complaint_data['status']

def test_student_feedback_creation(student_data, student_feedback_data):
    student = Student(**student_data)
    feedback = StudentFeedback(**student_feedback_data)
    student.feedback.append(feedback)
    assert feedback.student == student
    assert feedback.feedback_type == student_feedback_data['feedback_type']
    assert feedback.rating == student_feedback_data['rating']
    assert feedback.comments == student_feedback_data['comments']

def test_student_survey_creation(student_data, student_survey_data):
    student = Student(**student_data)
    survey = StudentSurvey(**student_survey_data)
    student.surveys.append(survey)
    assert survey.student == student
    assert survey.survey_type == student_survey_data['survey_type']
    assert survey.responses == student_survey_data['responses']

def test_student_location_creation(student_data, student_location_data):
    student = Student(**student_data)
    location = StudentLocation(**student_location_data)
    student.locations.append(location)
    assert location.student == student
    assert location.location_type == student_location_data['location_type']
    assert location.building == student_location_data['building']
    assert location.room == student_location_data['room']
    assert location.status == student_location_data['status']

def test_student_contact_creation(student_data, student_contact_data):
    student = Student(**student_data)
    contact = StudentContact(**student_contact_data)
    student.contacts.append(contact)
    assert contact.student == student
    assert contact.contact_type == student_contact_data['contact_type']
    assert contact.name == student_contact_data['name']
    assert contact.relationship == student_contact_data['relationship']
    assert contact.phone == student_contact_data['phone']
    assert contact.email == student_contact_data['email']

def test_student_emergency_creation(student_data, student_emergency_data):
    student = Student(**student_data)
    emergency = StudentEmergency(**student_emergency_data)
    student.emergencies.append(emergency)
    assert emergency.student == student
    assert emergency.emergency_type == student_emergency_data['emergency_type']
    assert emergency.description == student_emergency_data['description']
    assert emergency.status == student_emergency_data['status']

def test_student_to_dict(student_data):
    student = Student(**student_data)
    student_dict = student.to_dict()
    assert student_dict['student_id'] == student_data['student_id']
    assert student_dict['first_name'] == student_data['first_name']
    assert student_dict['last_name'] == student_data['last_name']
    assert student_dict['email'] == student_data['email']
    assert student_dict['phone'] == student_data['phone']
    assert student_dict['student_type'] == student_data['student_type']
    assert student_dict['program'] == student_data['program']
    assert student_dict['status'] == student_data['status']

def test_student_validation():
    with pytest.raises(ValueError):
        Student(
            student_id='STU001',
            first_name='John',
            last_name='Doe',
            email='invalid-email',
            phone='1234567890',
            student_type='invalid_type',
            program='Computer Science',
            enrollment_date=datetime.now(),
            status='active'
        ) 