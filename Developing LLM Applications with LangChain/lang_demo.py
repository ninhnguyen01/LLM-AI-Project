from langchain_openai import ChatOpenAI 
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", max_completion_tokens=256, temperature=0.3)   
response = llm.invoke("What is LangChain?")
print(response)