from datetime import datetime
from typing import List, Dict, Any, Optional
from . import db, cache
from .models import BaseModel, AuditLog
from .exceptions import (
    ValidationError, NotFoundError, UnauthorizedError,
    ForbiddenError, ConflictError
)
from .utils import format_response, paginate_query

class BaseService:
    """Base service class with common operations."""
    
    def __init__(self, model_class: BaseModel):
        self.model_class = model_class
    
    def get_by_id(self, id: int) -> BaseModel:
        """Get model instance by ID."""
        instance = self.model_class.get_by_id(id)
        if not instance:
            raise NotFoundError(f"{self.model_class.__name__} with ID {id} not found")
        return instance
    
    def get_all(self, page: int = 1, per_page: int = 10) -> Dict:
        """Get all model instances with pagination."""
        query = self.model_class.query
        return paginate_query(query, page, per_page)
    
    def create(self, data: Dict[str, Any], user_id: Optional[int] = None) -> BaseModel:
        """Create a new model instance."""
        try:
            instance = self.model_class(**data)
            instance.save()
            
            # Log the creation
            AuditLog(
                model_name=self.model_class.__name__,
                model_id=instance.id,
                action='create',
                changes=data,
                user_id=user_id
            ).save()
            
            return instance
        except Exception as e:
            raise ValidationError(str(e))
    
    def update(self, id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> BaseModel:
        """Update an existing model instance."""
        instance = self.get_by_id(id)
        
        try:
            for key, value in data.items():
                setattr(instance, key, value)
            
            # Log the changes
            AuditLog(
                model_name=self.model_class.__name__,
                model_id=instance.id,
                action='update',
                changes=data,
                user_id=user_id
            ).save()
            
            instance.save()
            return instance
        except Exception as e:
            raise ValidationError(str(e))
    
    def delete(self, id: int, user_id: Optional[int] = None) -> None:
        """Delete a model instance."""
        instance = self.get_by_id(id)
        
        try:
            # Log the deletion
            AuditLog(
                model_name=self.model_class.__name__,
                model_id=instance.id,
                action='delete',
                user_id=user_id
            ).save()
            
            instance.delete()
        except Exception as e:
            raise ValidationError(str(e))
    
    def search(self, query: str, page: int = 1, per_page: int = 10) -> Dict:
        """Search model instances."""
        # Implement search logic here
        results = []
        return {
            'results': results,
            'total': len(results),
            'page': page,
            'per_page': per_page
        }

class AuditLogService(BaseService):
    """Service for audit log operations."""
    
    def __init__(self):
        super().__init__(AuditLog)
    
    def get_by_model(self, model_name: str, model_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get audit logs for a specific model instance."""
        query = AuditLog.query.filter_by(
            model_name=model_name,
            model_id=model_id
        ).order_by(AuditLog.created_at.desc())
        
        return paginate_query(query, page, per_page)
    
    def get_by_user(self, user_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Get audit logs for a specific user."""
        query = AuditLog.query.filter_by(user_id=user_id).order_by(AuditLog.created_at.desc())
        return paginate_query(query, page, per_page)
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime, page: int = 1, per_page: int = 10) -> Dict:
        """Get audit logs within a date range."""
        query = AuditLog.query.filter(
            AuditLog.created_at.between(start_date, end_date)
        ).order_by(AuditLog.created_at.desc())
        
        return paginate_query(query, page, per_page) 