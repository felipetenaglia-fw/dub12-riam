from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User, UserRole
from ..models.quiz import Quiz, QuizResponse
from ..schemas.quiz import QuizCreate, QuizResponse as QuizResponseSchema, QuizResponseCreate, QuizResponseData
from ..auth import get_current_user, require_teacher
from ..services.consistency import validate_task_exists

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


@router.post("", response_model=QuizResponseSchema, status_code=status.HTTP_201_CREATED)
def create_quiz(
    quiz_data: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    """
    Create a quiz attached to a task. Teachers only.
    """
    # Validate task exists
    task = validate_task_exists(db, quiz_data.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check if teacher owns the task
    if task.teacher_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Access forbidden: Not your task")
    
    # Convert questions to dict format
    questions_dict = [q.model_dump() for q in quiz_data.questions]
    
    # Create quiz
    quiz = Quiz(
        task_id=quiz_data.task_id,
        musical_piece_id=quiz_data.musical_piece_id,
        questions=questions_dict
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    
    return quiz


@router.get("/{quiz_id}", response_model=QuizResponseSchema)
def get_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get quiz by ID.
    Students can see quizzes for their assigned tasks. Teachers can see their quizzes.
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Get associated task
    task = validate_task_exists(db, quiz.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Associated task not found")
    
    # Check permissions
    if current_user.role == UserRole.STUDENT and task.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    elif current_user.role == UserRole.TEACHER and task.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    return quiz


@router.post("/{quiz_id}/responses", response_model=QuizResponseData, status_code=status.HTTP_201_CREATED)
def submit_quiz_response(
    quiz_id: int,
    response_data: QuizResponseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit quiz response. Students only.
    """
    # Validate quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Get associated task
    task = validate_task_exists(db, quiz.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Associated task not found")
    
    # Students can only submit for their assigned tasks
    if current_user.role == UserRole.STUDENT and task.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden: Not your quiz")
    
    # Convert answers to dict format
    answers_dict = [a.model_dump() for a in response_data.answers]
    
    # Create quiz response
    quiz_response = QuizResponse(
        quiz_id=quiz_id,
        student_id=current_user.id if current_user.role == UserRole.STUDENT else task.student_id,
        answers=answers_dict
    )
    db.add(quiz_response)
    db.commit()
    db.refresh(quiz_response)
    
    return quiz_response


@router.get("/{quiz_id}/responses", response_model=List[QuizResponseData])
def get_quiz_responses(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all responses for a quiz. Teachers can see responses for their quizzes.
    """
    # Validate quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Get associated task
    task = validate_task_exists(db, quiz.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Associated task not found")
    
    # Check permissions
    if current_user.role == UserRole.TEACHER and task.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    elif current_user.role == UserRole.STUDENT and task.student_id != current_user.id:
        # Students can only see their own responses
        responses = db.query(QuizResponse).filter(
            QuizResponse.quiz_id == quiz_id,
            QuizResponse.student_id == current_user.id
        ).all()
        return responses
    
    # Teachers and admins can see all responses
    responses = db.query(QuizResponse).filter(
        QuizResponse.quiz_id == quiz_id
    ).order_by(QuizResponse.submitted_at.desc()).all()
    
    return responses
