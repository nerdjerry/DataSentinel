import asyncio
import sys
from pathlib import Path


from autogen_agentchat.ui import Console
from agent.DataAgent import DataAgent, DataAgentReport

if __name__ == "__main__":

    async def main() -> None:
        data_agent = DataAgent().get_agent()
        await Console(data_agent.run_stream(task="Find duplicate BOOKING_ID entries and summarize duplicates (count of duplicate IDs, sample rows) to assess whether duplicates distort distance/value/rating relationships."))  # type: ignore

    asyncio.run(main())