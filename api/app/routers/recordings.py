from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..models.user import User, UserRole
from ..models.recording import Recording
from ..schemas.recording import RecordingResponse, RecordingPresignedUrlResponse
from ..auth import get_current_user
from ..services.consistency import validate_task_exists
from ..services.s3 import s3_service

router = APIRouter(prefix="/recordings", tags=["Recordings"])


@router.post("/tasks/{task_id}/recordings", response_model=RecordingResponse, status_code=status.HTTP_201_CREATED)
def create_recording_entry(
    task_id: int,
    filename: str = Form(...),
    file_size: int = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a recording entry and get S3 presigned upload URL.
    Students can upload recordings for their own tasks.
    """
    # Validate task exists
    task = validate_task_exists(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Students can only upload for their own tasks
    if current_user.role == UserRole.STUDENT and task.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden: Not your task")
    
    # Generate S3 key
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    s3_key = f"recordings/{current_user.id}/{task_id}/{timestamp}_{filename}"
    
    # Generate S3 URL
    s3_url = s3_service.get_object_url(s3_key)
    
    # Create recording entry
    recording = Recording(
        task_id=task_id,
        student_id=current_user.id if current_user.role == UserRole.STUDENT else task.student_id,
        s3_key=s3_key,
        s3_url=s3_url,
        filename=filename,
        file_size=file_size
    )
    db.add(recording)
    db.commit()
    db.refresh(recording)
    
    return recording


@router.get("/tasks/{task_id}/recordings", response_model=List[RecordingResponse])
def list_task_recordings(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all recordings for a task.
    Students can see their own recordings. Teachers can see recordings for their students' tasks.
    """
    # Validate task exists
    task = validate_task_exists(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check permissions
    if current_user.role == UserRole.STUDENT and task.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    elif current_user.role == UserRole.TEACHER and task.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    recordings = db.query(Recording).filter(
        Recording.task_id == task_id
    ).order_by(Recording.created_at.desc()).all()
    
    return recordings


@router.get("/{recording_id}/url", response_model=RecordingPresignedUrlResponse)
def get_recording_presigned_url(
    recording_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get presigned download URL for a recording.
    """
    recording = db.query(Recording).filter(Recording.id == recording_id).first()
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    # Get task to check permissions
    task = validate_task_exists(db, recording.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Associated task not found")
    
    # Check permissions
    if current_user.role == UserRole.STUDENT and task.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    elif current_user.role == UserRole.TEACHER and task.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    # Generate presigned URL
    presigned_url = s3_service.generate_presigned_url(recording.s3_key, expiration=3600)
    if not presigned_url:
        raise HTTPException(status_code=500, detail="Failed to generate presigned URL")
    
    return {"url": presigned_url, "expires_in": 3600}


@router.get("/{recording_id}/upload-url")
def get_recording_upload_url(
    recording_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get presigned upload URL for a recording.
    """
    recording = db.query(Recording).filter(Recording.id == recording_id).first()
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    # Get task to check permissions
    task = validate_task_exists(db, recording.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Associated task not found")
    
    # Students can only get upload URLs for their own recordings
    if current_user.role == UserRole.STUDENT and recording.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    # Generate presigned upload URL
    presigned_post = s3_service.generate_presigned_upload_url(
        recording.s3_key,
        content_type="audio/mpeg",
        expiration=3600
    )
    if not presigned_post:
        raise HTTPException(status_code=500, detail="Failed to generate presigned upload URL")
    
    return presigned_post
