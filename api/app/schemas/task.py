from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.task import TaskType, TaskStatus


class TaskBase(BaseModel):
    """Base task schema."""
    student_id: int
    type: TaskType
    title: str
    description: Optional[str] = None
    musical_piece_id: Optional[int] = None
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    musical_piece_id: Optional[int] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None


class TaskStatusUpdate(BaseModel):
    """Schema for updating task status."""
    status: TaskStatus


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: int
    teacher_id: int
    status: TaskStatus
    created_at: datetime
    
    class Config:
        from_attributes = True
