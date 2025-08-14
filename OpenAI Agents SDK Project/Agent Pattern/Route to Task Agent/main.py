import asyncio
import uuid
from openai.types.responses import ResponseContentPartDoneEvent, ResponseTextDeltaEvent
from agents import Agent, RawResponsesStreamEvent, Runner, TResponseInputItem, trace
from dotenv import load_dotenv
load_dotenv()

"""
Handoffs/routing pattern

1) The triage agent receives the first message
2) Hands off to the appropriate agent based on the language of the request. 
3) Responses are streamed to the user.
"""

french_agent = Agent(
    name="french_agent",
    instructions="You only speak French",
    model="gpt-4.1-mini",
)

german_agent = Agent(
    name="german_agent",
    instructions="You only speak German",
    model="gpt-4.1-mini",
)

english_agent = Agent(
    name="english_agent",
    instructions="You only speak English",
    model="gpt-4.1-mini",
)

triage_agent = Agent(
    name="triage_agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    model="gpt-4.1-mini",
    handoffs=[french_agent, german_agent, english_agent],
)


async def main():
    # create an ID for this conversation, so we can link each trace
    conversation_id = str(uuid.uuid4().hex[:16])

    print()

    """ Whichever language you use to ask your first question to the AI model, it will use only that language.
    However, depending on your first question and the continous conversation, the AI model may still reroute
    to the other task agent (lang agent) based on my testing, which was modifying the 'instructions' in the agent and the 
    input in the 'msg' variable """

    msg = input("Hi! We speak French, German, and English. How can I help? ")
    agent = triage_agent
    inputs: list[TResponseInputItem] = [{"content": msg, "role": "user"}]

    while True:
        # Each conversation turn is a single trace. 
        # Normally, each input from the user would be an API request to your app and you can wrap the request in a trace()
        with trace("Routing example", group_id=conversation_id):
            result = Runner.run_streamed(
                agent,
                input=inputs,
            )
            async for event in result.stream_events():
                if not isinstance(event, RawResponsesStreamEvent):
                    continue
                data = event.data
                if isinstance(data, ResponseTextDeltaEvent):
                    print(data.delta, end="", flush=True)
                elif isinstance(data, ResponseContentPartDoneEvent):
                    print("\n")

        inputs = result.to_input_list()
        print("\n")

        user_msg = input("Enter a message ('exit' to quit): ")

        if user_msg == "exit":
            exit(0)

        inputs.append({"content": user_msg, "role": "user"})
        agent = result.current_agent


if __name__ == "__main__":
    asyncio.run(main())