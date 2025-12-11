import os
import asyncio
from dotenv import load_dotenv
from agents import Agent,Runner, set_default_openai_key


async def create_agent():
    load_dotenv()
    set_default_openai_key(os.getenv('OPENAI_KEY'))
    tutor_agent_history_as_tool = Agent(
        name="tutor_agent_history",
        instructions="You provide assistance historical question. Explain important events and context clearly",
        model="gpt-4.1-nano"
    ).as_tool(tool_name="tutor_agent_history_as_tool",tool_description="You specialize in history and must answer all questions related to it.")
    tutor_agent_philosophy_as_tool = Agent(
        name="tutor_agent_philosophy",
        model="gpt-4.1-nano",
        instructions="You provide help with philosophy questions. Discuss key thinkers, arguments, and schools of thought with clarify."
    ).as_tool(tool_name="tutor_agent_philosophy_as_tool", tool_description="You provide help with philosophy questions. Discuss key thinkers, arguments, and schools of thought with clarify.")
    triage_agent = Agent(
        name="triage_agent",
        model="gpt-4.1-nano",
        tools=[tutor_agent_history_as_tool, tutor_agent_philosophy_as_tool],
        instructions="Determine the tool to respond in the most appropriate manner"
    )
    result = await Runner.run(triage_agent,input("Enter question:"))
    return result.final_output

print(asyncio.run(create_agent()))
