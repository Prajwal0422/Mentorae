"""
Gemini API Client for AI-powered responses.
Handles communication with Google's Gemini AI model.
"""
import os
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai
from app.config import settings

logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for interacting with Google Gemini AI."""
    
    def __init__(self):
        """Initialize Gemini client with API key."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
            self.model = None
            return
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            self.model = None
    
    async def generate_response(
        self, 
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """
        Generate AI response using Gemini.
        
        Args:
            prompt: Input prompt for the AI
            temperature: Creativity level (0.0 to 1.0)
            max_tokens: Maximum response length
            
        Returns:
            Generated response text or None if error
        """
        if not self.model:
            logger.error("Gemini model not initialized")
            return None
        
        try:
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return None
    
    async def generate_streaming_response(
        self,
        prompt: str,
        temperature: float = 0.7
    ):
        """
        Generate streaming AI response.
        
        Args:
            prompt: Input prompt for the AI
            temperature: Creativity level
            
        Yields:
            Response chunks as they're generated
        """
        if not self.model:
            logger.error("Gemini model not initialized")
            return
        
        try:
            generation_config = {
                "temperature": temperature,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            logger.error(f"Error in streaming response: {e}")
            yield f"Error: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if Gemini client is available."""
        return self.model is not None


# Global client instance
gemini_client = GeminiClient()
