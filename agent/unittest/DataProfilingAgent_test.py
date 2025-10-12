import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from autogen_agentchat.ui import Console
from agent.DataProfilingAgent import DataProfilingAgent


async def test_profiling_agent():
    """Test the DataProfilingAgent with a sample profiling task."""
    print("=" * 80)
    print("Testing DataProfilingAgent")
    print("=" * 80)
    
    # Create the profiling agent
    profiling_agent = DataProfilingAgent(reports_dir="ge_reports").get_agent()
    
    # Test task: Profile the RIDEBOOKING table
    task = """
    Profile the RIDEBOOKING table in Snowflake. 
    Get a sample of 100 rows and analyze the data quality.
    Generate both HTML and JSON reports.
    
    Provide:
    1. Summary of the dataset (rows, columns)
    2. Data quality metrics (null counts, data types)
    3. Key findings or issues discovered
    4. Paths to the generated reports
    """
    
    print(f"\nTask: {task}\n")
    print("-" * 80)
    
    # Run the agent
    await Console(profiling_agent.run_stream(task=task))
    
    print("\n" + "=" * 80)
    print("Test completed!")
    print("=" * 80)


async def test_custom_query_profiling():
    """Test profiling with a custom aggregated query."""
    print("\n" + "=" * 80)
    print("Testing Custom Query Profiling")
    print("=" * 80)
    
    profiling_agent = DataProfilingAgent(reports_dir="ge_reports").get_agent()
    
    task = """
    Profile the daily booking statistics using this query:
    
    SELECT 
        DATE_TRUNC('day', BOOKING_DATE) as booking_day,
        COUNT(*) as total_bookings,
        AVG(FARE_AMOUNT) as avg_fare,
        SUM(FARE_AMOUNT) as total_revenue
    FROM RIDEBOOKING
    WHERE BOOKING_DATE >= DATEADD(day, -30, CURRENT_DATE())
    GROUP BY DATE_TRUNC('day', BOOKING_DATE)
    ORDER BY booking_day DESC
    
    Analyze the data quality of this aggregated view and identify any patterns or issues.
    """
    
    print(f"\nTask: {task}\n")
    print("-" * 80)
    
    await Console(profiling_agent.run_stream(task=task))
    
    print("\n" + "=" * 80)
    print("Custom query profiling completed!")
    print("=" * 80)


async def main():
    """Run all agent tests."""
    try:
        # Test basic profiling
        await test_profiling_agent()
        
        # Uncomment to test custom query profiling
        # await test_custom_query_profiling()
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
