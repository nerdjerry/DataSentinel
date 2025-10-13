import json
import os
from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent
from agent.model.ModelFactory import ModelFactory


class QueryTask(BaseModel):
    """A specific query task for DataAgent"""
    goal: str  # What DataAgent should investigate (DataAgent will determine the SQL)


class ProfilingTask(BaseModel):
    """A specific profiling task for DataProfilingAgent"""
    goal: str  # What to profile (DataProfilingAgent will determine the SQL or table)


class DataQualityPlan(BaseModel):
    """Complete plan for data quality analysis"""
    goal: str  # The original data quality goal
    query_tasks: list[QueryTask]  # Tasks for DataAgent
    profiling_tasks: list[ProfilingTask]  # Tasks for DataProfilingAgent
    execution_sequence: list[str]  # Order of execution (e.g., ["query_1", "profile_1", "query_2"])
    success_criteria: list[str]  # How to know if the goal is achieved


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
        self.model = ModelFactory.get_model()
        self.schema = self._load_schema()
        
        self.agent = AssistantAgent(
            name=name,
            model_client=self.model,
            description="Planner Agent for Data Quality Analysis",
            system_message=system_message or self._system_message(),
            model_client_stream=False,  # Disable streaming for structured output
            reflect_on_tool_use=False,  # Planner doesn't use tools, it creates plans
            output_content_type=DataQualityPlan
        )
    
    def _load_schema(self) -> dict:
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
    
    def _system_message(self) -> str:
        """Return the default agent description/system prompt."""
        
        # Extract known data quality issues
        quality_notes = self.schema.get('data_quality_notes', [])
        quality_notes_text = "\n    ".join(quality_notes) if quality_notes else "None"
        
        schema_json = json.dumps(self.schema, indent=2) if self.schema else "{}"
        
        return f"""{{
            "role": "You are the Planner Agent. Given a data quality goal and database_schema, create a structured execution plan with tasks for DataAgent (SQL investigations) and DataProfilingAgent (profiling analysis).",

            "database_schema": {schema_json},

            "responsibilities": [
                "Break down the data quality goal into actionable tasks using only columns from database_schema",
                "Define 3–4 investigation goals for DataAgent and 1 profiling goal for DataProfilingAgent",
                "Sequence tasks logically and define measurable success criteria"
            ],

            "query_tasks": [
                {{ "goal": "Check for null values in critical columns like BOOKING_VALUE" }},
                {{ "goal": "Identify negative or zero BOOKING_VALUE records" }},
                {{ "goal": "Find duplicate BOOKING_ID entries" }},
                {{ "goal": "Detect inconsistent date ranges between BOOKING_DATE and TRAVEL_DATE" }}
            ],

            "profiling_tasks": [
                {{ "goal": "Profile the BOOKING_VALUE column to understand its distribution and outliers" }}
            ],

            "constraints": [
                "Use only valid columns from database_schema",
                "Focus on what to analyze, not how to query",
                "Maintain privacy—never expose credentials or sensitive data"
            ],

            "termination_condition": "The plan is complete when it includes required DataAgent and profiling goals, follows schema rules, and meets success criteria."
        }}"""
    
    def get_agent(self):
        """Return the AutoGen agent instance"""
        return self.agent
