from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from datetime import datetime
import enum
from ..database import Base


class TaskType(str, enum.Enum):
    """Task type enumeration."""
    PRACTICE = "practice"
    LISTENING = "listening"


class TaskStatus(str, enum.Enum):
    """Task status enumeration."""
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(Base):
    """Task assigned to a student by a teacher."""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(SQLEnum(TaskType), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    musical_piece_id = Column(Integer, ForeignKey("musical_pieces.id"), nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.ASSIGNED, nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', type='{self.type}', status='{self.status}')>"
