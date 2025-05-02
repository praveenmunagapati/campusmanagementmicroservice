from datetime import datetime
from . import db
from .base_models import BaseModel


class Course(BaseModel):
    """Model for Course."""
    __tablename__ = 'courses'
    
    # Add model-specific fields here
    pass

class CourseSection(BaseModel):
    """Model for CourseSection."""
    __tablename__ = 'coursesections'
    
    # Add model-specific fields here
    pass

class CourseSchedule(BaseModel):
    """Model for CourseSchedule."""
    __tablename__ = 'courseschedules'
    
    # Add model-specific fields here
    pass

class CourseMaterial(BaseModel):
    """Model for CourseMaterial."""
    __tablename__ = 'coursematerials'
    
    # Add model-specific fields here
    pass

class CourseAssignment(BaseModel):
    """Model for CourseAssignment."""
    __tablename__ = 'courseassignments'
    
    # Add model-specific fields here
    pass

class CourseGrade(BaseModel):
    """Model for CourseGrade."""
    __tablename__ = 'coursegrades'
    
    # Add model-specific fields here
    pass

class CoursePrerequisite(BaseModel):
    """Model for CoursePrerequisite."""
    __tablename__ = 'courseprerequisites'
    
    # Add model-specific fields here
    pass

class CourseEnrollment(BaseModel):
    """Model for CourseEnrollment."""
    __tablename__ = 'courseenrollments'
    
    # Add model-specific fields here
    pass

class CourseEvaluation(BaseModel):
    """Model for CourseEvaluation."""
    __tablename__ = 'courseevaluations'
    
    # Add model-specific fields here
    pass
