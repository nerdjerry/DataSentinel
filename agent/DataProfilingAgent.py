import os
import json
from agent.tool.SnowflakeDataProfilingToolFactory import SnowflakeDataProfilingToolFactory
from autogen_agentchat.agents import AssistantAgent
from agent.model.ModelFactory import ModelFactory


class DataProfilingAgent:
    """
    A specialized agent for data profiling and quality assessment using ydata-profiling.
    
    This agent can:
    - Profile datasets from Snowflake queries
    - Generate comprehensive interactive HTML and JSON reports
    - Analyze data quality metrics, correlations, and distributions
    - Provide insights on data patterns and anomalies
    """
    
    def __init__(self, name="DataProfilingAgent", description=None, reports_dir="ge_reports"):
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
            self.profiling_tool_factory.create_profile_tool(),
            self.profiling_tool_factory.create_connection_test_tool()
        ]
        self.schema = self._get_schema()
        self.agent = AssistantAgent(
            name=name,
            tools=self.tools,
            model_client=self.model,
            description=description or self._default_description(),
            model_client_stream=True,
            reflect_on_tool_use=True
        )
    
    def _default_description(self) -> str:
        """Return the default agent description/system prompt."""
        schema_info = json.dumps(self.schema, indent=2) if self.schema else "No schema available"
        
        return f"""{{
            "role": "You are a Data Profiling Agent with access to Snowflake databases and ydata-profiling tools. Your responsibility is to profile datasets, analyze data quality, and generate comprehensive interactive reports.",
            
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
            "Provide the paths to the generated HTML and JSON reports.",
            "Offer insights and recommendations based on the profiling results."
            ],
            
            "output_guidelines": [
            "Always provide clear summaries of profiling results.",
            "Highlight critical data quality issues (e.g., >50% nulls, type mismatches).",
            "Present column-level statistics in an organized manner.",
            "Include report file paths for user reference.",
            "Suggest next steps or remediation actions when issues are found.",
            "Be specific about numbers and percentages when discussing data quality."
            ],
            
            "constraints": [
            "Do not profile more than 100,000 rows at once to avoid performance issues.",
            "Always test connection first if uncertain about database accessibility.",
            "Ensure SQL queries are valid Snowflake syntax.",
            "Do not make assumptions about data without profiling it first.",
            "Use the provided schema to validate table and column references."
            ]
        }}"""
    
    def _get_schema(self):
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'metadata', 'schema.json')
        with open(schema_path, 'r') as f:
            return json.load(f)

    def get_agent(self):
        """
        Get the configured AutoGen agent.
        
        Returns:
            AssistantAgent: Configured agent with ydata-profiling capabilities
        """
        return self.agent
