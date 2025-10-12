import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from autogen_agentchat.ui import Console
from agent.DataAgent import DataAgent

if __name__ == "__main__":

    async def main() -> None:
        data_agent = DataAgent().get_agent()
        await Console(data_agent.run_stream(task="Get schema for RIDEBOOKING table"))  # type: ignore

    asyncio.run(main())