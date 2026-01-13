from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class StudentPerformanceSummary(BaseModel):
    """Schema for student performance summary."""
    student_id: int
    student_name: str
    total_classes: int
    total_tasks_assigned: int
    total_tasks_completed: int
    total_tasks_in_progress: int
    total_recordings: int
    total_quizzes_completed: int
    completion_rate: float
    recent_classes: List[Dict[str, Any]]
    recent_tasks: List[Dict[str, Any]]


class TeacherPerformanceSummary(BaseModel):
    """Schema for teacher performance summary."""
    teacher_id: int
    teacher_name: str
    total_students: int
    total_classes_conducted: int
    total_tasks_assigned: int
    students_summary: List[StudentPerformanceSummary]


class OverallPerformanceSummary(BaseModel):
    """Schema for overall performance summary (admin view)."""
    total_students: int
    total_teachers: int
    total_classes: int
    total_tasks: int
    total_recordings: int
    total_quizzes: int
    teachers_summary: List[Dict[str, Any]]
