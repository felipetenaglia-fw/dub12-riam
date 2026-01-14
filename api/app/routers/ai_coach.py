from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Body
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models.user import User
from ..schemas.ai_coach import (
    AICoachAnalysisResponse,
    AICoachChatRequest,
    AICoachChatResponse
)
from ..services.bedrock import bedrock_service
from ..auth.dependencies import require_student

router = APIRouter(prefix="/ai-coach", tags=["AI Coach"])


@router.post("/analyze", response_model=AICoachAnalysisResponse)
async def analyze_performance(
    audio_file: UploadFile = File(..., description="Audio file of the performance (mp3, wav, m4a, ogg)"),
    piece_name: Optional[str] = Form(None, description="Name of the musical piece"),
    composer: Optional[str] = Form(None, description="Composer of the piece"),
    student_notes: Optional[str] = Form(None, description="Notes or context from the student"),
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Analyze a student's musical performance using AI.
    
    Upload an audio file and receive detailed feedback from an AI music coach
    based on the RIAM framework for developing great musicians.
    
    - **audio_file**: Audio recording of the performance (max 15MB)
    - **piece_name**: Optional name of the piece being performed
    - **composer**: Optional composer name
    - **student_notes**: Optional context or questions from the student
    """
    return await _process_audio_analysis(audio_file, piece_name, composer, student_notes)


@router.post("/analyze-public", response_model=AICoachAnalysisResponse)
async def analyze_performance_public(
    audio_file: UploadFile = File(..., description="Audio file of the performance (mp3, wav, m4a, ogg)"),
    piece_name: Optional[str] = Form(None, description="Name of the musical piece"),
    composer: Optional[str] = Form(None, description="Composer of the piece"),
    student_notes: Optional[str] = Form(None, description="Notes or context from the student")
):
    """
    Public endpoint for AI Coach analysis (no authentication required).
    
    Upload an audio file and receive detailed feedback from an AI music coach
    based on the RIAM framework for developing great musicians.
    
    - **audio_file**: Audio recording of the performance (max 15MB)
    - **piece_name**: Optional name of the piece being performed
    - **composer**: Optional composer name
    - **student_notes**: Optional context or questions from the student
    """
    return await _process_audio_analysis(audio_file, piece_name, composer, student_notes)


async def _process_audio_analysis(
    audio_file: UploadFile,
    piece_name: Optional[str],
    composer: Optional[str],
    student_notes: Optional[str]
) -> AICoachAnalysisResponse:
    """Shared logic for audio analysis processing."""
    # Validate file type
    allowed_extensions = ['mp3', 'wav', 'm4a', 'ogg']
    file_extension = audio_file.filename.split('.')[-1].lower() if audio_file.filename else ''
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Check file size (max 15MB)
    max_size = 15 * 1024 * 1024  # 15MB in bytes
    audio_data = await audio_file.read()
    
    if len(audio_data) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 15MB limit"
        )
    
    if len(audio_data) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Audio file is empty"
        )
    
    # Call Bedrock service to analyze
    try:
        result = bedrock_service.analyze_audio_performance(
            audio_data=audio_data,
            audio_format=file_extension,
            piece_name=piece_name,
            composer=composer,
            student_notes=student_notes
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to analyze audio. Please try again."
            )
        
        return AICoachAnalysisResponse(
            success=result.get("success", False),
            feedback=result.get("feedback"),
            audio_analysis=result.get("audio_analysis"),
            error=result.get("error"),
            model=result.get("model")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing performance: {str(e)}"
        )


@router.post("/chat", response_model=AICoachChatResponse)
async def chat_with_coach(
    request: AICoachChatRequest = Body(...),
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Chat with the AI Coach about your performance analysis.
    
    Ask follow-up questions about the feedback you received, request clarification,
    or get additional practice recommendations. The AI coach uses your previous
    analysis as context to provide personalized responses.
    
    - **question**: Your question about the performance or feedback
    - **analysis_context**: Previous analysis results (feedback and audio_analysis)
    - **conversation_history**: Previous messages in this conversation (optional)
    """
    return await _process_chat(request, student_name=current_user.name)


@router.post("/chat-public", response_model=AICoachChatResponse)
async def chat_with_coach_public(
    request: AICoachChatRequest = Body(...)
):
    """
    Public endpoint for AI Coach chat (no authentication required).
    
    Ask follow-up questions about the feedback you received, request clarification,
    or get additional practice recommendations.
    
    - **question**: Your question about the performance or feedback
    - **analysis_context**: Previous analysis results (feedback and audio_analysis)
    - **conversation_history**: Previous messages in this conversation (optional)
    """
    return await _process_chat(request, student_name=None)


async def _process_chat(request: AICoachChatRequest, student_name: Optional[str] = None) -> AICoachChatResponse:
    """Shared logic for chat processing."""
    if not request.question or not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty"
        )
    
    try:
        result = bedrock_service.chat_about_performance(
            question=request.question,
            analysis_context=request.analysis_context,
            conversation_history=request.conversation_history,
            student_name=student_name
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get response from AI coach. Please try again."
            )
        
        return AICoachChatResponse(
            success=result.get("success", False),
            response=result.get("response"),
            error=result.get("error"),
            model=result.get("model")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error chatting with AI coach: {str(e)}"
        )

