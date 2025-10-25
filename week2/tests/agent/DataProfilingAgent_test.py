import asyncio
import sys
import os
from pathlib import Path

from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import StructuredMessage
from autogen_agentchat.conditions import MaxMessageTermination
from agent.DataProfilingAgent import DataProfilingAgent
from agent.DataProfilingAgent import DataProfilingReport


async def test_profiling_agent():
    """Test the DataProfilingAgent with a sample profiling task."""
    print("=" * 80)
    print("Testing DataProfilingAgent")
    print("=" * 80)
    
    # Create the profiling agent
    profiling_agent = DataProfilingAgent(reports_dir="ge_reports").get_agent()
    
    # Test task: Profile the RIDEBOOKING table
    task = """
    Profile the BOOKING_VALUE column (after normalizing literal 'null' strings) to produce completeness (null rate), distinct count, min/max, mean, median, standard deviation, percentiles (p1/p5/p25/p50/p75/p95/p99), histogram and outlier detection; include breakdowns by VEHICLE_TYPE and PAYMENT_METHOD to identify distributional skew and segment-specific data-quality issues.
    """
    
    print(f"\nTask: {task}\n")
    print("-" * 80)
    
    # Run the agent
    await Console(profiling_agent.run_stream(task=task))
    
async def test_team_execution():
    """Test profiling with team execution using RoundRobinGroupChat."""
    print("\n" + "=" * 80)
    print("Testing Team Execution")
    print("=" * 80)
    
    # Create the profiling agent
    profiling_agent = DataProfilingAgent(reports_dir="ge_reports").get_agent()
    
    # Define the profiling task
    profiling_task_str = """
    Profile the BOOKING_VALUE column (after normalizing literal 'null' strings) to produce completeness (null rate), distinct count, min/max, mean, median, standard deviation, percentiles (p1/p5/p25/p50/p75/p95/p99), histogram and outlier detection; include breakdowns by VEHICLE_TYPE and PAYMENT_METHOD to identify distributional skew and segment-specific data-quality issues.
    """
    
    termination = MaxMessageTermination(max_messages=3)
    team = RoundRobinGroupChat(
        [profiling_agent],
        termination_condition=termination,
        custom_message_types=[StructuredMessage[DataProfilingReport]]
    )
    
    # Run with console output
    result = await Console(team.run_stream(task=profiling_task_str))
    
    # Extract and store result
    all_profiling_results = []
    for message in reversed(result.messages):
        if hasattr(message, 'content') and isinstance(message.content, DataProfilingReport):
            all_profiling_results.append(message.content)
            break
    
    print("\n" + "=" * 80)
    print("Team execution completed!")
    print("=" * 80)
    print(all_profiling_results)
    
    return all_profiling_results

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
        # await test_profiling_agent()
        
        # Uncomment to test custom query profiling
        # await test_custom_query_profiling()

        # Test team execution
        await test_team_execution()
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
