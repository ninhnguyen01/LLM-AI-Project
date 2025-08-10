import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    message: List[Union[HumanMessage, AIMessage]]

llm = ChatOpenAI(model="gpt-4.1-mini")

def process(state: AgentState) -> AgentState:
    """ This node solve input request """
    response = llm.invoke(state["message"])
    state["message"].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

convo_history = []

user_input = input("Enter text: ")
while user_input != "exit":
    convo_history.append(HumanMessage(content=user_input))
    agent.invoke({"message": convo_history})
    print("\n")
    user_input = input("Enter text (to quit, use 'exit'): ")

with open("log.txt", "w") as logFile:
    logFile.write("Conversation log: \n")

    for msg in convo_history:
        if isinstance(msg, HumanMessage):
            logFile.write(f"User Input: {msg.content}\n")
        elif isinstance(msg, AIMessage):
            logFile.write(f"AI Response: {msg.content}\n\n")
    
    logFile.write("End Conversation")

print("Conversation saved to log.txt")