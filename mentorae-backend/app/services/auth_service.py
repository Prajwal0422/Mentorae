"""
Authentication service for user registration, login, and management.
"""
from datetime import datetime
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException, status
from bson import ObjectId

from app.models import UserModel, StudentModel, MentorModel, UserRole
from app.schemas import UserRegister, UserLogin, StudentRegister, MentorRegister
from app.utils import get_password_hash, verify_password, create_access_token


class AuthService:
    """Service class for authentication operations."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.users_collection = db.users
        self.students_collection = db.students
        self.mentors_collection = db.mentors
    
    async def register_user(
        self, 
        user_data: UserRegister,
        student_data: Optional[StudentRegister] = None,
        mentor_data: Optional[MentorRegister] = None
    ) -> dict:
        """
        Register a new user with role-specific data.
        
        Args:
            user_data: Basic user registration data
            student_data: Student-specific data (if role is student)
            mentor_data: Mentor-specific data (if role is mentor)
            
        Returns:
            dict: Created user document
            
        Raises:
            HTTPException: If email already exists or validation fails
        """
        # Check if user already exists
        existing_user = await self.users_collection.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user document
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["hashed_password"] = get_password_hash(user_data.password)
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()
        user_dict["is_active"] = True
        user_dict["is_verified"] = False
        
        # Insert user
        result = await self.users_collection.insert_one(user_dict)
        user_id = result.inserted_id
        
        # Create role-specific document
        if user_data.role == UserRole.STUDENT and student_data:
            student_dict = student_data.model_dump()
            student_dict["user_id"] = user_id
            student_dict["created_at"] = datetime.utcnow()
            student_dict["updated_at"] = datetime.utcnow()
            await self.students_collection.insert_one(student_dict)
            
        elif user_data.role == UserRole.MENTOR and mentor_data:
            mentor_dict = mentor_data.model_dump()
            mentor_dict["user_id"] = user_id
            mentor_dict["created_at"] = datetime.utcnow()
            mentor_dict["updated_at"] = datetime.utcnow()
            await self.mentors_collection.insert_one(mentor_dict)
        
        # Fetch and return created user
        created_user = await self.users_collection.find_one({"_id": user_id})
        created_user["_id"] = str(created_user["_id"])
        
        return created_user
    
    async def authenticate_user(self, login_data: UserLogin) -> Optional[dict]:
        """
        Authenticate user with email and password.
        
        Args:
            login_data: User login credentials
            
        Returns:
            dict: User document if authentication successful, None otherwise
        """
        user = await self.users_collection.find_one({"email": login_data.email})
        
        if not user:
            return None
        
        if not verify_password(login_data.password, user["hashed_password"]):
            return None
        
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        # Update last login
        await self.users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        user["_id"] = str(user["_id"])
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """
        Get user by email address.
        
        Args:
            email: User email address
            
        Returns:
            dict: User document or None
        """
        user = await self.users_collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user
    
    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID string
            
        Returns:
            dict: User document or None
        """
        try:
            user = await self.users_collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user["_id"] = str(user["_id"])
            return user
        except Exception:
            return None
    
    async def update_user(self, user_id: str, update_data: dict) -> Optional[dict]:
        """
        Update user profile.
        
        Args:
            user_id: User ID string
            update_data: Dictionary of fields to update
            
        Returns:
            dict: Updated user document or None
        """
        try:
            update_data["updated_at"] = datetime.utcnow()
            
            result = await self.users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            if result.modified_count == 0:
                return None
            
            return await self.get_user_by_id(user_id)
            
        except Exception:
            return None
    
    async def change_password(
        self, 
        user_id: str, 
        current_password: str, 
        new_password: str
    ) -> bool:
        """
        Change user password.
        
        Args:
            user_id: User ID string
            current_password: Current password
            new_password: New password
            
        Returns:
            bool: True if password changed successfully
            
        Raises:
            HTTPException: If current password is incorrect
        """
        user = await self.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not verify_password(current_password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        hashed_password = get_password_hash(new_password)
        
        result = await self.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "hashed_password": hashed_password,
                "updated_at": datetime.utcnow()
            }}
        )
        
        return result.modified_count > 0
