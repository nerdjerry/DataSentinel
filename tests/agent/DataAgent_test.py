import asyncio
import sys
from pathlib import Path


from autogen_agentchat.ui import Console
from agent.DataAgent import DataAgent

if __name__ == "__main__":

    async def main() -> None:
        data_agent = DataAgent().get_agent()
        await Console(data_agent.run_stream(task="Compute total rows and counts/percentages of NULL or non-parsable 'null' string values for BOOKING_VALUE, RIDE_DISTANCE, and CUSTOMER_RATING (account for known 'null' string issue using TRY_CAST or equivalent)."))  # type: ignore

    asyncio.run(main())