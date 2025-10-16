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
        self.logs = []
        self.phase_status = {
            "Phase 1: Planning": "pending",
            "Phase 2: Investigation": "pending",
            "Phase 3: Analysis": "pending",
            "Phase 4: Reporting": "pending"
        }
        self.phase_details = {
            "Phase 1: Planning": {},
            "Phase 2: Investigation": {},
            "Phase 3: Analysis": {},
            "Phase 4: Reporting": {}
        }
        self.update_callback = update_callback
    
    def log(self, message: str, level: str = "info", show_in_ui: bool = True):
        """Add a log entry."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append({
            "timestamp": timestamp,
            "message": message,
            "level": level,
            "show_in_ui": show_in_ui
        })
        # Trigger callback if provided
        if self.update_callback:
            self.update_callback()
    
    def update_phase_status(self, phase: str, status: str, details: Dict[str, Any] = None):
        """Update the status of a phase."""
        self.phase_status[phase] = status
        if details:
            self.phase_details[phase].update(details)
        # Trigger callback if provided
        if self.update_callback:
            self.update_callback()
    
    def get_logs(self):
        """Get all logs."""
        return self.logs
    
    def get_phase_status(self):
        """Get phase statuses."""
        return self.phase_status, self.phase_details


class StreamlitOrchestrator(Orchestrator):
    """Extended Orchestrator with Streamlit logging capabilities."""
    
    def __init__(self, logger: WorkflowLogger, **kwargs):
        super().__init__(**kwargs)
        self.logger = logger
    
    async def run_analysis(self, goal: str) -> Dict[str, Any]:
        """Override run_analysis to include Streamlit logging."""
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
            self.logger.log("Starting data quality analysis...", "info")
            
            # Phase 1: Planning
            self.logger.log("Phase 1: Creating execution plan", "info")
            self.logger.update_phase_status("Phase 1: Planning", "running")
            plan = await self._run_planning_phase_logged(goal)
            results["plan"] = plan
            
            if plan:
                self.logger.update_phase_status(
                    "Phase 1: Planning", 
                    "complete",
                    {
                        "query_tasks": len(plan.query_tasks),
                        "profiling_tasks": len(plan.profiling_tasks)
                    }
                )
                self.logger.log(f"Phase 1 complete - Created {len(plan.query_tasks)} query tasks and {len(plan.profiling_tasks)} profiling tasks", "success")
            else:
                self.logger.update_phase_status("Phase 1: Planning", "error")
                self.logger.log("Phase 1 failed - Could not create execution plan", "error")
                results["error"] = "Planning failed"
                return results
            
            # Phase 2: Investigation & Profiling
            self.logger.log("Phase 2: Running queries and profiling data", "info")
            self.logger.update_phase_status("Phase 2: Investigation", "running")
            investigation_results, profiling_results = await self._run_investigation_phase_logged(plan)
            results["investigation_results"] = investigation_results
            results["profiling_results"] = profiling_results
            
            investigation_count = len(investigation_results) if investigation_results else 0
            profiling_count = len(profiling_results) if profiling_results else 0
            
            self.logger.update_phase_status(
                "Phase 2: Investigation",
                "complete",
                {
                    "investigation_tasks": investigation_count,
                    "profiling_tasks": profiling_count
                }
            )
            self.logger.log(f"Phase 2 complete - Executed {investigation_count} queries and generated {profiling_count} profiles", "success")
            
            # Phase 3: Analysis & Summarization
            self.logger.log("Phase 3: Analyzing findings and identifying issues", "info")
            self.logger.update_phase_status("Phase 3: Analysis", "running")
            analysis = await self._run_analysis_phase_logged(goal, plan, investigation_results, profiling_results)
            results["analysis"] = analysis
            
            if analysis:
                self.logger.update_phase_status(
                    "Phase 3: Analysis",
                    "complete",
                    {
                        "issues_found": len(analysis.issues),
                        "recommendations": len(analysis.recommendations)
                    }
                )
                self.logger.log(f"Phase 3 complete - Found {len(analysis.issues)} issues and created {len(analysis.recommendations)} recommendations", "success")
            else:
                self.logger.update_phase_status("Phase 3: Analysis", "error")
                self.logger.log("Phase 3 failed - Could not complete analysis", "error")
            
            # Phase 4: Report Generation
            self.logger.log("Phase 4: Generating final report", "info")
            self.logger.update_phase_status("Phase 4: Reporting", "running")
            report = await self._run_reporting_phase_logged(goal, plan, investigation_results, profiling_results, analysis)
            results["report"] = report
            
            if report:
                self.logger.update_phase_status("Phase 4: Reporting", "complete")
                self.logger.log("Phase 4 complete - Report generated successfully", "success")
            else:
                self.logger.update_phase_status("Phase 4: Reporting", "error")
                self.logger.log("Phase 4 failed - Could not generate report", "error")
            
            results["success"] = True
            self.logger.log("Analysis completed successfully!", "success")
            
            # Save results to file
            self._save_results(results)
            
            return results
            
        except Exception as e:
            self.logger.log(f"Error: {str(e)}", "error")
            results["error"] = str(e)
            import traceback
            results["traceback"] = traceback.format_exc()
            return results
    
    async def _run_planning_phase_logged(self, goal: str):
        """Planning phase with logging."""
        try:
            result = await super()._run_planning_phase(goal)
            return result
        except Exception as e:
            self.logger.log(f"Planning error: {str(e)}", "error")
            raise
    
    async def _run_investigation_phase_logged(self, plan):
        """Investigation phase with detailed logging."""
        try:
            investigation_results, profiling_results = await super()._run_investigation_phase(plan)
            return investigation_results, profiling_results
        except Exception as e:
            self.logger.log(f"Investigation error: {str(e)}", "error")
            raise
    
    async def _run_analysis_phase_logged(self, goal, plan, investigation_results, profiling_results):
        """Analysis phase with logging."""
        try:
            result = await super()._run_analysis_phase(goal, plan, investigation_results, profiling_results)
            return result
        except Exception as e:
            self.logger.log(f"Analysis error: {str(e)}", "error")
            raise
    
    async def _run_reporting_phase_logged(self, goal, plan, investigation_results, profiling_results, analysis):
        """Reporting phase with logging."""
        try:
            result = await super()._run_reporting_phase(goal, plan, investigation_results, profiling_results, analysis)
            return result
        except Exception as e:
            self.logger.log(f"Reporting error: {str(e)}", "error")
            raise


def render_phase_card(phase_name: str, status: str, details: Dict[str, Any]):
    """Render a phase status card."""
    status_icons = {
        "pending": "⏳",
        "running": "🔄",
        "complete": "✅",
        "error": "❌"
    }
    
    status_colors = {
        "pending": "",
        "running": "phase-running",
        "complete": "phase-complete",
        "error": "phase-error"
    }
    
    icon = status_icons.get(status, "⏳")
    color_class = status_colors.get(status, "")
    
    with st.container():
        st.markdown(f'<div class="phase-card {color_class}">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {icon} {phase_name}")
        
        with col2:
            st.markdown(f"**Status:** {status.upper()}")
        
        if details and status in ["complete", "running"]:
            st.markdown("---")
            cols = st.columns(len(details))
            for idx, (key, value) in enumerate(details.items()):
                with cols[idx]:
                    st.metric(label=key.replace("_", " ").title(), value=value)
        
        st.markdown('</div>', unsafe_allow_html=True)


def render_logs(logs):
    """Render logs in a simple, user-friendly format."""
    st.markdown("### 📝 Progress")
    
    # Filter to show only UI-relevant logs
    ui_logs = [log for log in logs if log.get("show_in_ui", True)]
    
    if not ui_logs:
        st.info("Waiting to start analysis...")
        return
    
    log_container = st.container()
    with log_container:
        for log in ui_logs[-10:]:  # Show last 10 logs only
            level_icons = {
                "info": "🔵",
                "success": "✅",
                "error": "❌",
                "warning": "⚠️"
            }
            icon = level_icons.get(log["level"], "🔵")
            
            # Simple format without timestamp for cleaner look
            if log["level"] == "success":
                st.success(f"{icon} {log['message']}")
            elif log["level"] == "error":
                st.error(f"{icon} {log['message']}")
            elif log["level"] == "warning":
                st.warning(f"{icon} {log['message']}")
            else:
                st.info(f"{icon} {log['message']}")


async def run_workflow_async(goal: str, logger: WorkflowLogger):
    """Run the workflow asynchronously."""
    orchestrator = StreamlitOrchestrator(
        logger=logger,
        reports_dir="ge_reports",
        max_rounds=20,
        enable_console_output=False  # Disable console output for Streamlit
    )
    
    results = await orchestrator.run_analysis(goal)
    return results


def main():
    """Main Streamlit app."""
    
    # Header
    st.markdown('<p class="main-header">🛡️ DataSentinel</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Multi-Agent Data Quality Analysis Platform</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ℹ️ About")
        st.markdown("""
        DataSentinel uses a multi-agent system to perform comprehensive data quality analysis:
        
        **Phase 1: Planning**  
        Creates an execution plan with query and profiling tasks
        
        **Phase 2: Investigation**  
        Executes queries and generates statistical profiles
        
        **Phase 3: Analysis**  
        Synthesizes findings and identifies issues
        
        **Phase 4: Reporting**  
        Generates a professional HTML report
        """)
        
    # Initialize session state
    if "workflow_running" not in st.session_state:
        st.session_state.workflow_running = False
    if "logger" not in st.session_state:
        st.session_state.logger = None
    if "results" not in st.session_state:
        st.session_state.results = None
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Data Quality Goal")
        goal = st.text_area(
            "Enter your data quality analysis goal:",
            height=100,
            placeholder="Example: Analyze missing values in the RIDEBOOKING table and assess data quality",
            key="goal_input"
        )
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        reports_dir = Path("ge_reports")
        if reports_dir.exists():
            html_reports = list(reports_dir.glob("*.html"))
            json_reports = list(reports_dir.glob("*.json"))
            st.metric("HTML Reports", len(html_reports))
            st.metric("JSON Reports", len(json_reports))
        else:
            st.metric("HTML Reports", 0)
            st.metric("JSON Reports", 0)
    
    # Run button
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        run_button = st.button("🚀 Run Analysis", disabled=st.session_state.workflow_running or not goal, use_container_width=True)
    
    with col_btn2:
        if st.session_state.results and st.session_state.results.get("report"):
            # Find the latest HTML report
            reports_dir = Path("ge_reports")
            html_reports = sorted(reports_dir.glob("data_quality_report_*.html"), key=lambda x: x.stat().st_mtime, reverse=True)
            if html_reports:
                report_path = html_reports[0]
                with open(report_path, 'r', encoding='utf-8') as f:
                    report_html = f.read()
                st.download_button(
                    "📥 Download Report",
                    data=report_html,
                    file_name=report_path.name,
                    mime="text/html",
                    use_container_width=True
                )
    
    # Handle workflow execution
    if run_button and goal:
        st.session_state.workflow_running = True
        st.session_state.logger = WorkflowLogger()
        st.session_state.results = None
        
        # Display workflow status section immediately
        st.markdown("## 📊 Workflow Progress")
        
        # Use st.status for expandable progress tracking
        with st.status("Running data quality analysis...", expanded=True) as status:
            st.write("🔄 Starting workflow...")
            
            # Run the workflow
            try:
                # Run async workflow in Streamlit
                results = asyncio.run(run_workflow_async(goal, st.session_state.logger))
                st.session_state.results = results
                
                # Show completion
                status.update(label="✅ Analysis complete!", state="complete", expanded=True)
            
            except Exception as e:
                status.update(label="❌ Analysis failed", state="error", expanded=True)
                st.error(f"Error: {str(e)}")
                import traceback
                with st.expander("View Error Details"):
                    st.code(traceback.format_exc())
                st.session_state.workflow_running = False
                st.stop()
        
        # Display phase cards after completion
        st.markdown("---")
        st.markdown("## 📊 Workflow Status")
        
        phase_status, phase_details = st.session_state.logger.get_phase_status()
        for phase_name, status_val in phase_status.items():
            render_phase_card(phase_name, status_val, phase_details.get(phase_name, {}))
        
        # Display logs after completion
        st.markdown("---")
        render_logs(st.session_state.logger.get_logs())
        
        # Show success message and summary
        try:
            if results.get("success"):
                st.markdown("---")
                st.success("✅ Workflow completed successfully!")
                
                # Display summary
                if results.get("analysis"):
                    analysis = results["analysis"]
                    st.markdown("---")
                    st.markdown("### 📋 Summary")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Issues Found", len(analysis.issues) if hasattr(analysis, 'issues') else 0)
                    with col2:
                        st.metric("Recommendations", len(analysis.recommendations) if hasattr(analysis, 'recommendations') else 0)
                    with col3:
                        st.metric("Follow-up Queries", len(analysis.required_followup_queries) if hasattr(analysis, 'required_followup_queries') else 0)
                    
                    if hasattr(analysis, 'summary'):
                        st.markdown("#### Executive Summary")
                        st.info(analysis.summary)
                
                # Show report location
                if results.get("report"):
                    reports_dir = Path("ge_reports")
                    html_reports = sorted(reports_dir.glob("data_quality_report_*.html"), key=lambda x: x.stat().st_mtime, reverse=True)
                    if html_reports:
                        st.markdown("---")
                        st.markdown("### 📄 Generated Reports")
                        st.success(f"Report saved to: `{html_reports[0]}`")
            else:
                st.error(f"❌ Workflow failed: {results.get('error', 'Unknown error')}")
                if results.get('traceback'):
                    with st.expander("View Error Details"):
                        st.code(results['traceback'])
        
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            import traceback
            with st.expander("View Error Details"):
                st.code(traceback.format_exc())
        
        finally:
            st.session_state.workflow_running = False
    
    # Display existing results if available
    elif st.session_state.logger:
        phase_status, phase_details = st.session_state.logger.get_phase_status()
        
        st.markdown("## 📊 Workflow Status")
        for phase_name, status in phase_status.items():
            render_phase_card(phase_name, status, phase_details.get(phase_name, {}))
        
        st.markdown("---")
        render_logs(st.session_state.logger.get_logs())
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>DataSentinel v2.1 | Powered by AutoGen & ydata-profiling</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
