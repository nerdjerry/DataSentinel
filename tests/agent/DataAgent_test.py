import asyncio
import sys
from pathlib import Path


from autogen_agentchat.ui import Console
from agent.DataAgent import DataAgent

if __name__ == "__main__":

    async def main() -> None:
        data_agent = DataAgent().get_agent()
        await Console(data_agent.run_stream(task="Identify nulls"))  # type: ignore

    asyncio.run(main())