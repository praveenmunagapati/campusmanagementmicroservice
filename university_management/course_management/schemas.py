from marshmallow import Schema, fields, validate
from .base_schemas import BaseSchema


class CourseSchema(BaseSchema):
    """Schema for Course."""
    # Add schema-specific fields here
    pass

class CourseSectionSchema(BaseSchema):
    """Schema for CourseSection."""
    # Add schema-specific fields here
    pass

class CourseScheduleSchema(BaseSchema):
    """Schema for CourseSchedule."""
    # Add schema-specific fields here
    pass

class CourseMaterialSchema(BaseSchema):
    """Schema for CourseMaterial."""
    # Add schema-specific fields here
    pass

class CourseAssignmentSchema(BaseSchema):
    """Schema for CourseAssignment."""
    # Add schema-specific fields here
    pass

class CourseGradeSchema(BaseSchema):
    """Schema for CourseGrade."""
    # Add schema-specific fields here
    pass

class CoursePrerequisiteSchema(BaseSchema):
    """Schema for CoursePrerequisite."""
    # Add schema-specific fields here
    pass

class CourseEnrollmentSchema(BaseSchema):
    """Schema for CourseEnrollment."""
    # Add schema-specific fields here
    pass

class CourseEvaluationSchema(BaseSchema):
    """Schema for CourseEvaluation."""
    # Add schema-specific fields here
    pass
