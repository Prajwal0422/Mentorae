"""
Authentication dependencies for route protection and user verification.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config import get_database
from app.utils import decode_access_token
from app.services import AuthService
from app.models import UserRole

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> dict:
    """
    Get current authenticated user from JWT token.
    
    Args:
        token: JWT access token
        db: Database instance
        
    Returns:
        dict: Current user document
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode token
    token_data = decode_access_token(token)
    if token_data is None or token_data.email is None:
        raise credentials_exception
    
    # Get user from database
    auth_service = AuthService(db)
    user = await auth_service.get_user_by_email(token_data.email)
    
    if user is None:
        raise credentials_exception
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user


async def get_current_active_user(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Get current active user.
    
    Args:
        current_user: Current user from get_current_user
        
    Returns:
        dict: Current active user
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def require_role(required_role: str):
    """
    Dependency factory for role-based access control.
    
    Args:
        required_role: Required user role
        
    Returns:
        Dependency function that checks user role
    """
    async def role_checker(current_user: dict = Depends(get_current_active_user)) -> dict:
        """
        Check if user has required role.
        
        Args:
            current_user: Current authenticated user
            
        Returns:
            dict: Current user if role matches
            
        Raises:
            HTTPException: If user doesn't have required role
        """
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {required_role}"
            )
        return current_user
    
    return role_checker


def require_roles(required_roles: list):
    """
    Dependency factory for multiple role-based access control.
    
    Args:
        required_roles: List of allowed user roles
        
    Returns:
        Dependency function that checks if user has any of the required roles
    """
    async def roles_checker(current_user: dict = Depends(get_current_active_user)) -> dict:
        """
        Check if user has any of the required roles.
        
        Args:
            current_user: Current authenticated user
            
        Returns:
            dict: Current user if role matches
            
        Raises:
            HTTPException: If user doesn't have any required role
        """
        if current_user.get("role") not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(required_roles)}"
            )
        return current_user
    
    return roles_checker


# Pre-defined role dependencies
require_student = require_role(UserRole.STUDENT)
require_mentor = require_role(UserRole.MENTOR)
require_admin = require_role(UserRole.ADMIN)
require_mentor_or_admin = require_roles([UserRole.MENTOR, UserRole.ADMIN])
