from dotenv import load_dotenv
load_dotenv()
from agents import Agent, Runner

# name your agent, instruct its purpose, pick model
agent = Agent(name="Assistant", instructions="You are a programmer assistant", model="gpt-4.1-mini")

# enter prompt from input_prompt variable
print()

# simple task programming agent
def program_agent():
    """ Function to invoke agent """
    """ This AI agent WILL NOT remember your previous conversation """
    """ Therefore, make your single question/instruction as detail as possible """
    
    input_prompt = input("Enter prompt or 'exit': ")

    if input_prompt != "exit":
        result = Runner.run_sync(agent, input_prompt)
        print()
        print(result.final_output)
        if result.final_output != "":
            print()
            program_agent()

program_agent()