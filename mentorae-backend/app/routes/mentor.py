"""
Mentor-specific routes.
Protected routes accessible only to users with mentor role.
"""
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config import get_database
from app.dependencies import require_mentor

router = APIRouter(prefix="/mentor", tags=["Mentor"])


@router.get("/dashboard")
async def get_mentor_dashboard(
    current_user: dict = Depends(require_mentor),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get mentor dashboard data.
    
    Returns:
        - Assigned students
        - Performance overview
        - Risk alerts
    """
    return {
        "message": "Mentor dashboard",
        "user": {
            "id": current_user["_id"],
            "name": current_user["full_name"],
            "email": current_user["email"]
        },
        "stats": {
            "total_students": 15,
            "at_risk_students": 3,
            "average_gpa": 3.5,
            "sessions_this_month": 24
        }
    }


@router.get("/students")
async def get_mentor_students(
    current_user: dict = Depends(require_mentor),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get list of students assigned to this mentor.
    """
    return {
        "message": "Mentor students",
        "students": [
            {
                "id": "1",
                "name": "Alice Johnson",
                "gpa": 3.8,
                "attendance": 95,
                "risk_level": "low"
            },
            {
                "id": "2",
                "name": "Bob Smith",
                "gpa": 2.9,
                "attendance": 78,
                "risk_level": "high"
            },
            {
                "id": "3",
                "name": "Carol Williams",
                "gpa": 3.5,
                "attendance": 88,
                "risk_level": "medium"
            }
        ]
    }


@router.get("/students/{student_id}")
async def get_student_details(
    student_id: str,
    current_user: dict = Depends(require_mentor),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get detailed information about a specific student.
    """
    return {
        "message": "Student details",
        "student": {
            "id": student_id,
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "gpa": 3.8,
            "attendance": 95,
            "risk_level": "low",
            "performance_trend": "improving",
            "recent_activities": [
                {"date": "2024-02-10", "activity": "Submitted assignment"},
                {"date": "2024-02-08", "activity": "Attended mentoring session"}
            ]
        }
    }


@router.get("/analytics")
async def get_mentor_analytics(
    current_user: dict = Depends(require_mentor),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get analytics for mentor's students.
    """
    return {
        "message": "Mentor analytics",
        "analytics": {
            "average_gpa": 3.5,
            "average_attendance": 88,
            "improvement_rate": 15,
            "at_risk_count": 3,
            "performance_distribution": {
                "excellent": 5,
                "good": 7,
                "average": 2,
                "poor": 1
            }
        }
    }


@router.post("/sessions")
async def create_mentoring_session(
    current_user: dict = Depends(require_mentor),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Create a new mentoring session.
    """
    return {
        "message": "Mentoring session created",
        "session": {
            "id": "session_123",
            "mentor_id": current_user["_id"],
            "date": "2024-02-15",
            "status": "scheduled"
        }
    }
