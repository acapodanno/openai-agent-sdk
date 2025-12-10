from user import User
import os
from dotenv import load_dotenv
from agents import Agent,Runner, set_default_openai_key
import asyncio
async def main():
    load_dotenv()
    set_default_openai_key(os.getenv("OPENAI_API_KEY"))
    agent = Agent(name="Extraced information", instructions="Analize and extraction information from text", output_type=User,
                  model="gpt-4.1-nano")
    runner = await  Runner.run(agent,input("Enter text to analize:"))
    return runner.final_output

print(asyncio.run(main()))
