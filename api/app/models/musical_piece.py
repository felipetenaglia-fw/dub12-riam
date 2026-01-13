from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from ..database import Base


class MusicalPiece(Base):
    """Musical piece from a composer."""
    __tablename__ = "musical_pieces"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    composer = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    audio_url = Column(String, nullable=True)  # URL to audio file
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<MusicalPiece(id={self.id}, title='{self.title}', composer='{self.composer}')>"
