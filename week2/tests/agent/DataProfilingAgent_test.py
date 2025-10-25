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
    
    # TODO: Student Implementation
    # 1. Create a DataProfilingAgent instance with reports_dir="ge_reports"
    # 2. Get the agent using the get_agent() method
    # 3. Define a profiling task to analyze the BOOKING_VALUE column
    # 4. Run the agent with Console output
    # 5. Return the results
    
    # Your implementation here:
    pass
    
async def test_team_execution():
    """Test profiling with team execution using RoundRobinGroupChat."""
    print("\n" + "=" * 80)
    print("Testing Team Execution")
    print("=" * 80)
    
    # TODO: Student Implementation
    # 1. Create a DataProfilingAgent with reports_dir="ge_reports"
    # 2. Define a profiling task for analyzing BOOKING_VALUE column
    # 3. Set up termination condition with MaxMessageTermination(max_messages=3)
    # 4. Create a RoundRobinGroupChat team with the agent
    # 5. Run the team with Console output
    # 6. Extract DataProfilingReport from results
    # 7. Return the profiling results
    
    # Your implementation here:
    pass

async def test_custom_query_profiling():
    """Test profiling with a custom aggregated query."""
    print("\n" + "=" * 80)
    print("Testing Custom Query Profiling")
    print("=" * 80)
    
    # TODO: Student Implementation
    # 1. Create a DataProfilingAgent instance
    # 2. Define a task with a custom SQL query for daily booking statistics
    #    Query should include:
    #    - Daily aggregations (COUNT, AVG, SUM)
    #    - Unique customer counts
    #    - Null value analysis
    # 3. Run the agent with the custom query task
    # 4. Display results using Console
    
    # Your implementation here:
    pass


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
