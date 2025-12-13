import os
from dotenv import load_dotenv
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    output_guardrail,
    set_default_openai_key, MessageOutputItem, OutputGuardrailTripwireTriggered,
)
import asyncio
from pydantic import BaseModel, Field

load_dotenv()
set_default_openai_key(os.environ["OPENAI_API_KEY"])
class MessageOutput(BaseModel):
    response: str
class MathHomeworkOutput(BaseModel):
    is_math_homework: bool = Field("Is Math Homework")
    reasoning: str = Field("Reason for Math Homework")
@output_guardrail
async def math_homework_output(
    ctx:RunContextWrapper,
        agent: Agent,
        output:MessageOutput
)-> GuardrailFunctionOutput:
    math_guardrail_agent = Agent(
        name="Guardrail check",
        instructions="Check if the output includes any math.",
        output_type=MathHomeworkOutput,
    )
    result = await Runner.run(math_guardrail_agent, output.response, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )

async def call_agent():
    triage_agent = Agent(
        name="Customer support agent",
        instructions="You are a customer support agent. You help customers with their questions.",
        output_guardrails=[math_homework_output],
        output_type=MessageOutput,
    )
    result = await Runner.run(triage_agent,input("Enter question: "))
    return result.final_output
if __name__ == '__main__':
    try:
        print(asyncio.run(call_agent()))
    except OutputGuardrailTripwireTriggered as e:
        print(e.guardrail_result.output.output_info.reasoning)
