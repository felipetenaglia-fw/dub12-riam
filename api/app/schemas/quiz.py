from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class QuizQuestion(BaseModel):
    """Schema for a quiz question (free text)."""
    question: str
    topic: Optional[str] = None  # e.g., "harmony", "performance", "composition"


class QuizBase(BaseModel):
    """Base quiz schema."""
    task_id: int
    musical_piece_id: Optional[int] = None
    questions: List[QuizQuestion]


class QuizCreate(QuizBase):
    """Schema for creating a quiz."""
    pass


class QuizResponse(BaseModel):
    """Schema for quiz response."""
    id: int
    task_id: int
    musical_piece_id: Optional[int] = None
    questions: List[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True


class QuizAnswer(BaseModel):
    """Schema for a quiz answer (free text)."""
    question_index: int
    answer: str


class QuizResponseCreate(BaseModel):
    """Schema for creating a quiz response."""
    answers: List[QuizAnswer]


class QuizResponseData(BaseModel):
    """Schema for quiz response data."""
    id: int
    quiz_id: int
    student_id: int
    answers: List[Dict[str, Any]]
    submitted_at: datetime
    
    class Config:
        from_attributes = True
