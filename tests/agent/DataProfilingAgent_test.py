import asyncio
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

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
        DATE as booking_date,
        COUNT(*) as total_bookings,
        AVG(TRY_CAST(BOOKING_VALUE AS DECIMAL(10,2))) as avg_booking_value,
        SUM(TRY_CAST(BOOKING_VALUE AS DECIMAL(10,2))) as total_revenue,
        AVG(TRY_CAST(RIDE_DISTANCE AS DECIMAL(10,2))) as avg_distance,
        COUNT(DISTINCT CUSTOMER_ID) as unique_customers,
        COUNT(CASE WHEN BOOKING_VALUE IS NULL OR BOOKING_VALUE = 'null' THEN 1 END) as null_booking_values,
        COUNT(CASE WHEN RIDE_DISTANCE IS NULL OR RIDE_DISTANCE = 'null' THEN 1 END) as null_distances
    FROM RIDEBOOKING
    WHERE DATE IS NOT NULL
    GROUP BY DATE
    ORDER BY DATE DESC
    LIMIT 30
    
    Analyze the data quality of this aggregated view and identify any patterns or issues.
    Focus on booking trends, revenue patterns, and customer activity.
    Pay special attention to null values and data quality issues.
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
        #await test_profiling_agent()
        
        # Uncomment to test custom query profiling
        await test_custom_query_profiling()
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
