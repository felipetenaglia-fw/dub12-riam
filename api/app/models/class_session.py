from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from ..database import Base


class ClassSession(Base):
    """Class session with teacher notes."""
    __tablename__ = "class_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(Text, nullable=True)
    improvement_points = Column(Text, nullable=True)
    actions = Column(Text, nullable=True)  # Actions for student to practice
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ClassSession(id={self.id}, teacher_id={self.teacher_id}, student_id={self.student_id})>"
