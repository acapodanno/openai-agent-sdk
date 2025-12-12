import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, RunContextWrapper, Runner, \
    TResponseInputItem, input_guardrail, set_default_openai_key
from pydantic import BaseModel, Field
load_dotenv()
set_default_openai_key(os.getenv('OPENAI_KEY'))

class DangerOutput(BaseModel):
    is_dangerous: bool = Field("True if the input is dangerous or unsafe. False otherwise")
    reasoning: str = Field("Reasoning of the input why it is dangerous")

@input_guardrail
async def agent_input_guardrail(ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    guardrail_agent = Agent(
        name="guardrail_agent",
        model="gpt-4.1-nano",
        instructions="Check if the user is asking abount something dangerous",
        output_type=DangerOutput
    )
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_dangerous
    )
async def create_agent():


    triage_agent = Agent(
        name="triage_agent",
        model="gpt-4.1-nano",
        instructions="You are a helpful agent",
        input_guardrails=[
            agent_input_guardrail
        ]
    )
    result = await Runner.run(triage_agent, input("Enter question:"))
    return result.final_output


try:
    print(asyncio.run(create_agent()))
except InputGuardrailTripwireTriggered as e:
    print(e.guardrail_result.output.output_info.reasoning)
