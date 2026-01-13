from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User, UserRole
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskStatusUpdate, TaskResponse
from ..auth import get_current_user, require_teacher
from ..auth.permissions import check_user_access_to_student
from ..services.consistency import validate_student_exists

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    """
    Assign a task to a student. Teachers only.
    """
    # Validate student exists
    student = validate_student_exists(db, task_data.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if teacher has access to this student
    if not check_user_access_to_student(db, current_user, task_data.student_id):
        raise HTTPException(status_code=403, detail="Access forbidden: Not your student")
    
    # Create task
    task = Task(
        student_id=task_data.student_id,
        teacher_id=current_user.id,
        type=task_data.type,
        title=task_data.title,
        description=task_data.description,
        musical_piece_id=task_data.musical_piece_id,
        due_date=task_data.due_date
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    student_id: int = None,
    teacher_id: int = None,
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List tasks.
    - Teachers can see tasks they assigned
    - Students can see their own tasks
    - Admins can see all tasks
    """
    query = db.query(Task)
    
    if current_user.role == UserRole.TEACHER:
        query = query.filter(Task.teacher_id == current_user.id)
    elif current_user.role == UserRole.STUDENT:
        query = query.filter(Task.student_id == current_user.id)
    # Admin can see all
    
    # Apply filters
    if student_id is not None:
        if not check_user_access_to_student(db, current_user, student_id):
            raise HTTPException(status_code=403, detail="Access forbidden")
        query = query.filter(Task.student_id == student_id)
    
    if teacher_id is not None:
        query = query.filter(Task.teacher_id == teacher_id)
    
    if status_filter is not None:
        query = query.filter(Task.status == status_filter)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get task by ID.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check permissions
    if current_user.role == UserRole.STUDENT:
        if task.student_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access forbidden")
    elif current_user.role == UserRole.TEACHER:
        if task.teacher_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access forbidden")
    # Admin can see all
    
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    """
    Update task details. Teachers only.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check if teacher owns this task
    if task.teacher_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    # Update fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.musical_piece_id is not None:
        task.musical_piece_id = task_data.musical_piece_id
    if task_data.status is not None:
        task.status = task_data.status
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    
    db.commit()
    db.refresh(task)
    
    return task


@router.put("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update task status. Students can update their own tasks.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Students can only update their own tasks
    if current_user.role == UserRole.STUDENT and task.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    # Teachers can update tasks they assigned
    if current_user.role == UserRole.TEACHER and task.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    task.status = status_data.status
    db.commit()
    db.refresh(task)
    
    return task
