from marshmallow import Schema, fields, validate, validates, ValidationError
from .base_schemas import BaseSchema, EmailSchema, PhoneSchema, DateRangeSchema


class StudentSchema(BaseSchema):
    """Schema for Student model."""
    student_id = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str()
    date_of_birth = fields.Date()
    gender = fields.Str(validate=validate.OneOf(['male', 'female', 'other']))
    nationality = fields.Str()
    status = fields.Str(validate=validate.OneOf(['active', 'inactive', 'graduated', 'suspended']))
    program_id = fields.Int()
    department_id = fields.Int()
    advisor_id = fields.Int()

class StudentProfileSchema(BaseSchema):
    """Schema for StudentProfile model."""
    student_id = fields.Int(required=True)
    address = fields.Str()
    city = fields.Str()
    state = fields.Str()
    country = fields.Str()
    postal_code = fields.Str()
    emergency_contact = fields.Str()
    emergency_phone = fields.Str()
    blood_group = fields.Str(validate=validate.OneOf(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']))
    medical_conditions = fields.Str()
    photo_url = fields.URL()

class StudentAcademicSchema(BaseSchema):
    """Schema for StudentAcademic model."""
    student_id = fields.Int(required=True)
    program_id = fields.Int()
    semester = fields.Str(required=True)
    year = fields.Int(required=True)
    gpa = fields.Float(validate=validate.Range(min=0, max=4.0))
    credits_earned = fields.Int(validate=validate.Range(min=0))
    credits_remaining = fields.Int(validate=validate.Range(min=0))
    academic_status = fields.Str(validate=validate.OneOf(['good', 'probation', 'warning', 'suspended']))
    graduation_date = fields.Date()
    honors = fields.Str()

class StudentFinancialSchema(BaseSchema):
    """Schema for StudentFinancial model."""
    student_id = fields.Int(required=True)
    tuition_fee = fields.Float(validate=validate.Range(min=0))
    scholarship_amount = fields.Float(validate=validate.Range(min=0))
    financial_aid_amount = fields.Float(validate=validate.Range(min=0))
    payment_status = fields.Str(validate=validate.OneOf(['paid', 'partial', 'unpaid', 'overdue']))
    payment_due_date = fields.Date()
    payment_history = fields.Dict()

class StudentDocumentSchema(BaseSchema):
    """Schema for StudentDocument model."""
    student_id = fields.Int(required=True)
    document_type = fields.Str(required=True)
    document_name = fields.Str(required=True)
    document_url = fields.URL(required=True)
    upload_date = fields.DateTime()
    status = fields.Str(validate=validate.OneOf(['pending', 'verified', 'rejected']))
    verified_by = fields.Int()
    verification_date = fields.DateTime()

class StudentEnrollmentSchema(BaseSchema):
    """Schema for StudentEnrollment model."""
    student_id = fields.Int(required=True)
    course_id = fields.Int(required=True)
    section_id = fields.Int(required=True)
    semester = fields.Str(required=True)
    year = fields.Int(required=True)
    enrollment_date = fields.DateTime()
    status = fields.Str(validate=validate.OneOf(['active', 'dropped', 'withdrawn', 'completed']))
    grade = fields.Str(validate=validate.OneOf(['A', 'B', 'C', 'D', 'F', 'W', 'I']))
    credits = fields.Int(validate=validate.Range(min=0))

class StudentAttendanceSchema(BaseSchema):
    """Schema for StudentAttendance model."""
    student_id = fields.Int(required=True)
    course_id = fields.Int(required=True)
    section_id = fields.Int(required=True)
    date = fields.Date(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(['present', 'absent', 'late']))
    reason = fields.Str()
    verified_by = fields.Int()

class StudentGradeSchema(BaseSchema):
    """Schema for StudentGrade model."""
    student_id = fields.Int(required=True)
    course_id = fields.Int(required=True)
    section_id = fields.Int(required=True)
    semester = fields.Str(required=True)
    year = fields.Int(required=True)
    grade = fields.Str(required=True, validate=validate.OneOf(['A', 'B', 'C', 'D', 'F', 'W', 'I']))
    grade_points = fields.Float(validate=validate.Range(min=0, max=4.0))
    credits = fields.Int(validate=validate.Range(min=0))
    remarks = fields.Str()
    posted_by = fields.Int()
    posted_date = fields.DateTime()

class StudentAdvisingSchema(BaseSchema):
    """Schema for StudentAdvising model."""
    student_id = fields.Int(required=True)
    advisor_id = fields.Int(required=True)
    meeting_date = fields.DateTime(required=True)
    meeting_type = fields.Str(validate=validate.OneOf(['academic', 'career', 'personal']))
    notes = fields.Str()
    follow_up_date = fields.DateTime()
    status = fields.Str(validate=validate.OneOf(['scheduled', 'completed', 'cancelled', 'rescheduled']))

class StudentServiceSchema(BaseSchema):
    """Schema for StudentService model."""
    student_id = fields.Int(required=True)
    service_type = fields.Str(required=True, validate=validate.OneOf(['counseling', 'career', 'health']))
    service_date = fields.DateTime(required=True)
    provider = fields.Str()
    notes = fields.Str()
    status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'cancelled']))
    follow_up_date = fields.DateTime()

class StudentComplaintSchema(BaseSchema):
    """Schema for StudentComplaint model."""
    student_id = fields.Int(required=True)
    complaint_type = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(validate=validate.OneOf(['open', 'in_progress', 'resolved', 'closed']))
    priority = fields.Str(validate=validate.OneOf(['low', 'medium', 'high', 'urgent']))
    assigned_to = fields.Int()
    resolution = fields.Str()
    resolution_date = fields.DateTime()

class StudentFeedbackSchema(BaseSchema):
    """Schema for StudentFeedback model."""
    student_id = fields.Int(required=True)
    feedback_type = fields.Str(required=True, validate=validate.OneOf(['course', 'faculty', 'service']))
    target_id = fields.Int(required=True)
    rating = fields.Int(validate=validate.Range(min=1, max=5))
    comments = fields.Str()
    submission_date = fields.DateTime()
    status = fields.Str(validate=validate.OneOf(['submitted', 'reviewed', 'archived']))

class StudentSurveySchema(BaseSchema):
    """Schema for StudentSurvey model."""
    student_id = fields.Int(required=True)
    survey_id = fields.Int(required=True)
    responses = fields.Dict(required=True)
    submission_date = fields.DateTime()
    status = fields.Str(validate=validate.OneOf(['completed', 'in_progress', 'not_started']))

class StudentLocationSchema(BaseSchema):
    """Schema for StudentLocation model."""
    student_id = fields.Int(required=True)
    building = fields.Str()
    room = fields.Str()
    check_in_time = fields.DateTime()
    check_out_time = fields.DateTime()
    purpose = fields.Str()
    status = fields.Str(validate=validate.OneOf(['active', 'inactive']))

class StudentContactSchema(BaseSchema):
    """Schema for StudentContact model."""
    student_id = fields.Int(required=True)
    contact_type = fields.Str(required=True, validate=validate.OneOf(['phone', 'email', 'address']))
    value = fields.Str(required=True)
    is_primary = fields.Bool()
    is_verified = fields.Bool()
    verification_date = fields.DateTime()

class StudentEmergencySchema(BaseSchema):
    """Schema for StudentEmergency model."""
    student_id = fields.Int(required=True)
    name = fields.Str(required=True)
    relationship = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email()
    address = fields.Str()
    is_primary = fields.Bool()
