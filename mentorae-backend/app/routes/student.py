"""
Student-specific routes.
Protected routes accessible only to users with student role.
"""
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config import get_database
from app.dependencies import require_student

router = APIRouter(prefix="/student", tags=["Student"])


@router.get("/dashboard")
async def get_student_dashboard(
    current_user: dict = Depends(require_student),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get student dashboard data.
    
    Returns:
        - Student profile
        - Academic performance
        - Attendance
        - Upcoming assignments
    """
    return {
        "message": "Student dashboard",
        "user": {
            "id": current_user["_id"],
            "name": current_user["full_name"],
            "email": current_user["email"]
        },
        "stats": {
            "gpa": 3.8,
            "attendance": 95,
            "assignments_completed": 24,
            "achievements": 12
        }
    }


@router.get("/courses")
async def get_student_courses(
    current_user: dict = Depends(require_student),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get student's enrolled courses.
    """
    return {
        "message": "Student courses",
        "courses": [
            {"id": "1", "name": "Data Structures", "credits": 4},
            {"id": "2", "name": "Algorithms", "credits": 4},
            {"id": "3", "name": "Database Systems", "credits": 3}
        ]
    }


@router.get("/performance")
async def get_student_performance(
    current_user: dict = Depends(require_student),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get student's academic performance analytics.
    """
    return {
        "message": "Student performance",
        "performance": {
            "overall_gpa": 3.8,
            "semester_gpa": 3.9,
            "attendance_percentage": 95,
            "subjects": [
                {"name": "Mathematics", "score": 85, "grade": "A"},
                {"name": "Physics", "score": 78, "grade": "B+"},
                {"name": "Computer Science", "score": 95, "grade": "A+"}
            ]
        }
    }


@router.get("/assignments")
async def get_student_assignments(
    current_user: dict = Depends(require_student),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get student's assignments and submissions.
    """
    return {
        "message": "Student assignments",
        "assignments": [
            {
                "id": "1",
                "title": "Data Structures Project",
                "due_date": "2024-02-15",
                "status": "submitted",
                "grade": "A"
            },
            {
                "id": "2",
                "title": "Algorithm Analysis",
                "due_date": "2024-02-20",
                "status": "pending",
                "grade": None
            }
        ]
    }


@router.get("/ai-recommendations")
async def get_ai_recommendations(
    current_user: dict = Depends(require_student),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get AI-powered personalized recommendations for the student.
    """
    return {
        "message": "AI recommendations",
        "recommendations": [
            {
                "id": "1",
                "title": "Focus on Calculus",
                "description": "Your performance in calculus has dropped by 12%",
                "priority": "high",
                "action": "Review chapters 5-7"
            },
            {
                "id": "2",
                "title": "Great Progress in CS",
                "description": "You're excelling in Computer Science",
                "priority": "low",
                "action": "Keep up the excellent work"
            }
        ]
    }
