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
        return """You are Mentorae, an expert AI Academic Mentor and Learning Assistant with deep expertise in pedagogy and student success strategies.

Core Responsibilities:
1. Provide personalized, context-aware academic guidance
2. Explain complex concepts using the Feynman Technique (simple terms, analogies, examples)
3. Design effective study strategies based on cognitive science principles
4. Recommend high-quality, relevant learning resources
5. Analyze performance patterns and suggest targeted improvements
6. Foster growth mindset and intrinsic motivation

Communication Style:
- Supportive, encouraging, and empathetic
- Clear, structured, and actionable
- Socratic when appropriate (guide discovery through questions)
- Adaptive to student's comprehension level
- Concise yet comprehensive

Pedagogical Approach:
- Focus on deep understanding over rote memorization
- Encourage active learning and spaced repetition
- Promote metacognition (thinking about thinking)
- Connect concepts to real-world applications
- Build on prior knowledge progressively
- Address misconceptions directly

Always prioritize the student's long-term learning success and academic growth."""
    
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
        # Build context dynamically
        context_parts = []
        
        if student_context.get('department'):
            context_parts.append(f"Department: {student_context['department']}")
        if student_context.get('semester'):
            context_parts.append(f"Semester: {student_context['semester']}")
        if student_context.get('cgpa'):
            context_parts.append(f"CGPA: {student_context['cgpa']}")
        if student_context.get('attendance'):
            context_parts.append(f"Attendance: {student_context['attendance']}%")
        
        weak_subjects = student_context.get('weak_subjects', [])
        if weak_subjects:
            context_parts.append(f"Areas needing improvement: {', '.join(weak_subjects)}")
        
        context_str = "\n- ".join(context_parts) if context_parts else "Limited profile data available"
        
        return f"""{PromptTemplates.get_mentor_system_prompt()}

Student Profile:
- {context_str}

Student Question: {user_message}

Provide a personalized, actionable response that:
1. Directly addresses the question
2. Considers the student's academic context
3. Offers specific, practical advice
4. Includes relevant examples or resources when helpful
5. Encourages further learning

Keep responses focused and valuable."""
    
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


    @staticmethod
    def get_exam_preparation_prompt(
        exam_date: str,
        subjects: list,
        student_context: Dict[str, Any]
    ) -> str:
        """
        Generate exam preparation roadmap prompt.
        
        Args:
            exam_date: Date of the exam
            subjects: List of subjects for exam
            student_context: Student's academic information
            
        Returns:
            Formatted prompt string
        """
        return f"""{PromptTemplates.get_mentor_system_prompt()}

Create a comprehensive exam preparation roadmap for:

Exam Date: {exam_date}
Subjects: {', '.join(subjects)}

Student Profile:
- Department: {student_context.get('department', 'Not specified')}
- Semester: {student_context.get('semester', 'Not specified')}
- CGPA: {student_context.get('cgpa', 'Not specified')}
- Weak Subjects: {', '.join(student_context.get('weak_subjects', ['None']))}

Create a strategic preparation plan that includes:
1. Timeline breakdown (weeks/days before exam)
2. Subject-wise preparation strategy
3. Topic prioritization based on importance and difficulty
4. Revision schedule
5. Practice test schedule
6. Last-minute revision tips
7. Exam day strategies
8. Stress management techniques

Make it practical and achievable."""


# Singleton instance
prompt_templates = PromptTemplates()
