from agent.SummarizerAgent import DataQualityIssue
from agent.tool.SnowflakeQueryToolFactory import SnowflakeQueryToolFactory
from autogen_agentchat.agents import AssistantAgent
from agent.model.ModelFactory import ModelFactory
from pydantic import BaseModel
import json
import os


class DataAgent:
    def __init__(self, name="DataAgent", system_message=None):
        """
        Initialize DataAgent.
        
        Args:
            name: Agent name
            system_message: Custom system prompt
            output_structured_report: If True, outputs DataAgentReport instead of plain text
        """
        # TODO: Initialize the SnowflakeQueryToolFactory
        self.snowflakeToolFactory = None  # Initialize SnowflakeQueryToolFactory here
        
        # TODO: Get the model from ModelFactory
        self.model = None  # Get model using ModelFactory.get_model()
        
        # TODO: Load the schema
        self.schema = {}  # Load schema using self._get_schema()
        
        # TODO: Create the tools list with the following tools:
        # - Query tool from snowflakeToolFactory
        # - Table info tool from snowflakeToolFactory  
        # - List tables tool from snowflakeToolFactory
        self.tools = []  # Create tools list
        
        # TODO: Initialize the AssistantAgent with:
        # - name: use the provided name parameter
        # - tools: use self.tools
        # - model_client: use self.model
        # - description: "Data Investigation Agent for identifying data quality issues"
        # - system_message: use system_message parameter or self._system_message()
        # - model_client_stream: False (to disable streaming for structured output)
        # - reflect_on_tool_use: False (to prevent JSON parsing issues)
        # - output_content_type: DataAgentReport
        self.agent = None  # Initialize AssistantAgent here

    def _get_schema(self):
        """Load table schema from metadata/schema.json"""
        # TODO: Construct the schema file path
        # Hint: Use os.path.join to build path to 'metadata/schema.json'
        # The schema file is located two directories up from this file
        schema_path = None  # Build the path to metadata/schema.json
        
        # TODO: Load and return the schema
        # 1. Open the schema file
        # 2. Parse the JSON content
        # 3. Handle FileNotFoundError - print warning and return empty dict
        # 4. Handle json.JSONDecodeError - print warning and return empty dict
        return {}  # Load and return the schema from the file
    
    def get_agent(self):
        return self.agent