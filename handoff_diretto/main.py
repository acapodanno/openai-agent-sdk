import os
from dotenv import load_dotenv
from agents import Agent, Runner, set_default_openai_key
import asyncio

async def main():
    load_dotenv()
    set_default_openai_key(os.getenv("OPENAI_API_KEY"))
    tutor_agent_history = Agent(name="handoff_agent_history",
                                  instructions="You provide assistance historical question. Explain important events and context clearly",
                                  model="gpt-4.1-nano",
                                  handoff_description="You specialize in history and must answer all questions related to it.")
    tutor_agent_philosophy = Agent(
        name="handoff_agent_philosophy",
        handoff_description="You specialize in philosophy and must answer all questions related to it.",
        model="gpt-4.1-nano",
        instructions="You provide help with philosophy questions. Discuss key thinkers, arguments, and schools of thought with clarify."
    )
    triage_agent = Agent(
        name="triage_agent",
        instructions="Determine the agent to respond in the most appropriate manner",
        handoffs= [tutor_agent_history,tutor_agent_philosophy],
        model="gpt-4.1-nano",
    )
    runner = await Runner.run(triage_agent,input("Enter your question:"))
    return runner.final_output

print(asyncio.run(main()))