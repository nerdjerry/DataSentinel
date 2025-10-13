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
            model_client_stream=True,
            reflect_on_tool_use=True,
            output_content_type=DataAgentReport
        )
    
    def _system_message(self) -> str:
        # Extract known data quality issues
        quality_notes = self.schema.get('data_quality_notes', [])
        quality_notes_text = "\n    ".join(quality_notes) if quality_notes else "None"
        
        base_description = f"""{{
            "role": "You are a Data Investigation Agent with direct access to RIDEBOOKING data in Snowflake. You execute investigation goals from the PlannerAgent and identify data quality issues.",
    
            "schema": {json.dumps(self.schema, indent=2)},
    
            "capabilities": {{
                "tools": {{
                    "list_tables": "Discover available tables",
                    "table_info": "Fetch schema details of a table",
                    "snowflake_sql": "Execute SQL queries and return results"
                }},
                "investigation": [
                    "Translate investigation goals into appropriate SQL queries",
                    "Execute queries and analyze results",
                    "Identify data quality issues (missing values, invalid data, outliers, inconsistencies)",
                    "Provide evidence with counts, samples, and statistics",
                    "Assess severity and impact of issues found"
                ]
            }},
    
            "known_data_issues": [
                {quality_notes_text}
            ],
    
            "query_best_practices": [
                "Use TRY_CAST for BOOKING_VALUE and RIDE_DISTANCE to handle 'null' strings",
                "Include both NULL checks and string 'null' checks for problematic columns",
                "Use LIMIT for sampling unless full count is needed",
                "Provide clear context with each query result",
                "Calculate percentages when reporting issues (e.g., % missing values)"
            ]}}"""

        
        base_description += """,
    
            "output_format": {
                "plan_goal": "The original goal from the plan",
                "tasks_executed": [
                    {
                        "task_purpose": "Why this query was run",
                        "investigation_goal": "What was being investigated",
                        "sql_query": "The actual SQL executed",
                        "row_count": "Number of rows returned",
                        "sample_data": "First 10 rows as formatted string",
                        "summary": "Brief summary of findings"
                    }
                ],
            "next_steps": ["Recommended follow-up actions"]
            },
    
            "issue_detection_guidelines": {
                "missing_values": {
                    "threshold": "Flag if > 5% missing in critical columns",
                    "severity": "Critical if > 20%, High if > 10%, Medium if > 5%",
                    "check": "COUNT NULL values AND string 'null' values"
                },
                "invalid_data": {
                    "examples": "Negative booking values, zero distances, future dates",
                    "severity": "Critical for revenue/distance fields",
                    "check": "Range validation, format validation"
                },
                "outliers": {
                    "detection": "Values > 3 standard deviations from mean",
                    "severity": "Medium unless affecting critical calculations",
                    "check": "Statistical analysis with percentiles"
                },
                "inconsistencies": {
                    "examples": "Completed rides with null values, cancelled rides with booking values",
                    "severity": "Varies based on business logic",
                    "check": "Cross-field validation"
                }
            }"""
        
        return base_description + "\n}"

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