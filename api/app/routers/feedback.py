from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User, UserRole
from ..models.feedback import StudentFeedback
from ..schemas.feedback import FeedbackCreate, FeedbackResponse
from ..auth import get_current_user
from ..services.consistency import validate_task_exists

router = APIRouter(prefix="/tasks", tags=["Feedback"])


@router.post("/{task_id}/feedback", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(
    task_id: int,
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit feedback for a task. Students submit for their own tasks.
    """
    # Validate task exists
    task = validate_task_exists(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Students can only submit feedback for their own tasks
    if current_user.role == UserRole.STUDENT and task.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden: Not your task")
    
    # Create feedback
    feedback = StudentFeedback(
        task_id=task_id,
        student_id=current_user.id if current_user.role == UserRole.STUDENT else task.student_id,
        content=feedback_data.content,
        feeling=feedback_data.feeling
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    return feedback


@router.get("/{task_id}/feedback", response_model=List[FeedbackResponse])
def get_task_feedback(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all feedback for a task.
    Students can see their own feedback. Teachers can see feedback for their students' tasks.
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
    
    feedback_list = db.query(StudentFeedback).filter(
        StudentFeedback.task_id == task_id
    ).order_by(StudentFeedback.created_at.desc()).all()
    
    return feedback_list
