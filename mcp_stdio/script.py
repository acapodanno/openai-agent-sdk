import math
import os

from agents.mcp import MCPServerStdio
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    set_default_openai_key
)
import asyncio
from fastmcp import Client

mcp_server = {
    "serverStdio": {
        "args": ["mcp_server_stdio.py"],
        "command": "python",
        "transport": "stdio"
    }
}


async def mcp_client_stdio():
    async with Client(mcp_server) as client:
        tools = await client.list_tools()
        for tool in tools:
            print(f"{tool.name}: {tool.description}")


async def mcp_client_stdio_test_call_tool():
    async with Client(mcp_server) as client:
        result = await client.call_tool("get_user_by_id", {"user_id": "123"})
        print(f"result: {result.data}")

async def run_agent():
    async with MCPServerStdio(
        params={ "args": ["mcp_server_stdio.py"],
        "command": "python"},
        name="serverStdio",
        client_session_timeout_seconds=30
    ) as mcp_server_stdio:
        load_dotenv()
        set_default_openai_key(os.getenv("OPENAI_KEY"))
        agent = Agent(
            name="Agent Assistent",
            instructions = "You are assistant helpful person. You use the enable tool if it is neccesary",
            mcp_servers=[mcp_server_stdio],
            model="gpt-4o"
        )
        result = await Runner.run(starting_agent=agent,input=input("Enter question:"))
        print(f"result: {result}")

if __name__ == "__main__":
    asyncio.run(mcp_client_stdio())
    asyncio.run(mcp_client_stdio_test_call_tool())
    asyncio.run(run_agent())
