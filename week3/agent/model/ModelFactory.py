import os
from typing import Any, Optional
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

class ModelFactory:
    """Factory to create model client instances."""

    @staticmethod
    def get_model(
        model: str = "gpt-5-mini"):
        load_dotenv()
        # Ensure the API key is available
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError(
            "OPENAI_API_KEY not set. Export it in your environment or add it to a .env file."
            )
        return OpenAIChatCompletionClient(
            model=model,
            api_key=os.environ.get("OPENAI_API_KEY")  # Reads API key from environment variable
    )