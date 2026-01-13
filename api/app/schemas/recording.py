from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RecordingResponse(BaseModel):
    """Schema for recording response."""
    id: int
    task_id: int
    student_id: int
    s3_key: str
    s3_url: str
    filename: str
    file_size: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class RecordingUploadResponse(BaseModel):
    """Schema for upload response."""
    recording_id: int
    upload_url: str
    message: str


class RecordingPresignedUrlResponse(BaseModel):
    """Schema for presigned URL response."""
    url: str
    expires_in: int
