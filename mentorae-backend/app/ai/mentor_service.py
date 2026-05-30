"""
AI Mentor Service - Core business logic for AI-powered academic mentoring.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase

from .gemini_client import gemini_client
from .prompt_templates import prompt_templates

logger = logging.getLogger(__name__)


class MentorService:
    """Service for AI-powered academic mentoring."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        """
        Initialize mentor service.
        
        Args:
            db: MongoDB database instance
        """
        self.db = db
        self.chat_history_collection = db.ai_chat_history
        self.study_plans_collection = db.study_plans
        self.recommendations_collection = db.recommendations
    
    async def get_student_context(self, user_id: str) -> Dict[str, Any]:
        """
        Get student's academic context from database.
        
        Args:
            user_id: Student's user ID
            
        Returns:
            Dictionary with student context
        """
        try:
            from bson import ObjectId
            
            # Get student data
            student = await self.db.students.find_one({"user_id": ObjectId(user_id)})
            
            if not student:
                return {
                    "department": "Not specified",
                    "semester": "Not specified",
                    "cgpa": "Not specified",
                    "attendance": "Not specified",
                    "weak_subjects": []
                }
            
            # Identify weak subjects (example logic - can be enhanced)
            weak_subjects = []
            # This would typically come from performance analysis
            
            return {
                "department": student.get("department", "Not specified"),
                "semester": student.get("semester", "Not specified"),
                "cgpa": student.get("gpa", "Not specified"),
                "attendance": student.get("attendance_percentage", "Not specified"),
                "weak_subjects": weak_subjects or ["None identified"]
            }
            
        except Exception as e:
            logger.error(f"Error getting student context: {e}")
            return {
                "department": "Not specified",
                "semester": "Not specified",
                "cgpa": "Not specified",
                "attendance": "Not specified",
                "weak_subjects": []
            }
    
    async def chat(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle chat interaction with AI mentor.
        
        Args:
            user_id: Student's user ID
            message: Student's message
            conversation_id: Optional conversation ID for context
            
        Returns:
            Dictionary with AI response and metadata
        """
        try:
            # Get student context
            student_context = await self.get_student_context(user_id)
            
            # Generate prompt
            prompt = prompt_templates.get_chat_prompt(message, student_context)
            
            # Get AI response
            response = await gemini_client.generate_response(prompt)
            
            if not response:
                return {
                    "success": False,
                    "error": "Failed to generate response"
                }
            
            # Save to chat history
            chat_record = {
                "user_id": user_id,
                "conversation_id": conversation_id,
                "message": message,
                "response": response,
                "timestamp": datetime.utcnow(),
                "student_context": student_context
            }
            
            await self.chat_history_collection.insert_one(chat_record)
            
            return {
                "success": True,
                "response": response,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_study_plan(
        self,
        user_id: str,
        duration_days: int,
        subjects: List[str],
        focus_areas: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate personalized study plan.
        
        Args:
            user_id: Student's user ID
            duration_days: Plan duration in days
            subjects: List of subjects
            focus_areas: Optional focus areas
            
        Returns:
            Dictionary with study plan
        """
        try:
            # Get student context
            student_context = await self.get_student_context(user_id)
            
            # Generate prompt
            prompt = prompt_templates.get_study_plan_prompt(
                duration_days,
                subjects,
                student_context,
                focus_areas
            )
            
            # Get AI response
            study_plan = await gemini_client.generate_response(
                prompt,
                temperature=0.7,
                max_tokens=2000
            )
            
            if not study_plan:
                return {
                    "success": False,
                    "error": "Failed to generate study plan"
                }
            
            # Save study plan
            plan_record = {
                "user_id": user_id,
                "duration_days": duration_days,
                "subjects": subjects,
                "focus_areas": focus_areas,
                "plan": study_plan,
                "created_at": datetime.utcnow(),
                "student_context": student_context
            }
            
            result = await self.study_plans_collection.insert_one(plan_record)
            
            return {
                "success": True,
                "plan_id": str(result.inserted_id),
                "study_plan": study_plan,
                "duration_days": duration_days,
                "subjects": subjects
            }
            
        except Exception as e:
            logger.error(f"Error generating study plan: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_recommendations(
        self,
        user_id: str,
        performance_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate personalized recommendations.
        
        Args:
            user_id: Student's user ID
            performance_data: Optional performance metrics
            
        Returns:
            Dictionary with recommendations
        """
        try:
            # Get student context
            student_context = await self.get_student_context(user_id)
            
            # Generate prompt
            prompt = prompt_templates.get_recommendations_prompt(
                student_context,
                performance_data
            )
            
            # Get AI response
            recommendations = await gemini_client.generate_response(
                prompt,
                temperature=0.7,
                max_tokens=1500
            )
            
            if not recommendations:
                return {
                    "success": False,
                    "error": "Failed to generate recommendations"
                }
            
            # Save recommendations
            rec_record = {
                "user_id": user_id,
                "recommendations": recommendations,
                "created_at": datetime.utcnow(),
                "student_context": student_context,
                "performance_data": performance_data
            }
            
            result = await self.recommendations_collection.insert_one(rec_record)
            
            return {
                "success": True,
                "recommendation_id": str(result.inserted_id),
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_chat_history(
        self,
        user_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get user's chat history.
        
        Args:
            user_id: Student's user ID
            limit: Maximum number of messages
            
        Returns:
            List of chat messages
        """
        try:
            cursor = self.chat_history_collection.find(
                {"user_id": user_id}
            ).sort("timestamp", -1).limit(limit)
            
            history = await cursor.to_list(length=limit)
            
            # Convert ObjectId to string
            for item in history:
                item["_id"] = str(item["_id"])
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting chat history: {e}")
            return []
