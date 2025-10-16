import asyncio
import sys
from pathlib import Path


from autogen_agentchat.ui import Console
from agent.DataAgent import DataAgent, DataAgentReport
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import StructuredMessage

async def test_team_execution():
    """Test profiling with team execution using RoundRobinGroupChat."""
    print("\n" + "=" * 80)
    print("Testing Team Execution")
    print("=" * 80)
    
    # Create the profiling agent
    data_agent = DataAgent().get_agent()
    
    # Define the profiling task
    task_str = """
    Check for NULLs and literal 'null' string values in critical columns: BOOKING_ID, DATE, TIME, CUSTOMER_ID, Booking Status, BOOKING_VALUE, RIDE_DISTANCE, PAYMENT_METHOD, DRIVER_RATINGS, CUSTOMER_RATING, VEHICLE_TYPE, PICKUP_LOCATION, DROP_LOCATION.
    """
    
    termination = MaxMessageTermination(max_messages=5)
    team = RoundRobinGroupChat(
        [data_agent],
        termination_condition=termination,
        custom_message_types=[StructuredMessage[DataAgentReport]]
    )
    
    # Run with console output
    result = await Console(team.run_stream(task=task_str))

    # Extract and store result
    all_profiling_results = []
    for message in reversed(result.messages):
        if hasattr(message, 'content') and isinstance(message.content, DataAgentReport):
            all_profiling_results.append(message.content)
            break
    
    print("\n" + "=" * 80)
    print("Team execution completed!")
    print("=" * 80)
    print(all_profiling_results)
    
    return all_profiling_results

async def test_data_agent_basic():
    """Test basic data agent functionality with a simple goal"""
    print("=" * 80)
    print("Testing DataAgent - Basic Goal")
    print("=" * 80)
    
    data_agent = DataAgent().get_agent()
    
    goal = "Highlight 1 data quality issue in RIDEBOOKING table and suggest a fix"
    
    print(f"\nData Quality Goal: {goal}\n")
    print("-" * 80)

    await Console(data_agent.run_stream(task=goal))

if __name__ == "__main__":

    async def main() -> None:
        #await test_data_agent_basic()
        await test_team_execution()

    asyncio.run(main())