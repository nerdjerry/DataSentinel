import asyncio
from autogen_agentchat.ui import Console
from DataAgent import DataAgent

if __name__ == "__main__":

    async def main() -> None:
        data_agent = DataAgent().get_agent()
        await Console(data_agent.run_stream(task="Get top 1 row in RIDEBOOKING table"))  # type: ignore

    asyncio.run(main())