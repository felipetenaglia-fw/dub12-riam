from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


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
