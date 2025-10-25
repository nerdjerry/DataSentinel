from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent
from agent.model.ModelFactory import ModelFactory
import json
import os

from agent.tool.ProfilingReportReaderToolFactory import ProfilingReportReaderToolFactory
class SummarizerAgent:
    def __init__(self, name="SummarizerAgent", system_message=None):
        # TODO: Initialize the model using ModelFactory
        self.model = None  # ModelFactory.get_model()
        
        # TODO: Initialize the profile reader factory with reports directory
        self.profile_reader_factory = None  # ProfilingReportReaderToolFactory(reports_dir="ge_reports")
        
        # TODO: Load the schema
        self.schema = {}  # self._get_schema()
        
        # TODO: Create tools list with profile reader tool
        self.tools = []  # [self.profile_reader_factory.create_read_tool()]
        
        # TODO: Create the AssistantAgent with appropriate configuration
        # Hint: Use the following parameters:
        # - name: provided name parameter
        # - model_client: self.model
        # - description: "Summarizer Agent for Data Quality Issue Reporting"
        # - tools: self.tools
        # - system_message: Use provided or create default with role, schema, capabilities, etc.
        # - reflect_on_tool_use: False
        # - model_client_stream: False
        # - output_content_type: DataQualityAgentReport
        self.agent = None

        def _get_schema(self):
        """Load table schema from metadata/schema.json
        
        TODO: Implement this method to:
        1. Build the schema file path using os.path.join
        2. Open and read the JSON file
        3. Handle FileNotFoundError and json.JSONDecodeError exceptions
        4. Return the loaded schema or empty dict on error
        """
        # TODO: Implement schema loading logic
        return {}
        
    def get_agent(self):
        return self.agent