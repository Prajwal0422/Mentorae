"""
AI Mentor API routes.
Provides endpoints for AI-powered academic mentoring.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, Field
from typing import List, Optional

from app.config import get_database
from app.dependencies import get_current_active_user
from app.ai.mentor_service import MentorService

router = APIRouter(prefix="/ai", tags=["AI Mentor"])


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat request model."""
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Can you explain the concept of recursion in programming?",
                "conversation_id": "conv_123"
            }
        }


class ChatResponse(BaseModel):
    """Chat response model."""
    success: bool
    response: Optional[str] = None
    timestamp: Optional[str] = None
    error: Optional[str] = None


class StudyPlanRequest(BaseModel):
    """Study plan request model."""
    duration_days: int = Field(..., ge=1, le=90)
    subjects: List[str] = Field(..., min_items=1, max_items=10)
    focus_areas: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "duration_days": 7,
                "subjects": ["Data Structures", "Algorithms", "Database Systems"],
                "focus_areas": ["Trees", "Sorting", "SQL Queries"]
            }
        }


class StudyPlanResponse(BaseModel):
    """Study plan response model."""
    success: bool
    plan_id: Optional[str] = None
    study_plan: Optional[str] = None
    duration_days: Optional[int] = None
    subjects: Optional[List[str]] = None
    error: Optional[str] = None


class RecommendationsRequest(BaseModel):
    """Recommendations request model."""
    include_performance: bool = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "include_performance": True
            }
        }


class RecommendationsResponse(BaseModel):
    """Recommendations response model."""
    success: bool
    recommendation_id: Optional[str] = None
    recommendations: Optional[str] = None
    error: Optional[str] = None


# Endpoints
@router.post("/chat", response_model=ChatResponse)
async def chat_with_mentor(
    request: ChatRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Chat with AI Mentor.
    
    Send a message to the AI mentor and get personalized academic guidance.
    The AI considers your academic context (CGPA, attendance, weak subjects) 
    when providing responses.
    
    - **message**: Your question or message (1-2000 characters)
    - **conversation_id**: Optional ID to maintain conversation context
    """
    mentor_service = MentorService(db)
    
    result = await mentor_service.chat(
        user_id=current_user["_id"],
        message=request.message,
        conversation_id=request.conversation_id
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to generate response")
        )
    
    return result


@router.post("/study-plan", response_model=StudyPlanResponse)
async def generate_study_plan(
    request: StudyPlanRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Generate Personalized Study Plan.
    
    Create a detailed, day-by-day study plan tailored to your academic profile.
    The plan considers your weak subjects, CGPA, and current semester.
    
    - **duration_days**: Plan duration (1-90 days)
    - **subjects**: List of subjects to include (1-10 subjects)
    - **focus_areas**: Optional specific topics to emphasize
    """
    mentor_service = MentorService(db)
    
    result = await mentor_service.generate_study_plan(
        user_id=current_user["_id"],
        duration_days=request.duration_days,
        subjects=request.subjects,
        focus_areas=request.focus_areas
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to generate study plan")
        )
    
    return result


@router.post("/recommendations", response_model=RecommendationsResponse)
async def get_recommendations(
    request: RecommendationsRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get Personalized Recommendations.
    
    Receive AI-powered recommendations for improving your academic performance.
    Includes study strategies, resource suggestions, and improvement plans.
    
    - **include_performance**: Include recent performance data in analysis
    """
    mentor_service = MentorService(db)
    
    # TODO: Fetch actual performance data if requested
    performance_data = None
    if request.include_performance:
        performance_data = {
            "recent_scores": "Not available",
            "assignment_completion": 85,
            "trend": "improving"
        }
    
    result = await mentor_service.get_recommendations(
        user_id=current_user["_id"],
        performance_data=performance_data
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to generate recommendations")
        )
    
    return result


@router.get("/history")
async def get_chat_history(
    limit: int = 50,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get Chat History.
    
    Retrieve your previous conversations with the AI mentor.
    
    - **limit**: Maximum number of messages to retrieve (default: 50)
    """
    mentor_service = MentorService(db)
    
    history = await mentor_service.get_chat_history(
        user_id=current_user["_id"],
        limit=limit
    )
    
    return {
        "success": True,
        "count": len(history),
        "history": history
    }


@router.get("/status")
async def get_ai_status():
    """
    Check AI Service Status.
    
    Verify if the AI mentor service is available and operational.
    """
    from app.ai.gemini_client import gemini_client
    
    return {
        "status": "operational" if gemini_client.is_available() else "unavailable",
        "service": "Gemini AI",
        "features": [
            "Academic Chat",
            "Study Plan Generation",
            "Personalized Recommendations"
        ]
    }
