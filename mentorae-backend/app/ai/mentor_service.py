"""
AI Mentor Service — core business logic for AI-powered academic mentoring.
"""
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase

from .gemini_client import gemini_client
from .prompt_templates import prompt_templates

logger = logging.getLogger(__name__)

# Fallback context used when student record is missing
_EMPTY_CONTEXT: Dict[str, Any] = {
    "department": "Not specified",
    "semester": "Not specified",
    "cgpa": "Not specified",
    "attendance": "Not specified",
    "weak_subjects": [],
}


class MentorService:
    """Service for AI-powered academic mentoring."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.chat_col = db.ai_chat_history
        self.plans_col = db.study_plans
        self.recs_col = db.recommendations

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _get_student_context(self, user_id: str) -> Dict[str, Any]:
        """Fetch student academic context from the database."""
        try:
            from bson import ObjectId

            student = await self.db.students.find_one({"user_id": ObjectId(user_id)})
            if not student:
                return _EMPTY_CONTEXT.copy()

            return {
                "department": student.get("department", "Not specified"),
                "semester": student.get("semester", "Not specified"),
                "cgpa": student.get("gpa", "Not specified"),
                "attendance": student.get("attendance_percentage", "Not specified"),
                "weak_subjects": student.get("weak_subjects", []) or ["None identified"],
            }
        except Exception as e:
            logger.error(f"Error fetching student context for {user_id}: {e}")
            return _EMPTY_CONTEXT.copy()

    def _ai_unavailable(self, feature: str) -> Dict[str, Any]:
        return {"success": False, "error": f"AI service unavailable — {feature} failed"}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def chat(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send a message to the AI mentor and persist the exchange."""
        context = await self._get_student_context(user_id)
        prompt = prompt_templates.get_chat_prompt(message, context)

        response = await gemini_client.generate_response(prompt)
        if not response:
            return self._ai_unavailable("chat")

        await self.chat_col.insert_one(
            {
                "user_id": user_id,
                "conversation_id": conversation_id,
                "message": message,
                "response": response,
                "timestamp": datetime.utcnow(),
                "student_context": context,
            }
        )

        return {
            "success": True,
            "response": response,
            "timestamp": datetime.utcnow().isoformat(),
        }

    async def generate_study_plan(
        self,
        user_id: str,
        duration_days: int,
        subjects: List[str],
        focus_areas: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Generate and persist a personalised study plan."""
        context = await self._get_student_context(user_id)
        prompt = prompt_templates.get_study_plan_prompt(
            duration_days, subjects, context, focus_areas
        )

        plan_text = await gemini_client.generate_response(
            prompt, temperature=0.7, max_tokens=2000
        )
        if not plan_text:
            return self._ai_unavailable("study plan generation")

        result = await self.plans_col.insert_one(
            {
                "user_id": user_id,
                "duration_days": duration_days,
                "subjects": subjects,
                "focus_areas": focus_areas,
                "plan": plan_text,
                "created_at": datetime.utcnow(),
                "student_context": context,
            }
        )

        return {
            "success": True,
            "plan_id": str(result.inserted_id),
            "study_plan": plan_text,
            "duration_days": duration_days,
            "subjects": subjects,
        }

    async def get_recommendations(
        self,
        user_id: str,
        performance_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate and persist personalised academic recommendations."""
        context = await self._get_student_context(user_id)
        prompt = prompt_templates.get_recommendations_prompt(context, performance_data)

        recs_text = await gemini_client.generate_response(
            prompt, temperature=0.7, max_tokens=1500
        )
        if not recs_text:
            return self._ai_unavailable("recommendations")

        result = await self.recs_col.insert_one(
            {
                "user_id": user_id,
                "recommendations": recs_text,
                "created_at": datetime.utcnow(),
                "student_context": context,
                "performance_data": performance_data,
            }
        )

        return {
            "success": True,
            "recommendation_id": str(result.inserted_id),
            "recommendations": recs_text,
        }

    async def get_chat_history(
        self,
        user_id: str,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Return the most recent chat messages for a user."""
        try:
            cursor = (
                self.chat_col.find({"user_id": user_id})
                .sort("timestamp", -1)
                .limit(limit)
            )
            history = await cursor.to_list(length=limit)
            for item in history:
                item["_id"] = str(item["_id"])
            return history
        except Exception as e:
            logger.error(f"Error fetching chat history for {user_id}: {e}")
            return []
