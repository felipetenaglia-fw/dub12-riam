"""Pydantic schemas for request/response validation."""

from .user import UserCreate, UserUpdate, UserResponse, UserLogin, Token, TokenData
from .class_session import ClassSessionCreate, ClassSessionUpdate, ClassSessionResponse
from .task import TaskCreate, TaskUpdate, TaskStatusUpdate, TaskResponse
from .musical_piece import MusicalPieceCreate, MusicalPieceUpdate, MusicalPieceResponse
from .feedback import FeedbackCreate, FeedbackResponse
from .recording import RecordingResponse, RecordingUploadResponse, RecordingPresignedUrlResponse
from .quiz import QuizCreate, QuizResponse, QuizResponseCreate, QuizResponseData, QuizQuestion, QuizAnswer
from .performance import StudentPerformanceSummary, TeacherPerformanceSummary, OverallPerformanceSummary

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenData",
    "ClassSessionCreate",
    "ClassSessionUpdate",
    "ClassSessionResponse",
    "TaskCreate",
    "TaskUpdate",
    "TaskStatusUpdate",
    "TaskResponse",
    "MusicalPieceCreate",
    "MusicalPieceUpdate",
    "MusicalPieceResponse",
    "FeedbackCreate",
    "FeedbackResponse",
    "RecordingResponse",
    "RecordingUploadResponse",
    "RecordingPresignedUrlResponse",
    "QuizCreate",
    "QuizResponse",
    "QuizResponseCreate",
    "QuizResponseData",
    "QuizQuestion",
    "QuizAnswer",
    "StudentPerformanceSummary",
    "TeacherPerformanceSummary",
    "OverallPerformanceSummary",
]
