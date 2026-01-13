from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User, UserRole
from ..models.class_session import ClassSession
from ..schemas.class_session import ClassSessionCreate, ClassSessionUpdate, ClassSessionResponse
from ..auth import get_current_user, require_teacher
from ..auth.permissions import check_user_access_to_student
from ..services.consistency import validate_student_exists

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.post("", response_model=ClassSessionResponse, status_code=status.HTTP_201_CREATED)
def create_class_session(
    session_data: ClassSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    """
    Create a new class session with notes. Teachers only.
    """
    # Validate student exists
    student = validate_student_exists(db, session_data.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if teacher has access to this student
    if not check_user_access_to_student(db, current_user, session_data.student_id):
        raise HTTPException(status_code=403, detail="Access forbidden: Not your student")
    
    # Create class session
    class_session = ClassSession(
        teacher_id=current_user.id,
        student_id=session_data.student_id,
        date=session_data.date,
        notes=session_data.notes,
        improvement_points=session_data.improvement_points,
        actions=session_data.actions
    )
    db.add(class_session)
    db.commit()
    db.refresh(class_session)
    
    return class_session


@router.get("", response_model=List[ClassSessionResponse])
def list_class_sessions(
    student_id: int = None,
    teacher_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List class sessions.
    - Teachers can see their own sessions
    - Students can see their own sessions
    - Admins can see all sessions
    """
    query = db.query(ClassSession)
    
    if current_user.role == UserRole.TEACHER:
        query = query.filter(ClassSession.teacher_id == current_user.id)
    elif current_user.role == UserRole.STUDENT:
        query = query.filter(ClassSession.student_id == current_user.id)
    # Admin can see all
    
    # Apply filters
    if student_id is not None:
        # Check permissions
        if not check_user_access_to_student(db, current_user, student_id):
            raise HTTPException(status_code=403, detail="Access forbidden")
        query = query.filter(ClassSession.student_id == student_id)
    
    if teacher_id is not None:
        query = query.filter(ClassSession.teacher_id == teacher_id)
    
    sessions = query.order_by(ClassSession.date.desc()).all()
    return sessions


@router.get("/{class_id}", response_model=ClassSessionResponse)
def get_class_session(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get class session by ID.
    """
    class_session = db.query(ClassSession).filter(ClassSession.id == class_id).first()
    if not class_session:
        raise HTTPException(status_code=404, detail="Class session not found")
    
    # Check permissions
    if current_user.role == UserRole.STUDENT:
        if class_session.student_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access forbidden")
    elif current_user.role == UserRole.TEACHER:
        if class_session.teacher_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access forbidden")
    # Admin can see all
    
    return class_session


@router.put("/{class_id}", response_model=ClassSessionResponse)
def update_class_session(
    class_id: int,
    session_data: ClassSessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    """
    Update class session notes. Teachers only.
    """
    class_session = db.query(ClassSession).filter(ClassSession.id == class_id).first()
    if not class_session:
        raise HTTPException(status_code=404, detail="Class session not found")
    
    # Check if teacher owns this session
    if class_session.teacher_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    # Update fields
    if session_data.notes is not None:
        class_session.notes = session_data.notes
    if session_data.improvement_points is not None:
        class_session.improvement_points = session_data.improvement_points
    if session_data.actions is not None:
        class_session.actions = session_data.actions
    
    db.commit()
    db.refresh(class_session)
    
    return class_session


@router.get("/students/{student_id}/history", response_model=List[ClassSessionResponse])
def get_student_class_history(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get class history for a specific student.
    """
    # Check permissions
    if not check_user_access_to_student(db, current_user, student_id):
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    sessions = db.query(ClassSession).filter(
        ClassSession.student_id == student_id
    ).order_by(ClassSession.date.desc()).all()
    
    return sessions
