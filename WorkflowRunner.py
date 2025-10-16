from agent.Orchestrator import Orchestrator
from typing import Any, Dict
import asyncio

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

if __name__ == "__main__":
    """Example usage of the Orchestrator"""
    
    async def main():
        # Example data quality goal
        goal = "Analyze missing values in the RIDEBOOKING table and assess data quality"
        
        # Run analysis
        results = await run_data_quality_analysis(
            goal=goal,
            reports_dir="ge_reports",
            enable_console=True
        )
        
        # Print summary
        print("\n" + "="*80)
        print("WORKFLOW SUMMARY")
        print("="*80)
        print(f"Goal: {results['goal']}")
        print(f"Success: {results['success']}")
        
        if results.get("analysis"):
            analysis = results["analysis"]
            print(f"\nIssues Found: {len(analysis.issues)}")
            print(f"Recommendations: {len(analysis.recommendations)}")
        
        if results.get("report"):
            print(f"\nFinal Report: Generated ✓")
        
        print("="*80)
    
    # Run the example
    asyncio.run(main())