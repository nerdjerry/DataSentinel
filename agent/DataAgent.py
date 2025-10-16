from agent.SummarizerAgent import DataQualityIssue
from agent.tool.SnowflakeQueryToolFactory import SnowflakeQueryToolFactory
from autogen_agentchat.agents import AssistantAgent
from agent.model.ModelFactory import ModelFactory
from pydantic import BaseModel
import json
import os


class QueryExecution(BaseModel):
    """Result of a single query execution"""
    investigation_goal: str  # What was being investigated
    sql_query: str  # The actual SQL query executed
    row_count: int  # Number of rows returned
    sample_data: str  # Sample of the data (first 10 rows as string)
    summary: str  # Brief summary of findings

class DataAgentReport(BaseModel):
    """Complete report from DataAgent after executing plan tasks"""
    plan_goal: str  # The original goal from the plan
    tasks_executed: list[QueryExecution]  # All query executions
    next_steps: list[str]  # Recommended follow-up actions

class DataAgent:
    def __init__(self, name="DataAgent", system_message=None):
        """
        Initialize DataAgent.
        
        Args:
            name: Agent name
            system_message: Custom system prompt
            output_structured_report: If True, outputs DataAgentReport instead of plain text
        """
        self.snowflakeToolFactory = SnowflakeQueryToolFactory()
        self.model = ModelFactory.get_model()
        self.schema = self._get_schema()
        self.tools = [
            self.snowflakeToolFactory.create_query_tool(), 
            self.snowflakeToolFactory.create_table_info_tool(), 
            self.snowflakeToolFactory.create_list_tables_tool()
        ]
        
        self.agent = AssistantAgent(
            name=name,
            tools=self.tools,
            model_client=self.model,
            description="Data Investigation Agent for identifying data quality issues",
            system_message=system_message or self._system_message(),
            model_client_stream=False,  # Disable streaming for structured output
            reflect_on_tool_use=False,  # Disabled to prevent JSON parsing issues with structured output
            output_content_type=DataAgentReport
        )
    
    def _system_message(self) -> str:
        # Extract known data quality issues
        quality_notes = self.schema.get('data_quality_notes', [])
        quality_notes_text = "\n    ".join(quality_notes) if quality_notes else "None"
        
        base_description = f"""{{
        "role": "You are the Data Investigation Agent. Given a goal, generate and execute Snowflake SQL queries on RIDEBOOKING data to identify data quality issues.",

        "schema": {json.dumps(self.schema)},

        "capabilities": {
            "tools": ["list_tables", "table_info", "execute_query"],
            "actions": [
            "Generate ONE valid Snowflake SQL query per goal",
            "Execute the query using snowflake_sql",
            "Analyze query results for data quality issues",
            "Summarize findings with row counts, samples, and observations",
            "Use list_tables and table_info to explore schema as needed"
            ]
        },

        "query_best_practices": [
            "Always validate data types from schema before casting.",
            "Use TRY_CAST only for numeric or textual conversions — NEVER for DATE/TIME columns.",
            "For DATE or TIME columns, use CAST(column AS VARCHAR) or TO_VARCHAR(column) for safe conversion when needed for 'null' or blank checks.",
            "Ensure each SELECT or UNION branch returns the SAME number of columns with compatible data types.",
            "Avoid complex multi-UNION constructions; if needed, use separate SELECT statements for each check instead.",
            "Use LIMIT for sampling results.",
            "Include counts and percentages in results for quantitative context.",
            "Wrap column names with double quotes if they contain special characters or mixed case."
        ],

        "query_error_handling": [
            "If a multi-UNION approach causes syntax or column mismatch errors, fall back to executing SEPARATE simple queries per check (e.g., completeness, consistency).",
            "When checking completeness, explicitly convert DATE/TIME columns using CAST/TO_VARCHAR rather than TRY_CAST.",
            "When checking consistency between fields, run one simple SELECT per rule instead of combining multiple checks via UNION."
        ],

        "output_format": {
            "plan_goal": "Original goal from the plan",
            "tasks_executed": [
            {
                "investigation_goal": "What was being investigated",
                "sql_query": "Executed SQL query",
                "row_count": 0,
                "sample_data": "First 10 rows as formatted string",
                "summary": "Brief summary of findings (avoid SQL error messages; describe outcome or next step)"
            }
            ],
            "next_steps": ["Recommended follow-up actions"]
        },

        "known_data_quality_issues": [
            {quality_notes_text}
        ],

        "constraints": [
            "Generate and execute only ONE valid Snowflake SQL query per goal.",
            "If a goal involves multiple conditions, prefer multiple independent SELECTs instead of UNIONs.",
            "Always verify column data types from schema before using TRY_CAST or CAST.",
            "Never use TRY_CAST on DATE/TIME columns.",
            "Use only columns defined in the provided schema.",
            "Never output credentials, secrets, or PII.",
            "Always return valid JSON conforming to the DataAgentReport structure."
        ],

        "termination_condition": "After executing one SQL query and producing a complete DataAgentReport, stop execution."
        }}"""
        return base_description

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
        return self.agent