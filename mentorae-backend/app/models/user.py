"""
User model for MongoDB.
Defines the structure of user documents in the database.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserRole:
    """User role constants."""
    STUDENT = "student"
    MENTOR = "mentor"
    ADMIN = "admin"


class UserModel(BaseModel):
    """User database model."""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    hashed_password: str
    full_name: str
    role: str = UserRole.STUDENT
    is_active: bool = True
    is_verified: bool = False
    avatar: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "email": "student@example.com",
                "full_name": "John Doe",
                "role": "student",
                "is_active": True,
                "phone": "+1234567890"
            }
        }


class StudentModel(BaseModel):
    """Student-specific data model."""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    student_id: str
    department: str
    year: int
    semester: int
    gpa: float = 0.0
    attendance_percentage: float = 0.0
    mentor_id: Optional[PyObjectId] = None
    courses: List[str] = []
    achievements: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class MentorModel(BaseModel):
    """Mentor-specific data model."""
    
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    employee_id: str
    department: str
    specialization: str
    experience_years: int
    students: List[PyObjectId] = []
    max_students: int = 20
    bio: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
