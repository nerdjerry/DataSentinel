import json
import os
from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent
from agent.model.ModelFactory import ModelFactory


class PlannerAgent:
    """
    Planner Agent that takes a data quality goal and creates a comprehensive plan
    with specific tasks for DataAgent (queries) and DataProfilingAgent (profiling).
    
    This agent:
    - Understands data quality goals
    - Reads table schema from metadata/schema.json
    - Plans appropriate tasks for DataAgent to gather evidence
    - Plans profiling analyses to understand distributions and patterns
    - Sequences tasks for optimal analysis
    - Provides clear success criteria
    """

    def __init__(self, name="PlannerAgent", system_message=None):
        """
        Initialize the PlannerAgent.
        
        Args:
            name (str): Name of the agent
            system_message (str): Custom system message/prompt for the agent
        """
        # TODO: Initialize the model using ModelFactory.get_model()
        self.model = None  # Placeholder
        
        # TODO: Load the schema using _load_schema() method
        self.schema = None  # Placeholder
        
        # TODO: Create an AssistantAgent with appropriate parameters:
        # - name: Use the provided name parameter
        # - model_client: Use self.model
        # - description: "Planner Agent for Data Quality Analysis"
        # - system_message: Use provided system_message or call _system_message()
        # - model_client_stream: Set to False for structured output
        # - reflect_on_tool_use: Set to False (Planner doesn't use tools)
        # - output_content_type: Use DataQualityPlan
        self.agent = None  # Placeholder
        raise NotImplementedError("Students need to implement the __init__ method")
    
    def _load_schema(self) -> dict:
        """Load table schema from metadata/schema.json"""
        # TODO: Implement schema loading logic:
        # 1. Construct the path to metadata/schema.json (use os.path.join and os.path.dirname)
        # 2. Try to open and read the JSON file
        # 3. Handle FileNotFoundError - print warning and return empty dict
        # 4. Handle json.JSONDecodeError - print warning and return empty dict
        # 5. Return the loaded schema as a dictionary
        raise NotImplementedError("Students need to implement the _load_schema method")
    
    def get_agent(self):
        """Return the AutoGen agent instance"""
        return self.agent
