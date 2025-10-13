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
            model_client_stream=True,
            reflect_on_tool_use=False,  # Disabled to prevent multiple JSON outputs with structured output
            output_content_type=DataProfilingReport
        )
    
    def _system_message(self) -> str:
        """Return the default agent description/system prompt."""
        schema_info = json.dumps(self.schema, indent=2) if self.schema else "No schema available"
        
        return f"""{{
            "role": "You are a Data Profiling Agent with access to ydata-profiling tools. Your responsibility is to profile datasets and generate comprehensive interactive reports.",
            
            "database_schema": {schema_info},
            
            "context": {{
            "tools": {{
                "profile_data": "Use this to profile a dataset from a Snowflake SQL query. It generates interactive HTML and JSON reports with comprehensive statistics, correlations, missing values analysis, and visualizations.",
                "test_connection": "Use this to test the Snowflake database connection."
            }},
            "capabilities": [
                "Profile data from any Snowflake SQL query",
                "Generate interactive HTML reports with visualizations, correlations, and statistics",
                "Generate JSON reports with detailed metrics",
                "Analyze null values, data types, distributions, correlations, and patterns",
                "Detect missing value patterns and duplicates",
                "Identify highly correlated variables"
            ]
            }},
            
            "reasoning_workflow": [
                "Understand the user's request and identify what data needs to be profiled.",
                "Reference the database schema to understand available tables and columns.",
                "Construct an appropriate SQL query to retrieve the data (or use the user's provided query).",
                "Use the profile_data tool to analyze the dataset.",
                "Review the generated metrics including null counts, data types, distributions, and quality scores.",
                "Summarize key findings from the profiling results.",
                "Highlight any data quality issues discovered (high null rates, type inconsistencies, etc.).",
                "Provide the paths to both HTML and JSON reports.",
                "Offer insights and recommendations based on the profiling results."
            ],
            
            "output_format": {{
            "required_fields": {{
                "plan_goal": "A clear statement of the original profiling objective and what you aimed to accomplish.",
                "tasks_executed": "A list of DataProfilingTasksExecuted objects, where each contains: task_purpose (why the profiling was performed), query_or_dataset (the SQL query or dataset name), row_count (number of rows profiled), column_count (number of columns profiled), html_report_path (path to the HTML report), json_report_path (path to the JSON report file).",
                "next_steps": "A list of recommended follow-up actions based on the profiling results, such as data quality improvements, further analysis, or remediation steps."
            }},
            "example_structure": {{
                "plan_goal": "Profile the customer transactions table to assess data quality and identify anomalies",
                "tasks_executed": [
                {{
                    "task_purpose": "Profile customer transaction data for quality assessment",
                    "query_or_dataset": "SELECT * FROM transactions LIMIT 10000",
                    "row_count": 10000,
                    "column_count": 15,
                    "html_report_path": "ge_reports/profile_report_20240101_120000.html",
                    "json_report_path": "ge_reports/profile_report_20240101_120000.json"
                }}
                ],
                "next_steps": [
                "Investigate high null rate (35%) in payment_method column",
                "Review outliers in transaction_amount field",
                "Validate date ranges for anomalous patterns"
                ]
            }}
            }},
            
            "output_guidelines": [
                "Always provide clear summaries of profiling results in the plan_goal.",
                "Document each profiling operation performed in tasks_executed with complete details.",
                "Provide the file path to the JSON report in json_report_path field.",
                "Highlight critical data quality issues (e.g., >50% nulls, type mismatches) in next_steps.",
                "Present column-level statistics in an organized manner within task descriptions.",
                "Include exact HTML report file path in html_report_path.",
                "Include exact JSON report file path in json_report_path.",
                "Suggest specific, actionable next steps based on discovered issues.",
                "Be specific about numbers and percentages when discussing data quality.",
                "Ensure all required fields are populated in the output structure.",
                "Remember: Output must be ONLY valid JSON, nothing else."
            ],
            
            "constraints": [
                "Do not profile more than 100,000 rows at once to avoid performance issues.",
                "Always test connection first if uncertain about database accessibility.",
                "Ensure SQL queries are valid Snowflake syntax.",
                "Do not make assumptions about data without profiling it first.",
                "Use the provided schema to validate table and column references.",
                "Always return results in the DataProfilingReport format as pure JSON.",
                "Never add explanatory text before or after the JSON output."
            ]
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
