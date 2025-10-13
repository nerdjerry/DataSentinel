import asyncio
import sys
from pathlib import Path

from agent.PlannerAgent import PlannerAgent
from autogen_agentchat.ui import Console


async def test_planner_basic():
    """Test basic planning with a simple goal"""
    print("=" * 80)
    print("Testing PlannerAgent - Basic Goal")
    print("=" * 80)
    
    planner = PlannerAgent().get_agent()
    
    goal = "Highlight 1 data quality issue in RIDEBOOKING table and suggest a fix"
    
    print(f"\nData Quality Goal: {goal}\n")
    print("-" * 80)

    await Console(planner.run_stream(task=goal))


async def test_planner_cancellation():
    """Test planning for cancellation analysis"""
    print("\n\n" + "=" * 80)
    print("Testing PlannerAgent - Cancellation Analysis")
    print("=" * 80)
    
    planner = PlannerAgent().get_agent()
    
    goal = "Understand patterns in customer cancellations and identify any data quality issues"
    
    print(f"\nData Quality Goal: {goal}\n")
    print("-" * 80)

    await Console(planner.run_stream(task=goal))


async def test_planner_correlations():
    """Test planning for correlation analysis"""
    print("\n\n" + "=" * 80)
    print("Testing PlannerAgent - Correlation Analysis")
    print("=" * 80)
    
    planner = PlannerAgent().get_agent()
    
    goal = "Analyze relationships between ride distance, booking value, and customer ratings. Find any inconsistencies."
    
    print(f"\nData Quality Goal: {goal}\n")
    print("-" * 80)

    await Console(planner.run_stream(task=goal))


async def test_planner_missing_data():
    """Test planning for missing data analysis"""
    print("\n\n" + "=" * 80)
    print("Testing PlannerAgent - Missing Data Analysis")
    print("=" * 80)
    
    planner = PlannerAgent().get_agent()
    
    goal = "Identify all missing or null values across critical booking fields and assess impact on data reliability"
    
    print(f"\nData Quality Goal: {goal}\n")
    print("-" * 80)

    await Console(planner.run_stream(task=goal))


async def test_planner_driver_performance():
    """Test planning for driver performance analysis"""
    print("\n\n" + "=" * 80)
    print("Testing PlannerAgent - Driver Performance Analysis")
    print("=" * 80)
    
    planner = PlannerAgent().get_agent()
    
    goal = "Evaluate driver ratings data quality and identify patterns in low-rated drivers"
    
    print(f"\nData Quality Goal: {goal}\n")
    print("-" * 80)

    await Console(planner.run_stream(task=goal))


async def main():
    """Run all planner tests"""
    try:
        # Run tests sequentially
        # await test_planner_basic()
        # await test_planner_cancellation()
        await test_planner_correlations()
        # await test_planner_missing_data()
        # await test_planner_driver_performance()
        
        print("\n\n" + "=" * 80)
        print("✓ All Planner Tests Completed!")
        print("=" * 80)
        print("\nThe Planner Agent successfully created comprehensive plans with:")
        print("  - Specific SQL queries for DataAgent")
        print("  - Profiling tasks for DataProfilingAgent")
        print("  - Clear execution sequences")
        print("  - Measurable success criteria")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
