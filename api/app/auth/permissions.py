from typing import Optional
from sqlalchemy.orm import Session
from ..models.user import User, UserRole
from ..models.teacher_student import TeacherStudent


def check_teacher_student_relationship(db: Session, teacher_id: int, student_id: int) -> bool:
    """Check if a teacher-student relationship exists."""
    relationship = db.query(TeacherStudent).filter(
        TeacherStudent.teacher_id == teacher_id,
        TeacherStudent.student_id == student_id
    ).first()
    return relationship is not None


def check_user_access_to_student(db: Session, user: User, student_id: int) -> bool:
    """
    Check if a user has access to a student's data.
    - Admins have access to all students
    - Teachers have access to their own students
    - Students have access to their own data
    """
    if user.role == UserRole.ADMIN:
        return True
    
    if user.role == UserRole.TEACHER:
        return check_teacher_student_relationship(db, user.id, student_id)
    
    if user.role == UserRole.STUDENT:
        return user.id == student_id
    
    return False


def check_user_access_to_teacher(db: Session, user: User, teacher_id: int) -> bool:
    """
    Check if a user has access to a teacher's data.
    - Admins have access to all teachers
    - Teachers have access to their own data
    """
    if user.role == UserRole.ADMIN:
        return True
    
    if user.role == UserRole.TEACHER:
        return user.id == teacher_id
    
    return False


def get_teacher_student_ids(db: Session, teacher_id: int) -> list[int]:
    """Get all student IDs for a given teacher."""
    relationships = db.query(TeacherStudent).filter(
        TeacherStudent.teacher_id == teacher_id
    ).all()
    return [rel.student_id for rel in relationships]


def get_student_teacher_ids(db: Session, student_id: int) -> list[int]:
    """Get all teacher IDs for a given student."""
    relationships = db.query(TeacherStudent).filter(
        TeacherStudent.student_id == student_id
    ).all()
    return [rel.teacher_id for rel in relationships]
