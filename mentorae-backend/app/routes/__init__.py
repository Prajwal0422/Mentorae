"""Routes package."""
from .auth import router as auth_router
from .student import router as student_router
from .mentor import router as mentor_router
from .admin import router as admin_router

__all__ = [
    "auth_router",
    "student_router",
    "mentor_router",
    "admin_router"
]
