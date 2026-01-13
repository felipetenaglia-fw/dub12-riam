from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models.user import User, UserRole
from ..models.class_session import ClassSession
from ..models.task import Task, TaskStatus
from ..models.recording import Recording
from ..models.quiz import QuizResponse
from ..schemas.performance import StudentPerformanceSummary, TeacherPerformanceSummary, OverallPerformanceSummary
from ..auth import get_current_user, require_admin
from ..auth.permissions import check_user_access_to_student, check_user_access_to_teacher, get_teacher_student_ids

router = APIRouter(prefix="/performance", tags=["Performance"])


@router.get("/students/{student_id}", response_model=StudentPerformanceSummary)
def get_student_performance(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get performance summary for a specific student.
    Teachers can see their students. Admins can see all.
    """
    # Check permissions
    if not check_user_access_to_student(db, current_user, student_id):
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    # Get student
    student = db.query(User).filter(User.id == student_id, User.role == UserRole.STUDENT).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get metrics
    total_classes = db.query(func.count(ClassSession.id)).filter(ClassSession.student_id == student_id).scalar()
    total_tasks_assigned = db.query(func.count(Task.id)).filter(Task.student_id == student_id).scalar()
    total_tasks_completed = db.query(func.count(Task.id)).filter(
        Task.student_id == student_id,
        Task.status == TaskStatus.COMPLETED
    ).scalar()
    total_tasks_in_progress = db.query(func.count(Task.id)).filter(
        Task.student_id == student_id,
        Task.status == TaskStatus.IN_PROGRESS
    ).scalar()
    total_recordings = db.query(func.count(Recording.id)).filter(Recording.student_id == student_id).scalar()
    total_quizzes_completed = db.query(func.count(QuizResponse.id)).filter(QuizResponse.student_id == student_id).scalar()
    
    completion_rate = (total_tasks_completed / total_tasks_assigned * 100) if total_tasks_assigned > 0 else 0.0
    
    # Get recent classes
    recent_classes = db.query(ClassSession).filter(
        ClassSession.student_id == student_id
    ).order_by(ClassSession.date.desc()).limit(5).all()
    
    recent_classes_data = [
        {
            "id": c.id,
            "date": c.date.isoformat(),
            "notes": c.notes,
            "improvement_points": c.improvement_points
        }
        for c in recent_classes
    ]
    
    # Get recent tasks
    recent_tasks = db.query(Task).filter(
        Task.student_id == student_id
    ).order_by(Task.created_at.desc()).limit(5).all()
    
    recent_tasks_data = [
        {
            "id": t.id,
            "title": t.title,
            "type": t.type.value,
            "status": t.status.value,
            "due_date": t.due_date.isoformat() if t.due_date else None
        }
        for t in recent_tasks
    ]
    
    return StudentPerformanceSummary(
        student_id=student.id,
        student_name=student.name,
        total_classes=total_classes,
        total_tasks_assigned=total_tasks_assigned,
        total_tasks_completed=total_tasks_completed,
        total_tasks_in_progress=total_tasks_in_progress,
        total_recordings=total_recordings,
        total_quizzes_completed=total_quizzes_completed,
        completion_rate=round(completion_rate, 2),
        recent_classes=recent_classes_data,
        recent_tasks=recent_tasks_data
    )


@router.get("/teachers/{teacher_id}", response_model=TeacherPerformanceSummary)
def get_teacher_performance(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Get performance summary for a specific teacher. Admins only.
    """
    # Get teacher
    teacher = db.query(User).filter(User.id == teacher_id, User.role == UserRole.TEACHER).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Get student IDs
    student_ids = get_teacher_student_ids(db, teacher_id)
    
    # Get metrics
    total_classes_conducted = db.query(func.count(ClassSession.id)).filter(
        ClassSession.teacher_id == teacher_id
    ).scalar()
    total_tasks_assigned = db.query(func.count(Task.id)).filter(Task.teacher_id == teacher_id).scalar()
    
    # Get summary for each student
    students_summary = []
    for student_id in student_ids:
        try:
            summary = get_student_performance(student_id, db, current_user)
            students_summary.append(summary)
        except:
            pass
    
    return TeacherPerformanceSummary(
        teacher_id=teacher.id,
        teacher_name=teacher.name,
        total_students=len(student_ids),
        total_classes_conducted=total_classes_conducted,
        total_tasks_assigned=total_tasks_assigned,
        students_summary=students_summary
    )


@router.get("/overview", response_model=OverallPerformanceSummary)
def get_overall_performance(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Get overall performance summary. Admins only.
    """
    total_students = db.query(func.count(User.id)).filter(User.role == UserRole.STUDENT).scalar()
    total_teachers = db.query(func.count(User.id)).filter(User.role == UserRole.TEACHER).scalar()
    total_classes = db.query(func.count(ClassSession.id)).scalar()
    total_tasks = db.query(func.count(Task.id)).scalar()
    total_recordings = db.query(func.count(Recording.id)).scalar()
    total_quizzes = db.query(func.count(QuizResponse.id)).scalar()
    
    # Get all teachers
    teachers = db.query(User).filter(User.role == UserRole.TEACHER).all()
    teachers_summary = []
    
    for teacher in teachers:
        student_ids = get_teacher_student_ids(db, teacher.id)
        classes_conducted = db.query(func.count(ClassSession.id)).filter(
            ClassSession.teacher_id == teacher.id
        ).scalar()
        tasks_assigned = db.query(func.count(Task.id)).filter(Task.teacher_id == teacher.id).scalar()
        
        teachers_summary.append({
            "teacher_id": teacher.id,
            "teacher_name": teacher.name,
            "total_students": len(student_ids),
            "total_classes": classes_conducted,
            "total_tasks": tasks_assigned
        })
    
    return OverallPerformanceSummary(
        total_students=total_students,
        total_teachers=total_teachers,
        total_classes=total_classes,
        total_tasks=total_tasks,
        total_recordings=total_recordings,
        total_quizzes=total_quizzes,
        teachers_summary=teachers_summary
    )
