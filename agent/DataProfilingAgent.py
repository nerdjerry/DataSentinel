import os
import json
from agent.tool.SnowflakeDataProfilingToolFactory import SnowflakeDataProfilingToolFactory
from autogen_agentchat.agents import AssistantAgent
from agent.model.ModelFactory import ModelFactory
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class DataProfilingTasksExecuted(BaseModel):
    """Result of a single data profiling operation"""
    task_purpose: str  # Why this profiling was performed
    query_or_dataset: str  # The SQL query or dataset profiled
    row_count: int  # Number of rows profiled
    column_count: int  # Number of columns profiled
    html_report_path: str  # Path to generated HTML report
    json_report_path: str  # Path to generated JSON report

class DataProfilingReport(BaseModel):
    """Complete report from DataProfilingAgent after executing profiling tasks"""
    plan_goal: str  # The original profiling goal
    tasks_executed: List[DataProfilingTasksExecuted]  # All profiling operations performed
    next_steps: List[str]  # Recommended follow-up actions

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
        self.profiling_tool_factory = SnowflakeDataProfilingToolFactory(reports_dir=reports_dir)
        self.model = ModelFactory.get_model()
        self.tools = [
            self.profiling_tool_factory.create_profile_tool()
        ]
        self.schema = self._get_schema()
        self.agent = AssistantAgent(
            name=name,
            tools=self.tools,
            model_client=self.model,
            description="Data Profiling Agent for analyzing data quality and generating reports",
            system_message=system_message or self._system_message(),
            model_client_stream=False,  # Disable streaming for structured output
            reflect_on_tool_use=False,  # Disabled to prevent multiple JSON outputs with structured output
            output_content_type=DataProfilingReport
        )
    
    def _system_message(self) -> str:
        """Return the default agent description/system prompt."""
        schema_info = json.dumps(self.schema, indent=2) if self.schema else "No schema available"
        
        return f"""{{
                "role": "You are the Data Profiling Agent. Given a profiling goal, determine the appropriate Snowflake SQL query and use the profiling tool to analyze data quality and structure.",

                "database_schema": {schema_info},

                "capabilities": {{
                    "tools": ["profile_data"],
                    "actions": [
                        "Identify and construct Snowflake SQL for profiling",
                        "Run profiling to generate HTML and JSON reports",
                        "Analyze nulls, distributions, correlations, and duplicates",
                        "Summarize key data quality insights"
                    ]
                }},

                "output_format": {{
                    "plan_goal": "Original profiling goal",
                    "tasks_executed": [
                    {{
                        "task_purpose": "Purpose of profiling task",
                        "query_or_dataset": "SQL query or dataset profiled",
                        "row_count": 0,
                        "column_count": 0,
                        "html_report_path": "path/to/report.html",
                        "json_report_path": "path/to/report.json"
                    }}
                    ],
                    "next_steps": ["Recommended follow-up actions"]
                }},

                "constraints": [
                    "Profile up to 100,000 rows per run",
                    "Use valid Snowflake SQL and schema columns only",
                    "Return output strictly in JSON format matching DataProfilingReport",
                    "Do not output extra text or explanations"
                ],

                "termination_condition": "Execute profiling once, produce a complete DataProfilingReport, and terminate after returning results."
        }}"""

    def _get_schema(self):
        """Load table schema from metadata/schema.json"""
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'metadata', 'schema.json')
        try:
            with open(schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Schema file not found at {schema_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in schema file {schema_path}")
            return {}
    
    def get_agent(self):
        """
        Get the configured AutoGen agent.
        
        Returns:
            AssistantAgent: Configured agent with ydata-profiling capabilities
        """
        return self.agent
