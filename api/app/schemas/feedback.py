from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FeedbackBase(BaseModel):
    """Base feedback schema."""
    content: str
    feeling: Optional[str] = None


class FeedbackCreate(FeedbackBase):
    """Schema for creating feedback."""
    pass


class FeedbackResponse(FeedbackBase):
    """Schema for feedback response."""
    id: int
    task_id: int
    student_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
