from .base_services import BaseService
from .models import *


class CourseService(BaseService):
    """Service for Course operations."""
    
    def __init__(self):
        super().__init__(Course)
    
    # Add service-specific methods here
    pass

class CourseSectionService(BaseService):
    """Service for CourseSection operations."""
    
    def __init__(self):
        super().__init__(CourseSection)
    
    # Add service-specific methods here
    pass

class CourseScheduleService(BaseService):
    """Service for CourseSchedule operations."""
    
    def __init__(self):
        super().__init__(CourseSchedule)
    
    # Add service-specific methods here
    pass

class CourseMaterialService(BaseService):
    """Service for CourseMaterial operations."""
    
    def __init__(self):
        super().__init__(CourseMaterial)
    
    # Add service-specific methods here
    pass

class CourseAssignmentService(BaseService):
    """Service for CourseAssignment operations."""
    
    def __init__(self):
        super().__init__(CourseAssignment)
    
    # Add service-specific methods here
    pass

class CourseGradeService(BaseService):
    """Service for CourseGrade operations."""
    
    def __init__(self):
        super().__init__(CourseGrade)
    
    # Add service-specific methods here
    pass

class CoursePrerequisiteService(BaseService):
    """Service for CoursePrerequisite operations."""
    
    def __init__(self):
        super().__init__(CoursePrerequisite)
    
    # Add service-specific methods here
    pass

class CourseEnrollmentService(BaseService):
    """Service for CourseEnrollment operations."""
    
    def __init__(self):
        super().__init__(CourseEnrollment)
    
    # Add service-specific methods here
    pass

class CourseEvaluationService(BaseService):
    """Service for CourseEvaluation operations."""
    
    def __init__(self):
        super().__init__(CourseEvaluation)
    
    # Add service-specific methods here
    pass
