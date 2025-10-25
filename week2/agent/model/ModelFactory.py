import os
from typing import Any, Optional
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

class ModelFactory:
    """Factory to create model client instances."""

    @staticmethod
    def get_model(
        model: str = "gpt-4o-mini"):
        """
        Create and return an OpenAI model client.
        
        TODO: Implement this method to:
        1. Load environment variables using load_dotenv()
        2. Check if OPENAI_API_KEY exists in environment variables
        3. If not found, raise an EnvironmentError with appropriate message
        4. Create and return an OpenAIChatCompletionClient instance with:
           - model parameter
           - api_key from environment variables
        
        Args:
            model: The model name to use (default: "gpt-4o-mini")
            
        Returns:
            OpenAIChatCompletionClient: Configured model client
            
        Raises:
            EnvironmentError: If OPENAI_API_KEY is not set
        """
        # TODO: Implement this method
        raise NotImplementedError("Please implement the get_model method")