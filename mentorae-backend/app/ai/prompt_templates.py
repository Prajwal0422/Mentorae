"""
Prompt templates for AI Mentor Assistant.
Provides structured prompts for different academic guidance scenarios.
"""
from typing import Dict, Any


class PromptTemplates:
    """Collection of prompt templates for AI mentor."""
    
    @staticmethod
    def get_mentor_system_prompt() -> str:
        """Get the system prompt for AI mentor."""
        return """You are Mentorae, an expert AI Academic Mentor and Learning Assistant. Your role is to:

1. Provide personalized academic guidance and support
2. Explain complex concepts in simple, understandable terms
3. Suggest effective study strategies and learning techniques
4. Recommend relevant learning resources
5. Help students improve their academic performance
6. Motivate and encourage students in their learning journey

Guidelines:
- Be supportive, encouraging, and patient
- Provide clear, structured explanations
- Use examples and analogies when helpful
- Tailor advice to the student's level and context
- Focus on understanding, not just memorization
- Encourage critical thinking and problem-solving
- Be concise but comprehensive

Always maintain a friendly, professional tone and prioritize the student's learning success."""
    
    @staticmethod
    def get_chat_prompt(
        user_message: str,
        student_context: Dict[str, Any]
    ) -> str:
        """
        Generate chat prompt with student context.
        
        Args:
            user_message: Student's question or message
            student_context: Student's academic information
            
        Returns:
            Formatted prompt string
        """
        context_str = f"""
Student Context:
- Department: {student_context.get('department', 'Not specified')}
- Current Semester: {student_context.get('semester', 'Not specified')}
- CGPA: {student_context.get('cgpa', 'Not specified')}
- Attendance: {student_context.get('attendance', 'Not specified')}%
- Weak Subjects: {', '.join(student_context.get('weak_subjects', ['None identified']))}
"""
        
        return f"""{PromptTemplates.get_mentor_system_prompt()}

{context_str}

Student Question: {user_message}

Please provide a helpful, personalized response considering the student's context."""
    
    @staticmethod
    def get_study_plan_prompt(
        duration_days: int,
        subjects: list,
        student_context: Dict[str, Any],
        focus_areas: list = None
    ) -> str:
        """
        Generate study plan prompt.
        
        Args:
            duration_days: Number of days for the plan
            subjects: List of subjects to include
            student_context: Student's academic information
            focus_areas: Specific areas to focus on
            
        Returns:
            Formatted prompt string
        """
        focus_str = f"\nFocus Areas: {', '.join(focus_areas)}" if focus_areas else ""
        
        return f"""{PromptTemplates.get_mentor_system_prompt()}

Create a detailed {duration_days}-day study plan for the following student:

Student Profile:
- Department: {student_context.get('department', 'Not specified')}
- Semester: {student_context.get('semester', 'Not specified')}
- CGPA: {student_context.get('cgpa', 'Not specified')}
- Attendance: {student_context.get('attendance', 'Not specified')}%
- Weak Subjects: {', '.join(student_context.get('weak_subjects', ['None']))}

Subjects to Cover: {', '.join(subjects)}{focus_str}

Requirements:
1. Create a day-by-day breakdown
2. Allocate appropriate time for each subject
3. Include breaks and revision sessions
4. Prioritize weak subjects
5. Balance theory and practice
6. Include self-assessment checkpoints
7. Provide specific learning objectives for each day

Format the plan clearly with:
- Day number and date
- Time slots
- Subject/Topic
- Learning objectives
- Recommended resources
- Practice exercises

Make it realistic and achievable."""
    
    @staticmethod
    def get_recommendations_prompt(
        student_context: Dict[str, Any],
        performance_data: Dict[str, Any] = None
    ) -> str:
        """
        Generate personalized recommendations prompt.
        
        Args:
            student_context: Student's academic information
            performance_data: Recent performance metrics
            
        Returns:
            Formatted prompt string
        """
        perf_str = ""
        if performance_data:
            perf_str = f"""
Recent Performance:
- Recent Test Scores: {performance_data.get('recent_scores', 'Not available')}
- Assignment Completion: {performance_data.get('assignment_completion', 'Not available')}%
- Improvement Trend: {performance_data.get('trend', 'Not available')}
"""
        
        return f"""{PromptTemplates.get_mentor_system_prompt()}

Analyze the following student profile and provide personalized recommendations:

Student Profile:
- Department: {student_context.get('department', 'Not specified')}
- Semester: {student_context.get('semester', 'Not specified')}
- CGPA: {student_context.get('cgpa', 'Not specified')}
- Attendance: {student_context.get('attendance', 'Not specified')}%
- Weak Subjects: {', '.join(student_context.get('weak_subjects', ['None']))}{perf_str}

Provide 5-7 specific, actionable recommendations covering:
1. Study strategies for weak subjects
2. Time management improvements
3. Resource recommendations (books, online courses, videos)
4. Practice and revision techniques
5. Attendance improvement strategies (if needed)
6. CGPA improvement plan
7. Skill development suggestions

For each recommendation:
- Explain WHY it's important
- Provide SPECIFIC action steps
- Suggest HOW to implement it
- Estimate the expected IMPACT

Prioritize recommendations by urgency and impact."""
    
    @staticmethod
    def get_concept_explanation_prompt(
        concept: str,
        subject: str,
        difficulty_level: str = "intermediate"
    ) -> str:
        """
        Generate concept explanation prompt.
        
        Args:
            concept: Concept to explain
            subject: Subject area
            difficulty_level: Student's level (beginner/intermediate/advanced)
            
        Returns:
            Formatted prompt string
        """
        return f"""{PromptTemplates.get_mentor_system_prompt()}

Explain the following concept to a {difficulty_level} level student:

Subject: {subject}
Concept: {concept}

Your explanation should:
1. Start with a simple, intuitive definition
2. Break down the concept into key components
3. Use real-world examples and analogies
4. Explain why it's important
5. Show how it connects to other concepts
6. Provide a practical example or application
7. Suggest resources for deeper learning

Make it engaging and easy to understand while maintaining accuracy."""


# Singleton instance
prompt_templates = PromptTemplates()
