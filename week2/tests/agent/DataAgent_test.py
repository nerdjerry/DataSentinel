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
    
    # TODO: Create the profiling agent
    # Hint: Use DataAgent().get_agent()
    
    # TODO: Define the profiling task
    # Task should check for NULLs and literal 'null' string values in critical columns:
    # BOOKING_ID, DATE, TIME, CUSTOMER_ID, Booking Status, BOOKING_VALUE, 
    # RIDE_DISTANCE, PAYMENT_METHOD, DRIVER_RATINGS, CUSTOMER_RATING, 
    # VEHICLE_TYPE, PICKUP_LOCATION, DROP_LOCATION
    
    # TODO: Create termination condition
    # Hint: Use MaxMessageTermination with max_messages=5
    
    # TODO: Create RoundRobinGroupChat team
    # Include:
    # - List of agents (just data_agent)
    # - termination_condition
    # - custom_message_types with StructuredMessage[DataAgentReport]
    
    # TODO: Run the team with console output
    # Hint: Use Console(team.run_stream(task=task_str))
    
    # TODO: Extract and store results
    # Loop through result.messages in reverse
    # Check for DataAgentReport content and append to all_profiling_results
    
    print("\n" + "=" * 80)
    print("Team execution completed!")
    print("=" * 80)
    
    # TODO: Print and return the profiling results
    pass  # Remove this when implementing

async def test_data_agent_basic():
    """Test basic data agent functionality with a simple goal"""
    print("=" * 80)
    print("Testing DataAgent - Basic Goal")
    print("=" * 80)
    
    # TODO: Create a DataAgent instance and get the agent
    # Hint: Use DataAgent().get_agent()
    
    # TODO: Define a data quality goal
    # Example: "Highlight 1 data quality issue in RIDEBOOKING table and suggest a fix"
    
    # TODO: Print the goal with formatting
    
    # TODO: Run the agent with Console output
    # Hint: Use Console(agent.run_stream(task=goal))
    
    pass  # Remove this when implementing

if __name__ == "__main__":

    async def main() -> None:
        #await test_data_agent_basic()
        await test_team_execution()

    asyncio.run(main())