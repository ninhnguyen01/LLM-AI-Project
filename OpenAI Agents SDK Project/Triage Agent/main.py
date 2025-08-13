from dotenv import load_dotenv
load_dotenv()
from agents import Agent, Runner, GuardrailFunctionOutput, InputGuardrail, InputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio

class InquiryOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=InquiryOutput,
    model="gpt-4.1-mini",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    model="gpt-4.1-mini",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
    model="gpt-4.1-mini",
)

async def safety_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(InquiryOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=safety_guardrail),
    ],
    model="gpt-4.1-mini",
)

async def main():
    # Example 1: History question
    try:
        print()
        question_input = input("Enter question: ")
        print()
        if question_input:
            result = await Runner.run(triage_agent, question_input)
            print(result.final_output,"\n")
        elif question_input == "":
            print("Exited the prompt...")
    except InputGuardrailTripwireTriggered as e:
        print("Guardrail blocked this input:", e)   

if __name__ == "__main__":
    asyncio.run(main())