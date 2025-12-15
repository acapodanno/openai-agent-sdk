import os

from agents.mcp import  MCPServerStreamableHttp
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    set_default_openai_key
)
import asyncio

async def run_agent():
    async with MCPServerStreamableHttp(
        params={
            "url": "http://127.0.0.1:8000/mcp",
            "timeout": 10,
        },
        name="serverStreamableHttp",
        cache_tools_list=False,
        max_retry_attempts=3,
        client_session_timeout_seconds=30
    ) as mcp_server_streamable_http:
        load_dotenv()
        set_default_openai_key(os.getenv("OPENAI_KEY"))
        agent = Agent(
            name="Agent Assistent",
            instructions = "You are assistant helpful person. You use the enable tool if it is neccesary",
            mcp_servers=[mcp_server_streamable_http],
            model="gpt-4o"
        )
        result = await Runner.run(starting_agent=agent,input=input("Enter question:"))
        print(f"result: {result}")

if __name__ == "__main__":
    asyncio.run(run_agent())
