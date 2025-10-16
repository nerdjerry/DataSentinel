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
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        self.max_rounds = max_rounds
        self.enable_console_output = enable_console_output
        
        # Initialize all agents
        print("🔧 Initializing agents...")
        self.planner_agent = PlannerAgent().get_agent()
        self.data_agent = DataAgent().get_agent()
        self.profiling_agent = DataProfilingAgent(reports_dir=reports_dir).get_agent()
        self.summarizer_agent = SummarizerAgent().get_agent()
        self.report_agent = ReportAgent().get_agent()
        
        print("✅ All agents initialized successfully")
    
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
        results = {
            "goal": goal,
            "plan": None,
            "investigation_results": None,
            "profiling_results": None,
            "analysis": None,
            "report": None,
            "success": False
        }
        
        try:
            print(f"\n{'='*80}")
            print(f"🎯 Starting Data Quality Analysis")
            print(f"{'='*80}")
            print(f"Goal: {goal}\n")
            
            # Phase 1: Planning
            print("📋 Phase 1: Creating Execution Plan...")
            plan = await self._run_planning_phase(goal)
            results["plan"] = plan
            
            # Phase 2: Investigation & Profiling
            print("\n🔍 Phase 2: Executing Investigation and Profiling...")
            investigation_results, profiling_results = await self._run_investigation_phase(plan)
            results["investigation_results"] = investigation_results
            results["profiling_results"] = profiling_results
            
            # Phase 3: Analysis & Summarization
            print("\n📊 Phase 3: Analyzing and Summarizing Findings...")
            analysis = await self._run_analysis_phase(
                goal, plan, investigation_results, profiling_results
            )
            results["analysis"] = analysis
            
            # Phase 4: Report Generation
            print("\n📄 Phase 4: Generating Final Report...")
            report = await self._run_reporting_phase(
                goal, plan, investigation_results, profiling_results, analysis
            )
            results["report"] = report
            
            results["success"] = True
            
            print(f"\n{'='*80}")
            print("✅ Data Quality Analysis Complete!")
            print(f"{'='*80}\n")
            
            # Save results to file
            self._save_results(results)
            
            return results
            
        except Exception as e:
            print(f"\n❌ Error during analysis: {str(e)}")
            results["error"] = str(e)
            import traceback
            results["traceback"] = traceback.format_exc()
            return results
    
    async def _run_planning_phase(self, goal: str) -> Optional[DataQualityPlan]:
        """
        Phase 1: Create execution plan using PlannerAgent.
        
        Args:
            goal: Data quality goal to plan for
            
        Returns:
            DataQualityPlan object or None if planning failed
        """
        try:
            
            # Create a single-agent team for planning
            termination = MaxMessageTermination(max_messages=3)
            team = RoundRobinGroupChat(
                [self.planner_agent],
                termination_condition=termination,
                custom_message_types=[StructuredMessage[DataQualityPlan]]
            )
            
            # Run planning
            task = f"Create a comprehensive execution plan for this data quality goal: {goal}"
            
            if self.enable_console_output:
                result = await Console(team.run_stream(task=task))
            else:
                result = await team.run(task=task)
            
            # Extract the plan from the last message
            for message in reversed(result.messages):
                if hasattr(message, 'content') and isinstance(message.content, DataQualityPlan):
                    print(f"✅ Plan created: {len(message.content.query_tasks)} query tasks, "
                          f"{len(message.content.profiling_tasks)} profiling tasks")
                    return message.content
            
            print("⚠️ Warning: Could not extract plan from planner response")
            return None
            
        except Exception as e:
            print(f"❌ Planning phase failed: {str(e)}")
            raise
    
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
        if not plan:
            print("⚠️ Skipping investigation phase - no plan available")
            return None, None
        
        try:
            # Helper function to execute a single query task
            async def execute_query_task(query_task):
                print(f"    🔄 Starting query task: {query_task.goal}")
                
                # Create task for this specific query
                query_task_str = f"""Execute this specific data quality query task:
                                Goal: {query_task.goal}
                                """
                
                # Run DataAgent for this task
                termination = MaxMessageTermination(max_messages=5)
                team = RoundRobinGroupChat(
                    [self.data_agent],
                    termination_condition=termination,
                    custom_message_types=[StructuredMessage[DataAgentReport]]
                )
                
                if self.enable_console_output:
                    result = await Console(team.run_stream(task=query_task_str))
                else:
                    result = await team.run(task=query_task_str)
                
                # Extract and return result
                for message in reversed(result.messages):
                    if hasattr(message, 'content') and isinstance(message.content, DataAgentReport):
                        print(f"    ✅ Completed query task: {query_task.goal}")
                        return message.content
                
                print(f"    ⚠️ No result for query task: {query_task.goal}")
                return None
            
            # Helper function to execute a single profiling task
            async def execute_profiling_task(profiling_task):
                print(f"    🔄 Starting profiling task: {profiling_task.goal}")
                
                # Create task for this specific profiling
                profiling_task_str = f"""Execute this specific data profiling task:
                                    Goal: {profiling_task.goal}
                                    """
                
                # Run DataProfilingAgent for this task
                termination = MaxMessageTermination(max_messages=5)
                team = RoundRobinGroupChat(
                    [self.profiling_agent],
                    termination_condition=termination,
                    custom_message_types=[StructuredMessage[DataProfilingReport]]
                )
                
                if self.enable_console_output:
                    result = await Console(team.run_stream(task=profiling_task_str))
                else:
                    result = await team.run(task=profiling_task_str)
                
                # Extract and return result
                for message in reversed(result.messages):
                    if hasattr(message, 'content') and isinstance(message.content, DataProfilingReport):
                        print(f"    ✅ Completed profiling task: {profiling_task.goal}")
                        return message.content
                
                print(f"    ⚠️ No result for profiling task: {profiling_task.goal}")
                return None
            
            # Execute all query tasks concurrently
            all_investigation_results = []
            if plan.query_tasks:
                print(f"  📊 Executing {len(plan.query_tasks)} query tasks concurrently...")
                query_coroutines = [execute_query_task(task) for task in plan.query_tasks]
                query_results = await asyncio.gather(*query_coroutines, return_exceptions=True)
                
                # Filter out None values and exceptions
                for result in query_results:
                    if isinstance(result, Exception):
                        print(f"    ❌ Query task failed with error: {str(result)}")
                    elif result is not None:
                        all_investigation_results.append(result)
            
            # Execute all profiling tasks concurrently
            all_profiling_results = []
            if plan.profiling_tasks:
                print(f"  📈 Executing {len(plan.profiling_tasks)} profiling tasks concurrently...")
                profiling_coroutines = [execute_profiling_task(task) for task in plan.profiling_tasks]
                profiling_results = await asyncio.gather(*profiling_coroutines, return_exceptions=True)
                
                # Filter out None values and exceptions
                for result in profiling_results:
                    if isinstance(result, Exception):
                        print(f"    ❌ Profiling task failed with error: {str(result)}")
                    elif result is not None:
                        all_profiling_results.append(result)
            
            # Combine all results
            combined_investigation = all_investigation_results if all_investigation_results else None
            combined_profiling = all_profiling_results if all_profiling_results else None
            
            print(f"  ✅ Investigation phase completed: {len(all_investigation_results)} query results, {len(all_profiling_results)} profiling results")
            
            return combined_investigation, combined_profiling
            
        except Exception as e:
            print(f"❌ Investigation phase failed: {str(e)}")
            raise
    
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
        try:
            # Create analysis task with results from investigation phase
            task = self._create_analysis_task(goal, plan, investigation_results, profiling_results)
            
            # Create single-agent team for summarization
            termination = MaxMessageTermination(max_messages=5)
            team = RoundRobinGroupChat(
                [self.summarizer_agent],
                termination_condition=termination,
                custom_message_types=[StructuredMessage[DataQualityAgentReport]]
            )
            
            # Run analysis
            if self.enable_console_output:
                result = await Console(team.run_stream(task=task))
            else:
                result = await team.run(task=task)
            
            # Extract analysis
            for message in reversed(result.messages):
                if hasattr(message, 'content') and isinstance(message.content, DataQualityAgentReport):
                    print(f"✅ Analysis completed: {len(message.content.issues)} issues identified")
                    return message.content
            
            print("⚠️ Warning: Could not extract analysis from summarizer response")
            return None
            
        except Exception as e:
            print(f"❌ Analysis phase failed: {str(e)}")
            raise
    
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
        try:
            # Create task with all context
            task = self._create_reporting_task(goal, plan, investigation_results, profiling_results, analysis)
            
            # Create single-agent team for reporting
            termination = MaxMessageTermination(max_messages=3)
            team = RoundRobinGroupChat(
                [self.report_agent],
                termination_condition=termination,
                custom_message_types=[StructuredMessage[ReportResponse]]
            )
            
            # Run reporting
            if self.enable_console_output:
                result = await Console(team.run_stream(task=task))
            else:
                result = await team.run(task=task)
            
            # Extract report
            for message in reversed(result.messages):
                if hasattr(message, 'content') and isinstance(message.content, ReportResponse):
                    html_report = message.content.html
                    if html_report:
                        # Save HTML report to file
                        report_path = self._save_html_report(html_report, goal)
                        print(f"✅ Report generated and saved to: {report_path}")
                        return html_report
            
            print("⚠️ Warning: Could not extract report from report agent response")
            return None
            
        except Exception as e:
            print(f"❌ Reporting phase failed: {str(e)}")
            raise
    
    def _create_analysis_task(
        self,
        goal: str,
        plan: Optional[DataQualityPlan],
        investigation_results: Optional[list],
        profiling_results: Optional[list]
    ) -> str:
        """Create task description for analysis phase."""
        task = f"""Analyze the following data quality investigation results and provide comprehensive insights:

        Original Goal: {goal}

        """
        if investigation_results:
            task += f"Investigation Results from DataAgent:\n"
            total_queries = sum(len(report.tasks_executed) for report in investigation_results)
            task += f"- {total_queries} queries executed across {len(investigation_results)} tasks\n"
            
            query_num = 1
            for report in investigation_results:
                for execution in report.tasks_executed:
                    task += f"\nQuery {query_num}: {execution.investigation_goal}\n"
                    task += f"  SQL: {execution.sql_query}\n"
                    task += f"  Rows: {execution.row_count}\n"
                    task += f"  Summary: {execution.summary}\n"
                    query_num += 1
        
        if profiling_results:
            task += f"\nProfiling Results from DataProfilingAgent:\n"
            total_profiles = sum(len(report.tasks_executed) for report in profiling_results)
            task += f"- {total_profiles} profiles generated across {len(profiling_results)} tasks\n"
            
            profile_num = 1
            for report in profiling_results:
                for prof in report.tasks_executed:
                    task += f"\nProfile {profile_num}: {prof.task_purpose}\n"
                    task += f"  Dataset: {prof.query_or_dataset}\n"
                    task += f"  Rows: {prof.row_count}, Columns: {prof.column_count}\n"
                    task += f"  JSON Report: {prof.json_report_path}\n"
                    profile_num += 1
        
        task += "\n\nPlease analyze these results and provide:\n"
        task += "1. A comprehensive summary of data quality findings\n"
        task += "2. List of identified issues with severity levels\n"
        task += "3. Prioritized recommendations for remediation\n"
        task += "4. Any follow-up queries needed for deeper investigation\n"
        
        return task
    
    def _create_reporting_task(
        self,
        goal: str,
        plan: Optional[DataQualityPlan],
        investigation_results: Optional[list],
        profiling_results: Optional[list],
        analysis: Optional[DataQualityAgentReport]
    ) -> str:
        """Create task description for reporting phase."""
        task = f"""Generate a professional HTML report for the following data quality analysis:

        Goal: {goal}

        """
        if analysis:
            task += f"Executive Summary:\n{analysis.summary}\n\n"
            
            if analysis.issues:
                task += "Identified Issues:\n"
                for i, issue in enumerate(analysis.issues, 1):
                    task += f"{i}. [{issue.severity}] {issue.type}\n"
                    task += f"   {issue.evidence_description}\n\n"
            
            if analysis.recommendations:
                task += "Recommendations:\n"
                for i, rec in enumerate(analysis.recommendations, 1):
                    task += f"{i}. {rec}\n"
        
        if investigation_results:
            task += f"\n\nInvestigation Details:\n"
            total_queries = sum(len(report.tasks_executed) for report in investigation_results)
            task += f"Total queries executed: {total_queries} across {len(investigation_results)} tasks\n"
        
        if profiling_results:
            total_profiles = sum(len(report.tasks_executed) for report in profiling_results)
            task += f"Total profiles generated: {total_profiles} across {len(profiling_results)} tasks\n"
            
            task += f"\nProfiling Reports Available:\n"
            for report in profiling_results:
                for prof in report.tasks_executed:
                    # Remove 'ge_reports/' prefix from paths if present
                    html_path = prof.html_report_path
                    json_path = prof.json_report_path
                    if html_path.startswith('ge_reports/'):
                        html_path = html_path[11:]  # Remove 'ge_reports/' prefix
                    if json_path.startswith('ge_reports/'):
                        json_path = json_path[11:]  # Remove 'ge_reports/' prefix
                    task += f"- {prof.task_purpose}:\n"
                    task += f"  - HTML: {html_path}\n"
                    task += f"  - JSON: {json_path}\n"
        
        task += "\n\nPlease generate a comprehensive, well-formatted HTML report with all sections."
        task += "\nEnd your response with REPORT_COMPLETE when finished."
        
        return task
    
    def _save_html_report(self, html: str, goal: str) -> Path:
        """Save HTML report to file."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create safe filename from goal
        safe_goal = "".join(c if c.isalnum() or c in (' ', '_') else '_' for c in goal)
        safe_goal = safe_goal[:50]  # Limit length
        filename = f"data_quality_report_{safe_goal}_{timestamp}.html"
        report_path = self.reports_dir / filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return report_path
    
    def _save_results(self, results: Dict[str, Any]) -> None:
        """Save complete workflow results to JSON file."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Convert Pydantic models to dicts for JSON serialization
        json_results = {
            "goal": results["goal"],
            "timestamp": timestamp,
            "success": results["success"]
        }
        
        if results.get("plan"):
            json_results["plan"] = results["plan"].model_dump() if hasattr(results["plan"], "model_dump") else str(results["plan"])
        
        if results.get("investigation_results"):
            # Handle list of results
            if isinstance(results["investigation_results"], list):
                json_results["investigation_results"] = [
                    r.model_dump() if hasattr(r, "model_dump") else str(r)
                    for r in results["investigation_results"]
                ]
            else:
                json_results["investigation_results"] = results["investigation_results"].model_dump() if hasattr(results["investigation_results"], "model_dump") else str(results["investigation_results"])
        
        if results.get("profiling_results"):
            # Handle list of results
            if isinstance(results["profiling_results"], list):
                json_results["profiling_results"] = [
                    r.model_dump() if hasattr(r, "model_dump") else str(r)
                    for r in results["profiling_results"]
                ]
            else:
                json_results["profiling_results"] = results["profiling_results"].model_dump() if hasattr(results["profiling_results"], "model_dump") else str(results["profiling_results"])
        
        if results.get("analysis"):
            json_results["analysis"] = results["analysis"].model_dump() if hasattr(results["analysis"], "model_dump") else str(results["analysis"])
        
        if results.get("error"):
            json_results["error"] = results["error"]
        
        results_path = self.reports_dir / f"workflow_results_{timestamp}.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(json_results, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Workflow results saved to: {results_path}")


# Convenience function for running the orchestrator
async def run_data_quality_analysis(
    goal: str,
    reports_dir: str = "ge_reports",
    max_rounds: int = 20,
    enable_console: bool = True
) -> Dict[str, Any]:
    """
    Convenience function to run complete data quality analysis.
    
    Args:
        goal: Data quality goal to analyze
        reports_dir: Directory for storing reports
        max_rounds: Maximum conversation rounds per phase
        enable_console: Whether to show console output
        
    Returns:
        Dictionary with complete workflow results
    """
    orchestrator = Orchestrator(
        reports_dir=reports_dir,
        max_rounds=max_rounds,
        enable_console_output=enable_console
    )
    return await orchestrator.run_analysis(goal)
