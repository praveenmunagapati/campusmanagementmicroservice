from datetime import datetime
from . import db
from .base_models import BaseModel


class Student(BaseModel):
    """Model for Student."""
    __tablename__ = 'students'
    
    # Add model-specific fields here
    pass

class StudentProfile(BaseModel):
    """Model for StudentProfile."""
    __tablename__ = 'studentprofiles'
    
    # Add model-specific fields here
    pass

class StudentAcademic(BaseModel):
    """Model for StudentAcademic."""
    __tablename__ = 'studentacademics'
    
    # Add model-specific fields here
    pass

class StudentFinancial(BaseModel):
    """Model for StudentFinancial."""
    __tablename__ = 'studentfinancials'
    
    # Add model-specific fields here
    pass

class StudentDocument(BaseModel):
    """Model for StudentDocument."""
    __tablename__ = 'studentdocuments'
    
    # Add model-specific fields here
    pass

class StudentEnrollment(BaseModel):
    """Model for StudentEnrollment."""
    __tablename__ = 'studentenrollments'
    
    # Add model-specific fields here
    pass

class StudentAttendance(BaseModel):
    """Model for StudentAttendance."""
    __tablename__ = 'studentattendances'
    
    # Add model-specific fields here
    pass

class StudentGrade(BaseModel):
    """Model for StudentGrade."""
    __tablename__ = 'studentgrades'
    
    # Add model-specific fields here
    pass

class StudentAdvising(BaseModel):
    """Model for StudentAdvising."""
    __tablename__ = 'studentadvisings'
    
    # Add model-specific fields here
    pass

class StudentService(BaseModel):
    """Model for StudentService."""
    __tablename__ = 'studentservices'
    
    # Add model-specific fields here
    pass

class StudentComplaint(BaseModel):
    """Model for StudentComplaint."""
    __tablename__ = 'studentcomplaints'
    
    # Add model-specific fields here
    pass

class StudentFeedback(BaseModel):
    """Model for StudentFeedback."""
    __tablename__ = 'studentfeedbacks'
    
    # Add model-specific fields here
    pass

class StudentSurvey(BaseModel):
    """Model for StudentSurvey."""
    __tablename__ = 'studentsurveys'
    
    # Add model-specific fields here
    pass

class StudentLocation(BaseModel):
    """Model for StudentLocation."""
    __tablename__ = 'studentlocations'
    
    # Add model-specific fields here
    pass

class StudentContact(BaseModel):
    """Model for StudentContact."""
    __tablename__ = 'studentcontacts'
    
    # Add model-specific fields here
    pass

class StudentEmergency(BaseModel):
    """Model for StudentEmergency."""
    __tablename__ = 'studentemergencys'
    
    # Add model-specific fields here
    pass
