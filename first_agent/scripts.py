import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, set_default_openai_key

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


async def main():
    name = input("Insert your name: ")
    set_default_openai_key(openai_api_key)
    agent = Agent(name="My agent", model='gpt-4.1-nano', instructions="You are a helpful agent.")
    result = await Runner.run(agent, f"Hi, my name is {name}.")
    return result.final_output


print(asyncio.run(main()))
