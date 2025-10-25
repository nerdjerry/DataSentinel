"""
Orchestrator for Data Quality Analysis Workflow

This module orchestrates a multi-agent workflow for comprehensive data quality analysis:
1. PlannerAgent: Breaks down the goal into specific tasks
2. DataAgent: Executes SQL queries to investigate data
3. DataProfilingAgent: Generates statistical profiles and reports
4. SummarizerAgent: Synthesizes findings into actionable insights
5. ReportAgent: Creates a professional HTML report

The orchestrator uses AutoGen's team framework to coordinate agent interactions.
"""

import asyncio
from typing import Optional, Dict, Any
from pathlib import Path
import json

from autogen_agentchat.teams import RoundRobinGroupChat, Swarm
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import StructuredMessage

from agent.PlannerAgent import PlannerAgent, DataQualityPlan
from agent.DataAgent import DataAgent, DataAgentReport
from agent.DataProfilingAgent import DataProfilingAgent, DataProfilingReport
from agent.SummarizerAgent import SummarizerAgent, DataQualityAgentReport
from agent.ReportAgent import ReportAgent, ReportResponse


class Orchestrator:
    """
    Orchestrates a multi-agent data quality analysis workflow.
    
    The orchestrator coordinates agents in a sequential workflow:
    1. Planning Phase: PlannerAgent creates execution plan
    2. Investigation Phase: DataAgent and DataProfilingAgent gather data
    3. Analysis Phase: SummarizerAgent synthesizes findings
    4. Reporting Phase: ReportAgent generates final HTML report
    
    Attributes:
        planner_agent: Agent for creating analysis plans
        data_agent: Agent for executing SQL queries
        profiling_agent: Agent for data profiling
        summarizer_agent: Agent for synthesizing findings
        report_agent: Agent for generating reports
        reports_dir: Directory for storing generated reports
    """
    
    def __init__(
        self,
        reports_dir: str = "ge_reports",
        max_rounds: int = 7,
        enable_console_output: bool = True
    ):
        """
        Initialize the Orchestrator with all required agents.
        
        Args:
            reports_dir: Directory for storing generated reports
            max_rounds: Maximum number of conversation rounds
            enable_console_output: Whether to print progress to console
        """
        # TODO: Implement the initialization
        # 1. Store the parameters as instance variables
        # 2. Create the reports directory if it doesn't exist
        # 3. Initialize all agents using their respective classes
        # 4. Print success message
        raise NotImplementedError("Students need to implement __init__ method")
    
    async def run_analysis(self, goal: str) -> Dict[str, Any]:
        """
        Run complete data quality analysis workflow.
        
        This method orchestrates the entire workflow:
        1. PlannerAgent creates a plan
        2. DataAgent + DataProfilingAgent execute the plan
        3. SummarizerAgent analyzes results
        4. ReportAgent generates final report
        
        Args:
            goal: Data quality goal/question to analyze
            
        Returns:
            Dictionary containing:
                - plan: The execution plan from PlannerAgent
                - investigation_results: Results from DataAgent
                - profiling_results: Results from DataProfilingAgent
                - analysis: Summary and findings from SummarizerAgent
                - report: Final HTML report from ReportAgent
                - success: Whether the workflow completed successfully
        """
        # TODO: Implement the main workflow orchestration
        # 1. Initialize results dictionary with all required keys
        # 2. Call each phase method in sequence:
        #    - _run_planning_phase
        #    - _run_investigation_phase
        #    - _run_analysis_phase
        #    - _run_reporting_phase
        # 3. Store results from each phase in the results dictionary
        # 4. Set success=True if all phases complete
        # 5. Save results using _save_results method
        # 6. Handle exceptions and store error information
        raise NotImplementedError("Students need to implement run_analysis method")
    
    async def _run_planning_phase(self, goal: str) -> Optional[DataQualityPlan]:
        """
        Phase 1: Create execution plan using PlannerAgent.
        
        Args:
            goal: Data quality goal to plan for
            
        Returns:
            DataQualityPlan object or None if planning failed
        """
        # TODO: Implement the planning phase
        # 1. Create a MaxMessageTermination with max_messages=3
        # 2. Create a RoundRobinGroupChat with planner_agent
        # 3. Include StructuredMessage[DataQualityPlan] in custom_message_types
        # 4. Create task string asking to plan for the goal
        # 5. Run the team (use Console if enable_console_output is True)
        # 6. Extract DataQualityPlan from the response messages
        # 7. Return the plan or None if not found
        raise NotImplementedError("Students need to implement _run_planning_phase method")
    
    async def _run_investigation_phase(
        self,
        plan: Optional[DataQualityPlan]
    ) -> tuple[Optional[DataAgentReport], Optional[DataProfilingReport]]:
        """
        Phase 2: Execute investigation and profiling tasks concurrently.
        
        Each task runs on its own async task (thread-like execution) for parallel processing.
        
        Args:
            plan: Execution plan from PlannerAgent
            
        Returns:
            Tuple of (DataAgentReport, DataProfilingReport) or (None, None) if failed
        """
        # TODO: Implement the investigation phase with concurrent execution
        # 1. Return (None, None) if no plan provided
        # 2. Create helper function execute_query_task for running DataAgent
        # 3. Create helper function execute_profiling_task for DataProfilingAgent
        # 4. Use asyncio.gather to run all query tasks concurrently
        # 5. Use asyncio.gather to run all profiling tasks concurrently
        # 6. Combine results from all tasks
        # 7. Return tuple of combined results
        # Hint: Each helper should create its own RoundRobinGroupChat with appropriate agent
        raise NotImplementedError("Students need to implement _run_investigation_phase method")
    
    async def _run_analysis_phase(
        self,
        goal: str,
        plan: Optional[DataQualityPlan],
        investigation_results: Optional[DataAgentReport],
        profiling_results: Optional[DataProfilingReport]
    ) -> Optional[DataQualityAgentReport]:
        """
        Phase 3: Synthesize findings using SummarizerAgent.
        
        Args:
            goal: Original data quality goal
            plan: Execution plan
            investigation_results: Results from DataAgent
            profiling_results: Results from DataProfilingAgent
            
        Returns:
            DataQualityAgentReport or None if analysis failed
        """
        # TODO: Implement the analysis phase
        # 1. Create analysis task using _create_analysis_task helper
        # 2. Create MaxMessageTermination with max_messages=5
        # 3. Create RoundRobinGroupChat with summarizer_agent
        # 4. Include StructuredMessage[DataQualityAgentReport] in custom_message_types
        # 5. Run the team with the task
        # 6. Extract DataQualityAgentReport from response
        # 7. Return the report or None
        raise NotImplementedError("Students need to implement _run_analysis_phase method")
    
    async def _run_reporting_phase(
        self,
        goal: str,
        plan: Optional[DataQualityPlan],
        investigation_results: Optional[DataAgentReport],
        profiling_results: Optional[DataProfilingReport],
        analysis: Optional[DataQualityAgentReport]
    ) -> Optional[str]:
        """
        Phase 4: Generate final HTML report using ReportAgent.
        
        Args:
            goal: Original data quality goal
            plan: Execution plan
            investigation_results: Results from DataAgent
            profiling_results: Results from DataProfilingAgent
            analysis: Analysis from SummarizerAgent
            
        Returns:
            HTML report string or None if reporting failed
        """
        # TODO: Implement the reporting phase
        # 1. Create reporting task using _create_reporting_task helper
        # 2. Create MaxMessageTermination with max_messages=3
        # 3. Create RoundRobinGroupChat with report_agent
        # 4. Include StructuredMessage[ReportResponse] in custom_message_types
        # 5. Run the team with the task
        # 6. Extract ReportResponse and get HTML content
        # 7. Save HTML using _save_html_report helper
        # 8. Return the HTML string or None
        raise NotImplementedError("Students need to implement _run_reporting_phase method")
    
    def _create_analysis_task(
        self,
        goal: str,
        plan: Optional[DataQualityPlan],
        investigation_results: Optional[list],
        profiling_results: Optional[list]
    ) -> str:
        """Create task description for analysis phase."""
        # TODO: Implement task creation for analysis
        # 1. Start with the original goal
        # 2. If investigation_results exist:
        #    - Summarize number of queries executed
        #    - Include details of each query execution
        # 3. If profiling_results exist:
        #    - Summarize number of profiles generated
        #    - Include details of each profiling task
        # 4. Add instructions for the analysis:
        #    - Request comprehensive summary
        #    - Ask for identified issues with severity
        #    - Request prioritized recommendations
        #    - Ask for follow-up queries if needed
        # 5. Return the complete task string
        raise NotImplementedError("Students need to implement _create_analysis_task method")
    
    def _create_reporting_task(
        self,
        goal: str,
        plan: Optional[DataQualityPlan],
        investigation_results: Optional[list],
        profiling_results: Optional[list],
        analysis: Optional[DataQualityAgentReport]
    ) -> str:
        """Create task description for reporting phase."""
        # TODO: Implement task creation for reporting
        # 1. Start with the original goal
        # 2. If analysis exists:
        #    - Include executive summary
        #    - List all identified issues with severity
        #    - Include all recommendations
        # 3. If investigation_results exist:
        #    - Summarize total queries executed
        # 4. If profiling_results exist:
        #    - Summarize total profiles generated
        #    - List available profiling reports with paths
        # 5. Add instruction to generate HTML report
        # 6. Add instruction to end with REPORT_COMPLETE
        # 7. Return the complete task string
        raise NotImplementedError("Students need to implement _create_reporting_task method")
    
    def _save_html_report(self, html: str, goal: str) -> Path:
        """Save HTML report to file."""
        # TODO: Implement HTML report saving
        # 1. Import datetime and create timestamp
        # 2. Create safe filename from goal (remove special chars)
        # 3. Limit filename length to reasonable size
        # 4. Create full filename with timestamp
        # 5. Create full path in reports_dir
        # 6. Write HTML content to file
        # 7. Return the Path object
        raise NotImplementedError("Students need to implement _save_html_report method")
    
    def _save_results(self, results: Dict[str, Any]) -> None:
        """Save complete workflow results to JSON file."""
        # TODO: Implement results saving to JSON
        # 1. Import datetime and create timestamp
        # 2. Create json_results dictionary with basic fields
        # 3. For each result that exists:
        #    - Convert Pydantic models using model_dump()
        #    - Handle lists of Pydantic models
        #    - Fall back to str() for non-Pydantic objects
        # 4. Create filename with timestamp
        # 5. Save json_results to file using json.dump
        # 6. Print success message with file path
        raise NotImplementedError("Students need to implement _save_results method")
