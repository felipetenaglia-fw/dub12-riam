from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, JSON
from datetime import datetime
from ..database import Base


class Quiz(Base):
    """Quiz for listening tasks (free text questions)."""
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    musical_piece_id = Column(Integer, ForeignKey("musical_pieces.id"), nullable=True)
    questions = Column(JSON, nullable=False)  # List of question objects
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Quiz(id={self.id}, task_id={self.task_id})>"


class QuizResponse(Base):
    """Student response to a quiz."""
    __tablename__ = "quiz_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    answers = Column(JSON, nullable=False)  # List of answer objects
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<QuizResponse(id={self.id}, quiz_id={self.quiz_id}, student_id={self.student_id})>"
