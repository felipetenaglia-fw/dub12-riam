from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime
from ..database import Base


class StudentFeedback(Base):
    """Student feedback for a task."""
    __tablename__ = "student_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)  # Feedback content
    feeling = Column(Text, nullable=True)  # How they felt during practice
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<StudentFeedback(id={self.id}, task_id={self.task_id}, student_id={self.student_id})>"
