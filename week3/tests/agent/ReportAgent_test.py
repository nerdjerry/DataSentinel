import asyncio
import sys
from pathlib import Path

from autogen_agentchat.ui import Console
from agent.ReportAgent import ReportAgent, ReportResponse
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import StructuredMessage

async def test_team_execution():
    """Test Report Agent with team execution using RoundRobinGroupChat.
    
    TODO: Implement this method to:
    1. Create a ReportAgent instance
    2. Define a profiling task with data quality analysis
    3. Set up a RoundRobinGroupChat team with termination conditions
    4. Run the team with console output
    5. Extract and save the HTML report from the results
    """
    # TODO: Implement the team execution test
    raise NotImplementedError("Students need to implement test_team_execution()")

def save_html_report(html: str, goal: str) -> str:
    """Save HTML report to file.
    
    Args:
        html: The HTML content to save
        goal: The goal/title for the report (used in filename)
    
    Returns:
        str: The path where the report was saved
    
    TODO: Implement this method to:
    1. Create a timestamp for the filename
    2. Create a safe filename from the goal parameter
    3. Create a reports directory if it doesn't exist
    4. Write the HTML content to the file
    5. Return the file path
    """
    # TODO: Implement the HTML report saving logic
    raise NotImplementedError("Students need to implement save_html_report()")

if __name__ == "__main__":

    async def main() -> None:
        """Main entry point for running the test.
        
        TODO: Call the test_team_execution() method
        """
        # TODO: Implement the main function
        raise NotImplementedError("Students need to implement main()")

    asyncio.run(main())
