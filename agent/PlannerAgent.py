import json
import os
from pydantic import BaseModel
from autogen_agentchat.agents import AssistantAgent
from agent.model.ModelFactory import ModelFactory


class QueryTask(BaseModel):
    """A specific query task for DataAgent"""
    purpose: str  # Why this analysis is needed
    goal: str  # What DataAgent should investigate (DataAgent will determine the SQL)
    expected_insight: str  # What we expect to learn


class ProfilingTask(BaseModel):
    """A specific profiling task for DataProfilingAgent"""
    purpose: str  # Why this profiling is needed
    query_or_table: str  # SQL query or table name to profile
    expected_insight: str  # What we expect to learn


class DataQualityPlan(BaseModel):
    """Complete plan for data quality analysis"""
    goal: str  # The original data quality goal
    query_tasks: list[QueryTask]  # Tasks for DataAgent
    profiling_tasks: list[ProfilingTask]  # Tasks for DataProfilingAgent
    execution_sequence: list[str]  # Order of execution (e.g., ["query_1", "profile_1", "query_2"])
    success_criteria: list[str]  # How to know if the goal is achieved
    reasoning: str  # Why this plan was chosen


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
    
    def __init__(self, name="PlannerAgent", description=None):
        """
        Initialize the PlannerAgent.
        
        Args:
            name (str): Name of the agent
            description (str): Custom description/system prompt for the agent
        """
        self.model = ModelFactory.get_model()
        self.schema = self._load_schema()
        
        self.agent = AssistantAgent(
            name=name,
            model_client=self.model,
            description=description or self._default_description(),
            model_client_stream=True,
            reflect_on_tool_use=False,  # Planner doesn't use tools, it creates plans
            handoffs=[],  # Planner creates plans but doesn't execute
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
    
    def _default_description(self) -> str:
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
                "Generate profiling requests for DataProfilingAgent to analyze patterns",
                "Sequence tasks for optimal analysis flow",
                "Define clear success criteria for the goal"
            ],
        
            "planning_process": {{
                "step_1_understand_goal": "Parse the data quality goal and identify what needs to be validated or analyzed",
                "step_2_identify_columns": "Determine which columns are relevant based on the schema - ONLY use columns that exist in database_schema",
                "step_3_plan_investigation_goals": "Design high-level investigation goals for DataAgent (DataAgent will determine the SQL)",
                "step_4_plan_profiling": "Design profiling tasks to understand distributions, patterns, correlations",
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
                "purpose": "Why this investigation is needed",
                "goal": "What DataAgent should investigate (DataAgent will create the SQL query)",
                "expected_insight": "What we expect to learn from this investigation"
                }}
            ],
            "profiling_tasks": [
                {{
                "purpose": "Why this profiling is needed",
                "query_or_table": "SQL query or 'RIDEBOOKING' table name",
                "expected_insight": "What we expect to learn from profiling"
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
            
            "security_privacy": "Never expose credentials, secrets, or PII in plans or outputs."
        }}"""
    
    def get_agent(self):
        """Return the AutoGen agent instance"""
        return self.agent
    
    async def create_plan(self, data_quality_goal: str):
        """
        Create a comprehensive plan for achieving the data quality goal.
        
        Args:
            data_quality_goal: The user's data quality objective
            
        Returns:
            Result from the agent containing the plan
        """
        planning_task = f"""
        Create a comprehensive data quality analysis plan for this goal:

        GOAL: {data_quality_goal}

        Your plan must include:
        1. **Query Tasks**: High-level investigation goals for DataAgent (DataAgent will create the SQL queries)
        - Each task should have: purpose, goal (what to investigate), expected_insight
        - Example: {{"purpose": "Check data completeness", "goal": "Find how many bookings have null BOOKING_VALUE", "expected_insight": "Percentage of missing values"}}
        2. **Profiling Tasks**: Specific profiling requests for DataProfilingAgent (with purpose and focus areas)
        3. **Execution Sequence**: The order in which tasks should be executed
        4. **Success Criteria**: Measurable indicators that the goal has been achieved
        5. **Reasoning**: Why this plan will achieve the goal

        Be specific about WHAT to investigate, but let DataAgent determine HOW to query. Focus on goals, not SQL syntax.

        Output your plan in a clear, structured format that can be easily parsed and executed.
        """
        
        result = await self.agent.run(task=planning_task)
        return result
