from autogen_agentchat.agents import AssistantAgent
from agent.model.ModelFactory import ModelFactory
from pydantic import BaseModel
class ReportAgent:
    def __init__(self, name="ReportAgent", system_message=None):
        """
        Initialize the ReportAgent with a model and assistant agent.
        
        Args:
            name: Name of the agent (default: "ReportAgent")
            system_message: Custom system message for the agent (optional)
        """
        # TODO: Initialize self.model using ModelFactory.get_model()
        raise NotImplementedError("Students must implement the __init__ method")
        
        # TODO: Initialize self.agent as an AssistantAgent with:
        #   - name parameter
        #   - model_client parameter (use self.model)
        #   - system_message parameter (use provided or default message)
        #   - reflect_on_tool_use=False
        #   - model_client_stream=False
        #   - output_content_type=ReportResponse
        
        # Default system message to use if none provided:
        # - Role: Reporting Specialist generating HTML reports
        # - Context: Inputs from DataProfilingAgent and AnalyticsAgent
        # - HTML Structure: Header, nav tabs, executive summary, data profile, 
        #   quality assessment, KPIs, visualizations, recommendations
        # - Style Requirements: Semantic HTML5, inline CSS, tab navigation
        # - Output Format: AgentResponse with html and thoughts fields
        # - Reasoning Workflow: 14 steps from parsing to REPORT_COMPLETE
        # - Constraints: Include all sections, extract HTML filename, use relative paths

    def get_agent(self):
        return self.agent