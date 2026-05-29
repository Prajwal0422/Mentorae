"""
Authentication routes for user registration, login, and profile management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config import get_database
from app.schemas import (
    UserRegister,
    UserLogin,
    UserResponse,
    UserUpdate,
    PasswordChange,
    StudentRegister,
    MentorRegister,
    Token
)
from app.services import AuthService
from app.utils import create_access_token
from app.dependencies import get_current_active_user
from app.models import UserRole

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    student_data: StudentRegister = None,
    mentor_data: MentorRegister = None,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Register a new user.
    
    - **email**: Valid email address
    - **password**: Strong password (min 8 chars, uppercase, lowercase, digit)
    - **full_name**: User's full name
    - **role**: User role (student, mentor, admin)
    - **student_data**: Required if role is student
    - **mentor_data**: Required if role is mentor
    """
    auth_service = AuthService(db)
    
    # Validate role-specific data
    if user_data.role == UserRole.STUDENT and not student_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student data is required for student registration"
        )
    
    if user_data.role == UserRole.MENTOR and not mentor_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mentor data is required for mentor registration"
        )
    
    # Register user
    user = await auth_service.register_user(user_data, student_data, mentor_data)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"]}
    )
    
    # Remove sensitive data
    user.pop("hashed_password", None)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Login with email and password.
    
    Returns JWT access token on successful authentication.
    """
    auth_service = AuthService(db)
    
    # Create login data from form
    login_data = UserLogin(email=form_data.username, password=form_data.password)
    
    # Authenticate user
    user = await auth_service.authenticate_user(login_data)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"]}
    )
    
    # Remove sensitive data
    user.pop("hashed_password", None)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get current authenticated user's profile.
    
    Requires valid JWT token in Authorization header.
    """
    # Remove sensitive data
    current_user.pop("hashed_password", None)
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Update current user's profile.
    
    Only updates provided fields.
    """
    auth_service = AuthService(db)
    
    # Filter out None values
    update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
    
    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    # Update user
    updated_user = await auth_service.update_user(current_user["_id"], update_dict)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Remove sensitive data
    updated_user.pop("hashed_password", None)
    return updated_user


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    password_data: PasswordChange,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Change current user's password.
    
    Requires current password for verification.
    """
    auth_service = AuthService(db)
    
    success = await auth_service.change_password(
        current_user["_id"],
        password_data.current_password,
        password_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to change password"
        )
    
    return {"message": "Password changed successfully"}


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(current_user: dict = Depends(get_current_active_user)):
    """
    Logout current user.
    
    Note: JWT tokens are stateless. Client should discard the token.
    """
    return {"message": "Logged out successfully"}
