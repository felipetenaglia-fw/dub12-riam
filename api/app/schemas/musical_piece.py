from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MusicalPieceBase(BaseModel):
    """Base musical piece schema."""
    title: str
    composer: str
    description: Optional[str] = None
    audio_url: Optional[str] = None


class MusicalPieceCreate(MusicalPieceBase):
    """Schema for creating a musical piece."""
    pass


class MusicalPieceUpdate(BaseModel):
    """Schema for updating a musical piece."""
    title: Optional[str] = None
    composer: Optional[str] = None
    description: Optional[str] = None
    audio_url: Optional[str] = None


class MusicalPieceResponse(MusicalPieceBase):
    """Schema for musical piece response."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
