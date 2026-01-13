"""Authentication and authorization modules."""

from .jwt import create_access_token, verify_password, get_password_hash
from .dependencies import get_current_user, get_current_active_user, require_role, require_admin, require_teacher, require_student
from .permissions import (
    check_teacher_student_relationship,
    check_user_access_to_student,
    check_user_access_to_teacher,
    get_teacher_student_ids,
    get_student_teacher_ids,
)

__all__ = [
    "create_access_token",
    "verify_password",
    "get_password_hash",
    "get_current_user",
    "get_current_active_user",
    "require_role",
    "require_admin",
    "require_teacher",
    "require_student",
    "check_teacher_student_relationship",
    "check_user_access_to_student",
    "check_user_access_to_teacher",
    "get_teacher_student_ids",
    "get_student_teacher_ids",
]
