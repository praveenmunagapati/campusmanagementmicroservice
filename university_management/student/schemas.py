from marshmallow import Schema, fields, validate, validates_schema
from datetime import datetime

class StudentSchema(Schema):
    student_id = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    phone = fields.Str(required=True, validate=validate.Length(min=10, max=15))
    student_type = fields.Str(required=True, validate=validate.OneOf(['undergraduate', 'graduate', 'phd']))
    program = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    enrollment_date = fields.DateTime(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(['active', 'inactive', 'graduated', 'withdrawn']))

class StudentProfileSchema(Schema):
    nationality = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    date_of_birth = fields.DateTime(required=True)
    gender = fields.Str(required=True, validate=validate.OneOf(['male', 'female', 'other']))
    address = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    city = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    state = fields.Str(validate=validate.Length(max=100))
    zip_code = fields.Str(validate=validate.Length(max=20))
    country = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    status = fields.Str(required=True, validate=validate.OneOf(['active', 'inactive']))

class StudentAcademicSchema(Schema):
    program = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    major = fields.Str(validate=validate.Length(max=100))
    minor = fields.Str(validate=validate.Length(max=100))
    start_date = fields.DateTime(required=True)
    expected_graduation = fields.DateTime()
    gpa = fields.Float(validate=validate.Range(min=0, max=4))
    status = fields.Str(required=True, validate=validate.OneOf(['active', 'completed', 'transferred']))

class StudentFinancialSchema(Schema):
    payment_type = fields.Str(required=True, validate=validate.OneOf(['tuition', 'fees', 'housing', 'meal_plan', 'other']))
    amount = fields.Float(required=True, validate=validate.Range(min=0))
    payment_date = fields.DateTime(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(['paid', 'pending', 'overdue', 'cancelled']))

class StudentDocumentSchema(Schema):
    document_type = fields.Str(required=True, validate=validate.OneOf(['transcript', 'certificate', 'id_card', 'other']))
    file_name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    file_path = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    upload_date = fields.DateTime(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(['verified', 'pending', 'rejected']))

class StudentEnrollmentSchema(Schema):
    course = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    section = fields.Str(required=True, validate=validate.Length(min=1, max=10))
    semester = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    enrollment_date = fields.DateTime(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(['enrolled', 'dropped', 'completed', 'withdrawn']))

class StudentAttendanceSchema(Schema):
    course = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    attendance_date = fields.DateTime(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(['present', 'absent', 'late', 'excused']))

class StudentGradeSchema(Schema):
    course = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    grade = fields.Str(required=True, validate=validate.Length(min=1, max=2))
    grade_points = fields.Float(required=True, validate=validate.Range(min=0, max=4))
    grade_date = fields.DateTime(required=True)

class StudentAdvisingSchema(Schema):
    advisor_id = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    advising_date = fields.DateTime(required=True)
    notes = fields.Str()
    status = fields.Str(required=True, validate=validate.OneOf(['scheduled', 'completed', 'cancelled']))

class StudentServiceSchema(Schema):
    service_type = fields.Str(required=True, validate=validate.OneOf(['counseling', 'tutoring', 'career', 'health', 'other']))
    service_date = fields.DateTime(required=True)
    notes = fields.Str()
    status = fields.Str(required=True, validate=validate.OneOf(['scheduled', 'completed', 'cancelled']))

class StudentComplaintSchema(Schema):
    complaint_type = fields.Str(required=True, validate=validate.OneOf(['academic', 'administrative', 'facility', 'other']))
    description = fields.Str(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(['pending', 'in_progress', 'resolved', 'rejected']))

class StudentFeedbackSchema(Schema):
    feedback_type = fields.Str(required=True, validate=validate.OneOf(['course', 'faculty', 'facility', 'service', 'other']))
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    comments = fields.Str()

class StudentSurveySchema(Schema):
    survey_type = fields.Str(required=True, validate=validate.OneOf(['course_evaluation', 'faculty_evaluation', 'service_evaluation', 'other']))
    responses = fields.Dict(required=True)

class StudentLocationSchema(Schema):
    location_type = fields.Str(required=True, validate=validate.OneOf(['residence', 'classroom', 'library', 'other']))
    building = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    room = fields.Str(validate=validate.Length(max=20))
    status = fields.Str(required=True, validate=validate.OneOf(['active', 'inactive']))

class StudentContactSchema(Schema):
    contact_type = fields.Str(required=True, validate=validate.OneOf(['emergency', 'parent', 'guardian', 'other']))
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    relationship = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    phone = fields.Str(required=True, validate=validate.Length(min=10, max=15))
    email = fields.Email()

class StudentEmergencySchema(Schema):
    emergency_type = fields.Str(required=True, validate=validate.OneOf(['medical', 'security', 'other']))
    description = fields.Str(required=True)
    occurred_at = fields.DateTime(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(['active', 'resolved'])) 