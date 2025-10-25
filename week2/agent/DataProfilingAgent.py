import os
import json
from agent.tool.SnowflakeDataProfilingToolFactory import SnowflakeDataProfilingToolFactory
from autogen_agentchat.agents import AssistantAgent
from agent.model.ModelFactory import ModelFactory
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class DataProfilingAgent:
    """
    A specialized agent for data profiling and quality assessment using ydata-profiling.
    
    This agent can:
    - Profile datasets
    - Generate comprehensive interactive HTML and JSON reports
    - Analyze data quality metrics, correlations, and distributions
    - Provide insights on data patterns and anomalies
    """

    def __init__(self, name="DataProfilingAgent", system_message=None, reports_dir="ge_reports"):
        """
        Initialize the DataProfilingAgent.
        
        Args:
            name (str): Name of the agent
            description (str): Custom description/system prompt for the agent
            reports_dir (str): Directory for storing generated reports
        """
        # TODO: Initialize the profiling tool factory
        # Hint: Use SnowflakeDataProfilingToolFactory with the reports_dir parameter
        self.profiling_tool_factory = None  # IMPLEMENT THIS
        
        # TODO: Get the model from ModelFactory
        # Hint: Use ModelFactory.get_model()
        self.model = None  # IMPLEMENT THIS
        
        # TODO: Create the tools list
        # Hint: Use profiling_tool_factory.create_profile_tool()
        self.tools = []  # IMPLEMENT THIS
        
        # TODO: Get the schema
        # Hint: Call the _get_schema() method
        self.schema = None  # IMPLEMENT THIS
        
        # TODO: Initialize the AssistantAgent with appropriate parameters
        # Hint: Use the following parameters:
        # - name: use the provided name parameter
        # - tools: use self.tools
        # - model_client: use self.model
        # - description: "Data Profiling Agent for analyzing data quality and generating reports"
        # - system_message: use system_message parameter or self._system_message()
        # - model_client_stream: False (to disable streaming for structured output)
        # - reflect_on_tool_use: False (to prevent multiple JSON outputs)
        # - output_content_type: DataProfilingReport
        self.agent = None  # IMPLEMENT THIS
    
    def _get_schema(self):
        """Load table schema from metadata/schema.json"""
        # TODO: Implement schema loading
        # Hint: 
        # 1. Construct the path to metadata/schema.json using os.path.join
        #    - Use os.path.dirname twice to go up two directories from the current file
        #    - Then join with 'metadata' and 'schema.json'
        # 2. Use a try-except block to handle potential errors:
        #    - FileNotFoundError: if the schema file doesn't exist
        #    - json.JSONDecodeError: if the JSON is invalid
        # 3. Open the file and load the JSON content
        # 4. Return the loaded schema dictionary, or an empty dict {} if there's an error
        
        return {}  # IMPLEMENT THIS
    
    def get_agent(self):
        """
        Get the configured AutoGen agent.
        
        Returns:
            AssistantAgent: Configured agent with ydata-profiling capabilities
        """
        return self.agent
