from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime
from .utils import validate_email, validate_phone

class BaseSchema(Schema):
    """Base schema with common fields."""
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class AuditLogSchema(Schema):
    """Schema for AuditLog model."""
    id = fields.Int(dump_only=True)
    model_name = fields.Str(required=True)
    model_id = fields.Int(required=True)
    action = fields.Str(required=True, validate=validate.OneOf(['create', 'update', 'delete']))
    changes = fields.Dict()
    user_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)

class PaginationSchema(Schema):
    """Schema for paginated responses."""
    items = fields.List(fields.Dict())
    total = fields.Int()
    pages = fields.Int()
    current_page = fields.Int()
    has_next = fields.Bool()
    has_prev = fields.Bool()

class ErrorSchema(Schema):
    """Schema for error responses."""
    status = fields.Str(default='error')
    message = fields.Str(required=True)
    errors = fields.Dict()
    timestamp = fields.DateTime(dump_only=True)

class SuccessSchema(Schema):
    """Schema for success responses."""
    status = fields.Str(default='success')
    message = fields.Str(required=True)
    data = fields.Dict()
    timestamp = fields.DateTime(dump_only=True)

class EmailSchema(Schema):
    """Schema for email validation."""
    email = fields.Email(required=True)
    
    @validates('email')
    def validate_email_format(self, value):
        if not validate_email(value):
            raise ValidationError('Invalid email format')
        return value

class PhoneSchema(Schema):
    """Schema for phone number validation."""
    phone = fields.Str(required=True)
    country_code = fields.Str(default='US')
    
    @validates('phone')
    def validate_phone_format(self, value, **kwargs):
        country_code = self.context.get('country_code', 'US')
        if not validate_phone(value, country_code):
            raise ValidationError('Invalid phone number format')
        return value

class DateRangeSchema(Schema):
    """Schema for date range validation."""
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    
    @validates('end_date')
    def validate_date_range(self, value, **kwargs):
        start_date = self.context.get('start_date')
        if start_date and value < start_date:
            raise ValidationError('End date must be after start date')
        return value

class SearchSchema(Schema):
    """Schema for search parameters."""
    query = fields.Str()
    page = fields.Int(default=1)
    per_page = fields.Int(default=10)
    sort_by = fields.Str()
    sort_order = fields.Str(validate=validate.OneOf(['asc', 'desc']))
    filters = fields.Dict() 