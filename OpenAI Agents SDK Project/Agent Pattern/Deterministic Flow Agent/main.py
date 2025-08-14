import asyncio
from pydantic import BaseModel
from agents import Agent, Runner, trace
from dotenv import load_dotenv
load_dotenv()

""" Deterministic Flow - each step is performed by an agent. """

# Step 1. The 1st agent - generation
story_outline_agent = Agent(
    name="story_outline_agent",
    instructions="Generate a very short story outline based on the user's input.",
    model="gpt-4.1-mini",
)

# Step 2. 1st agent -> action ->  2nd agent
class OutlineCheckerOutput(BaseModel):
    good_quality: bool
    is_folklore: bool

# Step 3. 2nd agent - quality assurance
outline_checker_agent = Agent(
    name="outline_checker_agent",
    instructions="Read the given story outline, and judge the quality. Also, determine if it is a folklore story.",
    output_type=OutlineCheckerOutput,
    model="gpt-4.1-mini",
)

# Step 4. The third agent - perform action
story_agent = Agent(
    name="story_agent",
    instructions="Write a short story based on the given outline.",
    output_type=str,
    model="gpt-4.1-mini",
)

async def main():
    print()
    input_prompt = input("What kind of story do you want? ")

    # Ensure the entire workflow is a single trace
    with trace("Deterministic story flow"):
        # 1. Generate an outline
        outline_result = await Runner.run(
            story_outline_agent,
            input_prompt,
        )
        print()
        print("Outline generated")

        # 2. Check the outline
        outline_checker_result = await Runner.run(
            outline_checker_agent,
            outline_result.final_output,
        )

        # 3. Add a gate to stop if the outline is not good quality or not a folklore story
        assert isinstance(outline_checker_result.final_output, OutlineCheckerOutput)
        if not outline_checker_result.final_output.good_quality:
            print()
            print("Outline is not good quality, so we stop here.", "\n")
            exit(0)

        if not outline_checker_result.final_output.is_folklore:
            print()
            print("Outline is not a folklore story, so we stop here.", "\n")
            exit(0)

        print("Outline is good quality and a folklore story, so we continue to write the story.","\n")

        # 4. Write the story
        story_result = await Runner.run(
            story_agent,
            outline_result.final_output,
        )

        print(f"Story: {story_result.final_output}")
        print()


if __name__ == "__main__":
    asyncio.run(main())