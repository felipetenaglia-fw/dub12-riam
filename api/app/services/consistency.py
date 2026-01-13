"""Service helper for ensuring data consistency without foreign key enforcement."""

from sqlalchemy.orm import Session
from typing import Optional
from ..models.user import User, UserRole
from ..models.teacher_student import TeacherStudent
from ..models.task import Task
from ..models.class_session import ClassSession


def validate_user_exists(db: Session, user_id: int) -> Optional[User]:
    """Validate that a user exists."""
    return db.query(User).filter(User.id == user_id).first()


def validate_teacher_exists(db: Session, teacher_id: int) -> Optional[User]:
    """Validate that a teacher exists."""
    teacher = db.query(User).filter(
        User.id == teacher_id,
        User.role == UserRole.TEACHER
    ).first()
    return teacher


def validate_student_exists(db: Session, student_id: int) -> Optional[User]:
    """Validate that a student exists."""
    student = db.query(User).filter(
        User.id == student_id,
        User.role == UserRole.STUDENT
    ).first()
    return student


def validate_teacher_student_relationship(db: Session, teacher_id: int, student_id: int) -> bool:
    """Validate that a teacher-student relationship exists."""
    relationship = db.query(TeacherStudent).filter(
        TeacherStudent.teacher_id == teacher_id,
        TeacherStudent.student_id == student_id
    ).first()
    return relationship is not None


def validate_task_exists(db: Session, task_id: int) -> Optional[Task]:
    """Validate that a task exists."""
    return db.query(Task).filter(Task.id == task_id).first()


def validate_class_session_exists(db: Session, class_id: int) -> Optional[ClassSession]:
    """Validate that a class session exists."""
    return db.query(ClassSession).filter(ClassSession.id == class_id).first()


def cleanup_orphaned_records(db: Session):
    """
    Clean up orphaned records that reference non-existent users.
    This is useful for maintaining consistency without FK constraints.
    """
    # This could be run periodically or on-demand
    # For now, we'll rely on application-level validation
    pass
