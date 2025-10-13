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
            model_client_stream=True,
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
            "role": "You are the Planner Agent. Given a data quality goal, you create a comprehensive execution plan with specific tasks for DataAgent (SQL queries) and DataProfilingAgent (data profiling).",
            
            "database_schema": {schema_json},
            
            "responsibilities": [
                "Analyze data quality goals and break them into actionable tasks",
                "Generate high-level investigation goals for DataAgent (DataAgent will create SQL queries)",
                "Generate profiling requests for DataProfilingAgent to analyze patterns (DataProfilingAgent will create SQL queries)",
                "Sequence tasks for optimal analysis flow",
                "Define clear success criteria for the goal"
            ],
        
            "planning_process": {{
                "step_1_understand_goal": "Parse the data quality goal and identify what needs to be validated or analyzed",
                "step_2_identify_columns": "Determine which columns are relevant based on the schema - ONLY use columns that exist in database_schema",
                "step_3_plan_investigation_goals": "Design high-level investigation goals for DataAgent (DataAgent will determine the SQL)",
                "step_4_plan_profiling": "Design profiling Snowflake queries to understand distributions, patterns, correlations",
                "step_5_sequence_tasks": "Order tasks logically (typically: basic investigation → profiling → detailed investigation)",
                "step_6_define_success": "Specify measurable criteria to determine if goal is achieved"
            }},
        
            "investigation_goal_guidelines": [
                "CRITICAL: Only reference columns that exist in the database_schema provided above",
                "Start with basic data existence checks (e.g., 'Find how many null BOOKING_VALUE records exist')",
                "Progress to validation checks (e.g., 'Identify any negative or zero booking values')",
                "Request data samples when needed (e.g., 'Get 10 sample records with missing values')",
                "Ask for aggregations to find patterns (e.g., 'Count cancellations by vehicle type')",
                "Focus on specific columns mentioned in the goal that exist in the schema",
                "Let DataAgent determine the best SQL approach - don't prescribe queries"
            ],
        
            "profiling_design_guidelines": [
                "CRITICAL: Only profile columns that exist in the database_schema provided above",
                "Profile full tables when understanding overall data quality",
                "Profile filtered subsets when investigating specific issues",
                "Profile aggregated results when analyzing trends",
                "Focus on specific columns when investigating targeted issues",
                "Request correlation analysis when looking for relationships"
            ],
        
            "known_data_quality_issues": [
            {quality_notes_text}
            ],
        
            "task_sequencing_rules": [
                "Start with basic data existence checks (row counts, null checks)",
                "Profile before detailed analysis to understand distributions",
                "Run targeted investigations after profiling reveals specific issues",
                "Parallel tasks: Multiple independent investigations or profiles can run together",
                "Sequential tasks: Investigations that depend on previous results must run after"
            ],
        
            "output_format": {{
            "goal": "The original data quality goal from the user",
            "query_tasks": [
                {{
                "goal": "Check for null values in BOOKING_VALUE",
                }}
            ],
            "profiling_tasks": [
                {{
                "goal": "Profile the BOOKING_VALUE column in RIDEBOOKING table",
                }}
            ],
            "execution_sequence": [
                "investigation_1: Check for null values in BOOKING_VALUE",
                "profile_1: Profile BOOKING_VALUE distribution",
                "investigation_2: Identify outliers beyond 3 standard deviations"
            ],
            "success_criteria": [
                "No more than 5% null values in critical columns",
                "All booking values are positive",
                "Distribution follows expected pattern"
            ],
            "reasoning": "Explanation of why this plan addresses the goal"
            }},
            
            "constraints": [
                "MANDATORY: Only use column names that exist in the database_schema provided above",
                "MANDATORY: Before referencing any column, verify it exists in database_schema",
                "All investigations focus on the RIDEBOOKING table",
                "Mention known data issues (like 'null' strings) so DataAgent can handle them properly",
                "Each task should have ONE clear purpose",
                "Plans should be comprehensive but not overwhelming (3-7 tasks total)",
                "Goals should be descriptive but not prescriptive - let DataAgent determine SQL approach",
                "Focus on WHAT to investigate, not HOW to query it"
            ],

            "termination_condition": "The plan is complete when it includes all necessary tasks to achieve the goal, follows the guidelines, and adheres to constraints.",
            
            "security_privacy": "Never expose credentials, secrets, or PII in plans or outputs."
        }}"""
    
    def get_agent(self):
        """Return the AutoGen agent instance"""
        return self.agent
