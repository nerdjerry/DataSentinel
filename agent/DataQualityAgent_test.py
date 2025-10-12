import asyncio
from autogen_agentchat.ui import Console
from DataQualityAgent import DataQualityAgent
from DataQualityAgent import DataQualityAgentReport, DataQualityIssue
from DataAgent import DataAgent
from ReportAgent import ReportAgent
from ReportAgent import ReportResponse
from autogen_agentchat.messages import StructuredMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination


if __name__ == "__main__":

    async def main() -> None:
        analytics_agent = DataQualityAgent().get_agent()
        data_agent = DataAgent().get_agent()
        agents = [analytics_agent, data_agent]
        termination = MaxMessageTermination(10)
        #, StructuredMessage[ReportResponse]]
        team = RoundRobinGroupChat(agents, termination_condition=termination, custom_message_types=[StructuredMessage[DataQualityAgentReport], StructuredMessage[DataQualityIssue]])
        print("🔎 Running Analytics Agent test with DataAgent collaboration...")
        await team.reset()  # Reset the team for a new task.
        await Console(team.run_stream(task="Find out 1 data quality issue in RIDEBOOKING table and suggest a fix and then Stop"))  # type: ignore
        print("\n--- Analytics Agent Output ---\n")

    asyncio.run(main())