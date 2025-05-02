from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime

class BaseSchema(Schema):
    """Base schema with common fields and validation methods."""
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class PaginationSchema(Schema):
    """Schema for pagination parameters."""
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=10, validate=validate.Range(min=1, max=100))

class ErrorSchema(Schema):
    """Schema for error responses."""
    status = fields.Str(required=True)
    message = fields.Str(required=True)
    errors = fields.Dict(keys=fields.Str(), values=fields.List(fields.Str()))

class SuccessSchema(Schema):
    """Schema for success responses."""
    status = fields.Str(required=True)
    message = fields.Str(required=True)
    data = fields.Dict(required=True)

class DateRangeSchema(Schema):
    """Schema for date range parameters."""
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

    @validates('end_date')
    def validate_date_range(self, value, **kwargs):
        start_date = self.context.get('start_date')
        if start_date and value < start_date:
            raise ValidationError('End date must be after start date')

class FileUploadSchema(Schema):
    """Schema for file upload parameters."""
    file = fields.Raw(required=True)
    description = fields.Str(required=False)
    tags = fields.List(fields.Str(), required=False)

class SearchSchema(Schema):
    """Schema for search parameters."""
    query = fields.Str(required=True)
    filters = fields.Dict(keys=fields.Str(), values=fields.Str(), required=False)
    sort_by = fields.Str(required=False)
    sort_order = fields.Str(validate=validate.OneOf(['asc', 'desc']), required=False)

class AuditSchema(Schema):
    """Schema for audit trail entries."""
    user_id = fields.Int(required=True)
    action = fields.Str(required=True)
    timestamp = fields.DateTime(dump_only=True)
    details = fields.Dict(required=False) 