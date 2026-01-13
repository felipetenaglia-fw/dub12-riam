# RIAM LMS - Agent Development Guide

This document provides coding standards and operational guidelines for AI coding agents working in this repository.

## Project Overview

**RIAM Learning Management System** - A full-stack application for the Royal Irish Academy of Music with:
- **Backend API** (`api/`): FastAPI + SQLAlchemy + SQLite
- **Web UI** (`ui/`): Flask + HTMX + Alpine.js + Tailwind CSS  
- **Infrastructure** (`infra/`): AWS CDK for ECS deployment
- **Postman Collection** (`postman/`): API testing

## Quick Commands

### Development Servers
```bash
# Start both API and UI
./start.sh

# Or manually:
# Terminal 1 - API (port 8000)
cd api && uvicorn app.main:app --reload

# Terminal 2 - UI (port 5000)
cd ui && python app.py
```

### Testing
```bash
# Run all tests (API)
cd api && pytest

# Run specific test file
cd api && pytest tests/test_auth.py

# Run specific test
cd api && pytest tests/test_auth.py::test_login_success -v

# Run with coverage
cd api && pytest --cov=app --cov-report=html
```

### Code Quality
```bash
# Format code (if black is installed)
cd api && black app/

# Type checking (if mypy is installed)
cd api && mypy app/

# Lint (if flake8 is installed)
cd api && flake8 app/
```

### Database
```bash
# Reset database (delete and restart)
cd api && rm -f riam_lms.db && uvicorn app.main:app

# Database is auto-created and seeded on first startup
# Location: api/riam_lms.db
```

### AWS Deployment
```bash
cd infra
pip install -r requirements.txt
cdk bootstrap  # First time only
cdk deploy
cdk destroy    # Teardown
```

## Code Style Guidelines

### Python (API & UI)

#### Import Order
Follow this strict order with blank lines between groups:
```python
# 1. Standard library
import os
from datetime import datetime
from typing import Optional, List

# 2. Third-party packages
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

# 3. Local application imports
from ..database import get_db
from ..models.user import User
from ..schemas.user import UserResponse
from ..auth import get_current_user
```

#### Naming Conventions
- **Classes**: `PascalCase` - `UserRole`, `ClassSession`, `StudentFeedback`
- **Functions/Methods**: `snake_case` - `get_current_user`, `create_access_token`
- **Variables**: `snake_case` - `access_token`, `user_data`, `task_id`
- **Constants**: `UPPER_SNAKE_CASE` - `API_BASE_URL`, `JWT_SECRET_KEY`
- **Private**: Prefix with `_` - `_load_backend_mixin`, `_execute_internal`
- **Enums**: Class in `PascalCase`, values in `UPPER_CASE`
  ```python
  class UserRole(str, enum.Enum):
      STUDENT = "student"
      TEACHER = "teacher"
      ADMIN = "admin"
  ```

#### Type Hints
Always use type hints for function signatures:
```python
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    """Get user by ID."""
    pass

async def fetch_data(url: str) -> Optional[dict]:
    """Fetch data from URL."""
    pass
```

#### Docstrings
Use concise docstrings for all public functions/classes:
```python
def create_task(task_data: TaskCreate, db: Session) -> Task:
    """
    Create a new task assignment.
    
    Args:
        task_data: Task creation data
        db: Database session
        
    Returns:
        Created task instance
    """
```

#### Error Handling
- Use FastAPI's `HTTPException` with appropriate status codes
- Include descriptive error messages for API responses
- Always specify `status_code` and `detail`
```python
if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
```

#### Database Patterns
- **No physical foreign keys** - Consistency enforced in application code
- Use validation helpers from `services.consistency` module
- Always check relationships exist before operations
```python
# Import validation helpers
from ..services.consistency import validate_student_exists

# Validate before operations
student = validate_student_exists(db, student_id)
if not student:
    raise HTTPException(status_code=404, detail="Student not found")
```

#### Router Structure
- One router per resource in `app/routers/`
- Use `APIRouter` with `prefix` and `tags`
- Group related endpoints together
```python
router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(...):
    pass

@router.get("", response_model=List[TaskResponse])
def list_tasks(...):
    pass
```

#### Authentication & Authorization
- JWT tokens stored in session (UI) or Authorization header (API)
- Role-based access via dependencies: `require_admin`, `require_teacher`, `require_student`
- Check permissions explicitly for cross-role access
```python
from ..auth import get_current_user, require_teacher
from ..auth.permissions import check_user_access_to_student

@router.post("/classes")
def create_class(
    data: ClassSessionCreate,
    current_user: User = Depends(require_teacher)
):
    if not check_user_access_to_student(db, current_user, data.student_id):
        raise HTTPException(status_code=403, detail="Access forbidden")
```

### HTML/Templates (UI)

#### Template Structure
- Use Jinja2 inheritance with `base.html`
- Keep logic minimal in templates
- Use Alpine.js for reactivity, HTMX for server interactions
```html
{% extends "base.html" %}
{% block content %}
<div x-data="dashboard()" x-init="init()">
    <!-- Content -->
</div>
{% endblock %}
```

#### Styling
- Use Tailwind CSS utility classes
- Maintain responsive design (`md:`, `lg:` breakpoints)
- Keep colors consistent with theme (indigo-600, gray-50, etc.)

## Project-Specific Rules

### Data Consistency
- **Foreign keys disabled** at database level (PRAGMA foreign_keys=OFF)
- **Always validate** user/task/session existence before operations
- Use `services.consistency` module validators

### Role-Based Logic
Three roles with distinct permissions:
- **Admin**: Full system access, view all users/stats
- **Teacher**: Manage own students, assign tasks, write notes
- **Student**: View own tasks/classes, submit feedback

### Database Lifecycle
- SQLite file-based: `api/riam_lms.db`
- Auto-initialized on startup via `lifespan` context manager
- Seeded with mock data (6 users, classes, tasks, pieces)
- To reset: delete `riam_lms.db` and restart

### API Response Models
- Always define Pydantic schemas for requests/responses
- Use `response_model` parameter in route decorators
- Include `Config` with `from_attributes = True` for ORM models

### S3 Integration
- Recordings use presigned URLs (both upload and download)
- S3 service in `app/services/s3.py`
- Keys format: `recordings/{user_id}/{task_id}/{timestamp}_{filename}`

### Mock Credentials
Pre-seeded users for testing:
```
admin/admin - RIAM Administrator
teacher/teacher - Dr. Sarah Murphy
student/student - Emma Walsh
```

## Common Patterns

### Adding a New Endpoint
1. Create/update model in `app/models/`
2. Define Pydantic schemas in `app/schemas/`
3. Create router in `app/routers/`
4. Register router in `app/main.py`
5. Add to Postman collection
6. Update UI if needed

### Adding New Role Permission
1. Update check in `app/auth/permissions.py`
2. Create dependency in `app/auth/dependencies.py`
3. Apply to router with `Depends(require_xxx)`

## Testing Guidelines

### Test Structure
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/auth/login", json={
        "username": "admin",
        "password": "admin"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Test Database
Tests should use a separate test database or in-memory SQLite.

## Critical Reminders

⚠️ **Never commit**:
- `api/riam_lms.db` - Database file
- `.env` files - Secrets
- `__pycache__/` - Python cache
- AWS credentials

✅ **Always**:
- Validate user/relationship existence before operations
- Use type hints and docstrings
- Follow import order convention
- Check role permissions explicitly
- Test with all three roles (admin/teacher/student)

## Architecture Notes

```
Browser → Flask UI (port 5000) → FastAPI API (port 8000) → SQLite DB
                                        ↓
                                   AWS S3 (recordings)
```

- **Stateless API**: JWT tokens for authentication
- **Session-based UI**: Flask sessions with JWT stored
- **No caching**: Direct database queries
- **CORS enabled**: Open for development (restrict in production)

---

*This guide is for AI coding agents. Keep it updated as patterns evolve.*
