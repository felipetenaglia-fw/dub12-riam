from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class AICoachAnalysisRequest(BaseModel):
    """Request schema for AI coach analysis."""
    piece_name: Optional[str] = Field(None, description="Name of the musical piece")
    composer: Optional[str] = Field(None, description="Composer of the piece")
    student_notes: Optional[str] = Field(None, description="Notes or context from the student")
    
    class Config:
        from_attributes = True


class AICoachAnalysisResponse(BaseModel):
    """Response schema for AI coach analysis."""
    success: bool = Field(..., description="Whether the analysis was successful")
    feedback: Optional[str] = Field(None, description="Detailed feedback from the AI coach")
    audio_analysis: Optional[Dict[str, Any]] = Field(None, description="Extracted audio features and metrics")
    error: Optional[str] = Field(None, description="Error message if analysis failed")
    model: Optional[str] = Field(None, description="AI model used for analysis")
    
    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    """Single chat message."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class AICoachChatRequest(BaseModel):
    """Request schema for AI coach chat conversation."""
    question: str = Field(..., description="Student's question about their performance")
    analysis_context: Optional[Dict[str, Any]] = Field(
        None,
        description="Previous analysis context (feedback and audio_analysis from AICoachAnalysisResponse)"
    )
    conversation_history: Optional[List[ChatMessage]] = Field(
        default_factory=list,
        description="Previous messages in the conversation"
    )
    
    class Config:
        from_attributes = True


class AICoachChatResponse(BaseModel):
    """Response schema for AI coach chat."""
    success: bool = Field(..., description="Whether the chat was successful")
    response: Optional[str] = Field(None, description="AI coach's response to the question")
    error: Optional[str] = Field(None, description="Error message if chat failed")
    model: Optional[str] = Field(None, description="AI model used for the response")
    
    class Config:
        from_attributes = True
