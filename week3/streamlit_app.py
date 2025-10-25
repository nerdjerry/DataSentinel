"""
DataSentinel Streamlit App

A user-friendly web interface for running data quality analysis workflows.
Users can input goals and monitor the 4-phase execution in real-time.
"""

import streamlit as st
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from agent.Orchestrator import Orchestrator


# Page configuration
st.set_page_config(
    page_title="DataSentinel - Data Quality Analysis",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .phase-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 2px solid #e0e0e0;
        background-color: #f8f9fa;
    }
    .phase-running {
        border-color: #1f77b4;
        background-color: #e3f2fd;
    }
    .phase-complete {
        border-color: #2e7d32;
        background-color: #e8f5e9;
    }
    .phase-error {
        border-color: #c62828;
        background-color: #ffebee;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: 600;
        border-radius: 0.5rem;
        padding: 0.75rem;
    }
    .stButton>button:hover {
        background-color: #1565c0;
    }
    </style>
    """, unsafe_allow_html=True)


class WorkflowLogger:
    """Custom logger for capturing workflow progress in Streamlit."""
    
    def __init__(self, update_callback=None):
        """
        Initialize the workflow logger.
        
        Args:
            update_callback: Optional callback function to trigger on updates
        """
        # TODO: Initialize instance variables
        # - logs: list to store log entries
        # - phase_status: dict with 4 phases, all set to "pending"
        # - phase_details: dict with 4 phases, each with empty dict
        # - update_callback: store the callback function
        raise NotImplementedError("Students need to implement __init__ method")
    
    def log(self, message: str, level: str = "info", show_in_ui: bool = True):
        """
        Add a log entry.
        
        Args:
            message: Log message to add
            level: Log level (info, success, error, warning)
            show_in_ui: Whether to show this log in the UI
        
        TODO:
        - Create timestamp using datetime.now().strftime("%H:%M:%S")
        - Append log entry dict to self.logs with timestamp, message, level, show_in_ui
        - Trigger callback if provided
        """
        raise NotImplementedError("Students need to implement log method")
    
    def update_phase_status(self, phase: str, status: str, details: Dict[str, Any] = None):
        """
        Update the status of a phase.
        
        Args:
            phase: Phase name (e.g., "Phase 1: Planning")
            status: New status (pending, running, complete, error)
            details: Optional dict with phase-specific details
        
        TODO:
        - Update phase status in self.phase_status
        - Update phase details if provided
        - Trigger callback if provided
        """
        raise NotImplementedError("Students need to implement update_phase_status method")
    
    def get_logs(self):
        """
        Get all logs.
        
        Returns:
            List of log entries
        """
        # TODO: Return the logs list
        raise NotImplementedError("Students need to implement get_logs method")
    
    def get_phase_status(self):
        """
        Get phase statuses.
        
        Returns:
            Tuple of (phase_status dict, phase_details dict)
        """
        # TODO: Return phase_status and phase_details
        raise NotImplementedError("Students need to implement get_phase_status method")


class StreamlitOrchestrator(Orchestrator):
    """Extended Orchestrator with Streamlit logging capabilities."""
    
    def __init__(self, logger: WorkflowLogger, **kwargs):
        """
        Initialize StreamlitOrchestrator.
        
        Args:
            logger: WorkflowLogger instance
            **kwargs: Additional arguments for parent Orchestrator
        
        TODO:
        - Call parent class __init__ with kwargs
        - Store logger instance
        """
        raise NotImplementedError("Students need to implement __init__ method")
    
    async def run_analysis(self, goal: str) -> Dict[str, Any]:
        """
        Override run_analysis to include Streamlit logging.
        
        Args:
            goal: Analysis goal string
        
        Returns:
            Dictionary with analysis results
        
        TODO:
        - Initialize results dictionary with all None values
        - Log start of analysis
        - Run each phase with proper logging and error handling:
          - Phase 1: Planning
          - Phase 2: Investigation & Profiling  
          - Phase 3: Analysis & Summarization
          - Phase 4: Report Generation
        - Update phase status and details after each phase
        - Handle exceptions and log errors
        - Save results to file
        - Return results dictionary
        """
        raise NotImplementedError("Students need to implement run_analysis method")
    
    async def _run_planning_phase_logged(self, goal: str):
        """
        Planning phase with logging.
        
        Args:
            goal: Analysis goal
        
        Returns:
            Planning result from parent class
        
        TODO:
        - Call parent class _run_planning_phase
        - Handle exceptions and log errors
        - Return result
        """
        raise NotImplementedError("Students need to implement _run_planning_phase_logged method")
    
    async def _run_investigation_phase_logged(self, plan):
        """
        Investigation phase with detailed logging.
        
        Args:
            plan: Execution plan from planning phase
        
        Returns:
            Tuple of (investigation_results, profiling_results)
        
        TODO:
        - Call parent class _run_investigation_phase
        - Handle exceptions and log errors
        - Return results tuple
        """
        raise NotImplementedError("Students need to implement _run_investigation_phase_logged method")
    
    async def _run_analysis_phase_logged(self, goal, plan, investigation_results, profiling_results):
        """
        Analysis phase with logging.
        
        Args:
            goal: Analysis goal
            plan: Execution plan
            investigation_results: Results from investigation
            profiling_results: Results from profiling
        
        Returns:
            Analysis result from parent class
        
        TODO:
        - Call parent class _run_analysis_phase
        - Handle exceptions and log errors
        - Return result
        """
        raise NotImplementedError("Students need to implement _run_analysis_phase_logged method")
    
    async def _run_reporting_phase_logged(self, goal, plan, investigation_results, profiling_results, analysis):
        """
        Reporting phase with logging.
        
        Args:
            goal: Analysis goal
            plan: Execution plan
            investigation_results: Results from investigation
            profiling_results: Results from profiling
            analysis: Analysis results
        
        Returns:
            Report result from parent class
        
        TODO:
        - Call parent class _run_reporting_phase
        - Handle exceptions and log errors
        - Return result
        """
        raise NotImplementedError("Students need to implement _run_reporting_phase_logged method")


def render_phase_card(phase_name: str, status: str, details: Dict[str, Any]):
    """
    Render a phase status card.
    
    Args:
        phase_name: Name of the phase
        status: Current status (pending, running, complete, error)
        details: Dict with phase-specific details to display
    
    TODO:
    - Define status icons (pending: ⏳, running: 🔄, complete: ✅, error: ❌)
    - Define CSS classes for each status
    - Create card container with appropriate styling
    - Display phase name with icon
    - Display status
    - If details exist and status is complete/running, show metrics
    """
    raise NotImplementedError("Students need to implement render_phase_card function")


def render_logs(logs):
    """
    Render logs in a simple, user-friendly format.
    
    Args:
        logs: List of log entries
    
    TODO:
    - Display "Progress" header
    - Filter logs to show only UI-relevant ones (show_in_ui=True)
    - Show "Waiting to start analysis..." if no logs
    - Display last 10 logs with appropriate icons and styling:
      - info: 🔵 with st.info()
      - success: ✅ with st.success()
      - error: ❌ with st.error()
      - warning: ⚠️ with st.warning()
    """
    raise NotImplementedError("Students need to implement render_logs function")


async def run_workflow_async(goal: str, logger: WorkflowLogger):
    """
    Run the workflow asynchronously.
    
    Args:
        goal: Analysis goal
        logger: WorkflowLogger instance
    
    Returns:
        Analysis results dictionary
    
    TODO:
    - Create StreamlitOrchestrator with logger
    - Set reports_dir="ge_reports"
    - Set max_rounds=20
    - Set enable_console_output=False
    - Call run_analysis with goal
    - Return results
    """
    raise NotImplementedError("Students need to implement run_workflow_async function")


def main():
    """
    Main Streamlit app.
    
    TODO:
    - Display header and subtitle
    - Create sidebar with information about phases
    - Initialize session state variables (workflow_running, logger, results)
    - Create goal input area
    - Display quick stats (count of existing reports)
    - Create Run Analysis button
    - Handle button click:
      - Set workflow_running to True
      - Create new WorkflowLogger
      - Run workflow with asyncio.run()
      - Display phase cards and logs
      - Show success/error messages
      - Handle report download
    - Display footer
    """
    raise NotImplementedError("Students need to implement main function")


if __name__ == "__main__":
    main()
