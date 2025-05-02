from .base_services import BaseService
from .models import *


class FacultyService(BaseService):
    """Service for Faculty operations."""
    
    def __init__(self):
        super().__init__(Faculty)
    
    # Add service-specific methods here
    pass

class FacultyProfileService(BaseService):
    """Service for FacultyProfile operations."""
    
    def __init__(self):
        super().__init__(FacultyProfile)
    
    # Add service-specific methods here
    pass

class FacultyAcademicService(BaseService):
    """Service for FacultyAcademic operations."""
    
    def __init__(self):
        super().__init__(FacultyAcademic)
    
    # Add service-specific methods here
    pass

class FacultyScheduleService(BaseService):
    """Service for FacultySchedule operations."""
    
    def __init__(self):
        super().__init__(FacultySchedule)
    
    # Add service-specific methods here
    pass

class FacultyResearchService(BaseService):
    """Service for FacultyResearch operations."""
    
    def __init__(self):
        super().__init__(FacultyResearch)
    
    # Add service-specific methods here
    pass

class FacultyPublicationService(BaseService):
    """Service for FacultyPublication operations."""
    
    def __init__(self):
        super().__init__(FacultyPublication)
    
    # Add service-specific methods here
    pass

class FacultyGrantService(BaseService):
    """Service for FacultyGrant operations."""
    
    def __init__(self):
        super().__init__(FacultyGrant)
    
    # Add service-specific methods here
    pass

class FacultyAdvisingService(BaseService):
    """Service for FacultyAdvising operations."""
    
    def __init__(self):
        super().__init__(FacultyAdvising)
    
    # Add service-specific methods here
    pass

class FacultyEvaluationService(BaseService):
    """Service for FacultyEvaluation operations."""
    
    def __init__(self):
        super().__init__(FacultyEvaluation)
    
    # Add service-specific methods here
    pass

class FacultyDevelopmentService(BaseService):
    """Service for FacultyDevelopment operations."""
    
    def __init__(self):
        super().__init__(FacultyDevelopment)
    
    # Add service-specific methods here
    pass
