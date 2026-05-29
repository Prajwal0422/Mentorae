"""
Pydantic schemas for user-related requests and responses.
Used for data validation and API documentation.
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')


class UserRegister(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, max_length=100)
    role: str = Field(default="student", pattern="^(student|mentor|admin)$")
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "student@example.com",
                "full_name": "John Doe",
                "password": "SecurePass123",
                "role": "student",
                "phone": "+1234567890"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "student@example.com",
                "password": "SecurePass123"
            }
        }


class UserResponse(UserBase):
    """Schema for user response."""
    id: str = Field(..., alias="_id")
    role: str
    is_active: bool
    is_verified: bool
    avatar: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "email": "student@example.com",
                "full_name": "John Doe",
                "role": "student",
                "is_active": True,
                "is_verified": False,
                "phone": "+1234567890",
                "created_at": "2024-01-01T00:00:00",
                "last_login": "2024-01-15T10:30:00"
            }
        }


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    avatar: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Updated Doe",
                "phone": "+1234567890",
                "avatar": "https://example.com/avatar.jpg"
            }
        }


class PasswordChange(BaseModel):
    """Schema for password change."""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @validator('new_password')
    def validate_password(cls, v):
        """Validate password strength."""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v


class StudentRegister(BaseModel):
    """Schema for student-specific registration data."""
    student_id: str = Field(..., min_length=5, max_length=20)
    department: str = Field(..., min_length=2, max_length=100)
    year: int = Field(..., ge=1, le=6)
    semester: int = Field(..., ge=1, le=12)
    
    class Config:
        json_schema_extra = {
            "example": {
                "student_id": "STU2024001",
                "department": "Computer Science",
                "year": 2,
                "semester": 3
            }
        }


class MentorRegister(BaseModel):
    """Schema for mentor-specific registration data."""
    employee_id: str = Field(..., min_length=5, max_length=20)
    department: str = Field(..., min_length=2, max_length=100)
    specialization: str = Field(..., min_length=2, max_length=100)
    experience_years: int = Field(..., ge=0, le=50)
    bio: Optional[str] = Field(None, max_length=500)
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP2024001",
                "department": "Computer Science",
                "specialization": "Machine Learning",
                "experience_years": 5,
                "bio": "Experienced mentor in AI and ML"
            }
        }


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "_id": "507f1f77bcf86cd799439011",
                    "email": "student@example.com",
                    "full_name": "John Doe",
                    "role": "student"
                }
            }
        }


class TokenData(BaseModel):
    """Schema for token payload data."""
    email: Optional[str] = None
    role: Optional[str] = None
