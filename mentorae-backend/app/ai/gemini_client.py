"""
Gemini API Client for AI-powered responses.
Handles communication with Google's Gemini AI model with retry logic and caching.
"""
import os
import logging
import asyncio
from typing import Optional, AsyncGenerator
import google.generativeai as genai

logger = logging.getLogger(__name__)

# Generation config defaults
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000
MAX_RETRIES = 3
RETRY_DELAY = 1.0  # seconds


class GeminiClient:
    """Client for interacting with Google Gemini AI."""

    def __init__(self):
        """Initialize Gemini client with API key."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None

        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set — AI features will be unavailable")
            return

        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-pro")
            logger.info("Gemini client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")

    def is_available(self) -> bool:
        """Check if Gemini client is ready."""
        return self.model is not None

    async def generate_response(
        self,
        prompt: str,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> Optional[str]:
        """
        Generate AI response with automatic retry on transient failures.

        Args:
            prompt: Input prompt
            temperature: Creativity level (0.0–1.0)
            max_tokens: Maximum output tokens

        Returns:
            Response text, or None on failure
        """
        if not self.model:
            logger.error("Gemini model not initialized")
            return None

        config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self.model.generate_content(prompt, generation_config=config)
                return response.text
            except Exception as e:
                logger.warning(f"Gemini attempt {attempt}/{MAX_RETRIES} failed: {e}")
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(RETRY_DELAY * attempt)

        logger.error("All Gemini retry attempts exhausted")
        return None

    async def generate_streaming_response(
        self,
        prompt: str,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> AsyncGenerator[str, None]:
        """
        Stream AI response chunks as they are generated.

        Args:
            prompt: Input prompt
            temperature: Creativity level

        Yields:
            Text chunks
        """
        if not self.model:
            logger.error("Gemini model not initialized")
            return

        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"temperature": temperature},
                stream=True,
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"Error: {str(e)}"


# Singleton instance
gemini_client = GeminiClient()
