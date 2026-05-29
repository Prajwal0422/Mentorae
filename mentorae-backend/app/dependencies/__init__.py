"""Dependencies package."""
from .auth import (
    get_current_user,
    get_current_active_user,
    require_role,
    require_roles,
    require_student,
    require_mentor,
    require_admin,
    require_mentor_or_admin
)

__all__ = [
    "get_current_user",
    "get_current_active_user",
    "require_role",
    "require_roles",
    "require_student",
    "require_mentor",
    "require_admin",
    "require_mentor_or_admin"
]
