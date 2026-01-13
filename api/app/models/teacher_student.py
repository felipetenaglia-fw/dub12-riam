from sqlalchemy import Column, Integer, ForeignKey
from ..database import Base


class TeacherStudent(Base):
    """Many-to-many relationship between teachers and students."""
    __tablename__ = "teacher_students"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    def __repr__(self):
        return f"<TeacherStudent(teacher_id={self.teacher_id}, student_id={self.student_id})>"
