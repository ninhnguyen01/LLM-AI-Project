import os
from google import genai
from tool_use import *
from dotenv import load_dotenv
load_dotenv()

class Agent:
    def __init__(self, model: str, tools: dict, system_instruction: str = "You are a helpful assistant."):
        self.model = model
        self.client = genai.Client(api_key=os.getenv("Gemini_API_Key"))
        self.last_interaction_id = None
        self.tools = tools
        self.system_instruction = system_instruction
 
    def run(self, contents: str | list):
        response = self.client.interactions.create(
            model=self.model,
            input=contents,
            system_instruction=self.system_instruction,
            tools=[tool["definition"] for tool in self.tools.values()],
            previous_interaction_id=self.last_interaction_id
        )
        self.last_interaction_id = response.id

        tool_results = []
        for output in response.outputs:
            if output.type == "function_call":
                print(f"[Function Call] {output.name}({output.arguments})")
                
                if output.name in self.tools:
                    result = self.tools[output.name]["function"](**output.arguments)
                else:
                    result = "Error: Tool not found"
                
                print(f"[Function Response] {result}")
                tool_results.append({
                    "type": "function_result",
                    "call_id": output.id,
                    "name": output.name,
                    "result": str(result)
                })
        
        # If there were tool calls, send results back to the model
        if tool_results:
            return self.run(tool_results)
        
        return response
 
agent = Agent(model="gemini-3-flash-preview", tools=file_tools, system_instruction="You are a helpful Coding Assistant. Respond like you are Linus Torvalds.")

print("Agent ready. Ask it to check files in this directory.")
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break
 
    response = agent.run(user_input)
    print(f"Linus: {response.outputs[-1].text}\n")

response = agent.run(
    contents="Can you list my files in the current directory?"
)

# Output: Function call: list_dir with arguments {'directory_path': '.'}
for output in response.outputs:
    if output.type == "function_call":
        print(f"Function call: {output.name} with arguments {output.arguments}")

response1 = agent.run(
    contents="Hello, What are top 3 cities in California to visit? Only return the names of the cities."
)

# City Output 1
print(f"Model: {response1.outputs[-1].text}")
 
response2 = agent.run(
    contents="Tell me something about the second city."
)

# City Output 2
print(f"Model: {response2.outputs[-1].text}")
