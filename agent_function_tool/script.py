import os
from dotenv import load_dotenv
from agents import Agent, Runner, set_default_openai_key, function_tool
import asyncio

@function_tool
async def findUserById(user_id:str)-> str | None:
    if user_id == "1234":
        return "Alessandro Capodanno"
    elif user_id == "10":
        return "Diego Armando Maradona"
    else:
        return None


async def call_agent():
    load_dotenv()
    set_default_openai_key(os.environ["OPENAI_API_KEY"])
    agent = Agent( name="Hello world",
    instructions="Find the user from id. You can use the tool",
                   model="gpt-4.1-nano",
                   tools=[findUserById],)
    result = await Runner.run(agent,input("Enter answer"))
    return result.final_output
if __name__ == '__main__':
    print(asyncio.run(call_agent()))