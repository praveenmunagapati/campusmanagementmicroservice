from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime
from .utils import validate_email, validate_phone

class BaseSchema(Schema):
    """Base schema with common fields and validation methods."""
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class StudentSchema(BaseSchema):
    """Schema for Student model."""
    student_id = fields.Str(required=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    student_type = fields.Str(required=True, validate=validate.OneOf(['undergraduate', 'graduate', 'phd']))
    program = fields.Str(required=True)
    enrollment_date = fields.Date(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(['active', 'inactive', 'graduated', 'suspended']))

    @validates('email')
    def validate_email_format(self, value):
        validate_email(value)
        return value

    @validates('phone')
    def validate_phone_format(self, value):
        validate_phone(value)
        return value

class StudentProfileSchema(BaseSchema):
    """Schema for StudentProfile model."""
    student_id = fields.Int(required=True)
    date_of_birth = fields.Date(required=True)
    gender = fields.Str(validate=validate.OneOf(['male', 'female', 'other']))
    nationality = fields.Str()
    address = fields.Str()
    emergency_contact = fields.Str()
    medical_conditions = fields.Str()
    disabilities = fields.Str()

class StudentAcademicSchema(BaseSchema):
    """Schema for StudentAcademic model."""
    student_id = fields.Int(required=True)
    gpa = fields.Float(validate=validate.Range(min=0.0, max=4.0))
    credits_earned = fields.Int(validate=validate.Range(min=0))
    current_semester = fields.Str()
    major = fields.Str()
    minor = fields.Str()
    advisor_id = fields.Int()

class StudentFinancialSchema(BaseSchema):
    """Schema for StudentFinancial model."""
    student_id = fields.Int(required=True)
    tuition_balance = fields.Float(validate=validate.Range(min=0.0))
    financial_aid_status = fields.Str(validate=validate.OneOf(['pending', 'approved', 'rejected']))
    scholarship_status = fields.Str(validate=validate.OneOf(['pending', 'approved', 'rejected']))
    payment_plan = fields.Str()

class StudentDocumentSchema(BaseSchema):
    """Schema for StudentDocument model."""
    student_id = fields.Int(required=True)
    document_type = fields.Str(required=True)
    file_path = fields.Str(required=True)
    upload_date = fields.DateTime(required=True)
    status = fields.Str(validate=validate.OneOf(['pending', 'approved', 'rejected']))

class StudentEnrollmentSchema(BaseSchema):
    """Schema for StudentEnrollment model."""
    student_id = fields.Int(required=True)
    course_id = fields.Int(required=True)
    semester = fields.Str(required=True)
    enrollment_date = fields.DateTime(required=True)
    status = fields.Str(validate=validate.OneOf(['enrolled', 'dropped', 'completed']))

class StudentAttendanceSchema(BaseSchema):
    """Schema for StudentAttendance model."""
    student_id = fields.Int(required=True)
    course_id = fields.Int(required=True)
    date = fields.Date(required=True)
    status = fields.Str(validate=validate.OneOf(['present', 'absent', 'late']))
    reason = fields.Str()

class StudentGradeSchema(BaseSchema):
    """Schema for StudentGrade model."""
    student_id = fields.Int(required=True)
    course_id = fields.Int(required=True)
    grade = fields.Str(validate=validate.OneOf(['A', 'B', 'C', 'D', 'F', 'W', 'I']))
    grade_points = fields.Float(validate=validate.Range(min=0.0, max=4.0))
    semester = fields.Str(required=True)
    comments = fields.Str()

class StudentAdvisingSchema(BaseSchema):
    """Schema for StudentAdvising model."""
    student_id = fields.Int(required=True)
    advisor_id = fields.Int(required=True)
    meeting_date = fields.DateTime(required=True)
    meeting_type = fields.Str(validate=validate.OneOf(['academic', 'career', 'personal']))
    notes = fields.Str()
    follow_up_date = fields.DateTime()

class StudentServiceSchema(BaseSchema):
    """Schema for StudentService model."""
    student_id = fields.Int(required=True)
    service_type = fields.Str(required=True)
    request_date = fields.DateTime(required=True)
    status = fields.Str(validate=validate.OneOf(['pending', 'in_progress', 'completed', 'cancelled']))
    description = fields.Str()
    resolution = fields.Str()

class StudentComplaintSchema(BaseSchema):
    """Schema for StudentComplaint model."""
    student_id = fields.Int(required=True)
    complaint_type = fields.Str(required=True)
    submission_date = fields.DateTime(required=True)
    status = fields.Str(validate=validate.OneOf(['open', 'in_progress', 'resolved', 'closed']))
    description = fields.Str(required=True)
    resolution = fields.Str()

class StudentFeedbackSchema(BaseSchema):
    """Schema for StudentFeedback model."""
    student_id = fields.Int(required=True)
    feedback_type = fields.Str(required=True)
    submission_date = fields.DateTime(required=True)
    rating = fields.Int(validate=validate.Range(min=1, max=5))
    comments = fields.Str()
    response = fields.Str()

class StudentSurveySchema(BaseSchema):
    """Schema for StudentSurvey model."""
    student_id = fields.Int(required=True)
    survey_type = fields.Str(required=True)
    submission_date = fields.DateTime(required=True)
    responses = fields.Dict(keys=fields.Str(), values=fields.Raw())
    status = fields.Str(validate=validate.OneOf(['pending', 'completed']))

class StudentLocationSchema(BaseSchema):
    """Schema for StudentLocation model."""
    student_id = fields.Int(required=True)
    building = fields.Str(required=True)
    room = fields.Str(required=True)
    check_in_time = fields.DateTime(required=True)
    check_out_time = fields.DateTime()
    purpose = fields.Str()

class StudentContactSchema(BaseSchema):
    """Schema for StudentContact model."""
    student_id = fields.Int(required=True)
    contact_type = fields.Str(required=True, validate=validate.OneOf(['email', 'phone', 'address']))
    value = fields.Str(required=True)
    is_primary = fields.Bool(default=False)

    @validates('value')
    def validate_contact_value(self, value, **kwargs):
        contact_type = self.context.get('contact_type')
        if contact_type == 'email':
            validate_email(value)
        elif contact_type == 'phone':
            validate_phone(value)
        return value

class StudentEmergencySchema(BaseSchema):
    """Schema for StudentEmergency model."""
    student_id = fields.Int(required=True)
    contact_name = fields.Str(required=True)
    relationship = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email()
    address = fields.Str()

    @validates('phone')
    def validate_phone_format(self, value):
        validate_phone(value)
        return value 