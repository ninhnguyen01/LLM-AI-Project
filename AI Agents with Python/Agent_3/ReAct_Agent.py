from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_core.messages import ToolMessage
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b:int):
    """ Addition function """

    return a + b 

@tool
def subtract(a: int, b: int):
    """ Subtraction function """

    return a - b

@tool
def multiply(a: int, b: int):
    """ Multiplication function """
    
    return a * b

tools = [add, subtract, multiply]

model = ChatOpenAI(model="gpt-4.1-mini").bind_tools(tools)

def model_call(state:AgentState) -> AgentState:
    system_prompt = SystemMessage(content=
        "You're my AI assistant, wait for input."
    )
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}

def prompt_continue(state: AgentState): 
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls: 
        return "end"
    else:
        return "continue"

graph = StateGraph(AgentState)
graph.add_node("your_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("your_agent")

graph.add_conditional_edges(
    "your_agent",
    prompt_continue,
    {
        "continue": "tools",
        "end": END,
    },
)

graph.add_edge("tools", "your_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("user", "Add 5 + 2. Sutract 7 - 3. Multiply 10 * 2. Also tell me the latest LLM models for AI.")]}
print_stream(app.stream(inputs, stream_mode="values"))