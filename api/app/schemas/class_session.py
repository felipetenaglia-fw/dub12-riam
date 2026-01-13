from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ClassSessionBase(BaseModel):
    """Base class session schema."""
    student_id: int
    notes: Optional[str] = None
    improvement_points: Optional[str] = None
    actions: Optional[str] = None


class ClassSessionCreate(ClassSessionBase):
    """Schema for creating a class session."""
    date: Optional[datetime] = None


class ClassSessionUpdate(BaseModel):
    """Schema for updating a class session."""
    notes: Optional[str] = None
    improvement_points: Optional[str] = None
    actions: Optional[str] = None


class ClassSessionResponse(ClassSessionBase):
    """Schema for class session response."""
    id: int
    teacher_id: int
    date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
