import asyncio
import sys
from pathlib import Path

# Add project root and agent directory to Python path
project_root = Path(__file__).parent.parent.parent
agent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(agent_dir))

from autogen_agentchat.ui import Console
from DataAgent import DataAgent

if __name__ == "__main__":

    async def main() -> None:
        data_agent = DataAgent().get_agent()
        await Console(data_agent.run_stream(task="Get schema for RIDEBOOKING table"))  # type: ignore

    asyncio.run(main())