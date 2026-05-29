"""
Admin-specific routes.
Protected routes accessible only to users with admin role.
"""
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config import get_database
from app.dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
async def get_admin_dashboard(
    current_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get admin dashboard with system-wide statistics.
    """
    return {
        "message": "Admin dashboard",
        "stats": {
            "total_users": 2450,
            "active_students": 1850,
            "active_mentors": 145,
            "total_courses": 85,
            "system_health": "excellent"
        }
    }


@router.get("/users")
async def get_all_users(
    current_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get list of all users in the system.
    """
    users_collection = db.users
    users = await users_collection.find({}, {"hashed_password": 0}).to_list(100)
    
    # Convert ObjectId to string
    for user in users:
        user["_id"] = str(user["_id"])
    
    return {
        "message": "All users",
        "count": len(users),
        "users": users
    }


@router.get("/users/{user_id}")
async def get_user_by_id(
    user_id: str,
    current_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get detailed information about a specific user.
    """
    from bson import ObjectId
    
    users_collection = db.users
    user = await users_collection.find_one(
        {"_id": ObjectId(user_id)},
        {"hashed_password": 0}
    )
    
    if user:
        user["_id"] = str(user["_id"])
        return {"message": "User details", "user": user}
    
    return {"message": "User not found"}


@router.put("/users/{user_id}/activate")
async def activate_user(
    user_id: str,
    current_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Activate a user account.
    """
    from bson import ObjectId
    from datetime import datetime
    
    users_collection = db.users
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_active": True, "updated_at": datetime.utcnow()}}
    )
    
    if result.modified_count > 0:
        return {"message": "User activated successfully"}
    
    return {"message": "User not found or already active"}


@router.put("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: str,
    current_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Deactivate a user account.
    """
    from bson import ObjectId
    from datetime import datetime
    
    users_collection = db.users
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )
    
    if result.modified_count > 0:
        return {"message": "User deactivated successfully"}
    
    return {"message": "User not found or already inactive"}


@router.get("/analytics")
async def get_system_analytics(
    current_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get system-wide analytics and statistics.
    """
    return {
        "message": "System analytics",
        "analytics": {
            "user_growth": {
                "this_month": 120,
                "last_month": 95,
                "growth_rate": 26.3
            },
            "engagement": {
                "daily_active_users": 850,
                "weekly_active_users": 1450,
                "monthly_active_users": 2100
            },
            "performance": {
                "average_gpa": 3.5,
                "average_attendance": 88,
                "completion_rate": 92
            },
            "departments": [
                {"name": "Computer Science", "students": 450, "avg_gpa": 3.6},
                {"name": "Engineering", "students": 380, "avg_gpa": 3.4},
                {"name": "Business", "students": 320, "avg_gpa": 3.5}
            ]
        }
    }


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(require_admin),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Delete a user account (soft delete - mark as inactive).
    """
    from bson import ObjectId
    from datetime import datetime
    
    users_collection = db.users
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_active": False, "deleted_at": datetime.utcnow()}}
    )
    
    if result.modified_count > 0:
        return {"message": "User deleted successfully"}
    
    return {"message": "User not found"}
