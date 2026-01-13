from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from ..database import Base


class Recording(Base):
    """Practice recording uploaded by student."""
    __tablename__ = "recordings"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    s3_key = Column(String, nullable=False)  # S3 object key
    s3_url = Column(String, nullable=False)  # Full S3 URL
    filename = Column(String, nullable=False)  # Original filename
    file_size = Column(Integer, nullable=True)  # File size in bytes
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Recording(id={self.id}, task_id={self.task_id}, filename='{self.filename}')>"
