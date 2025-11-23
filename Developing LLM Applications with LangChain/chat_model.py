from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate  
from dotenv import load_dotenv

load_dotenv()

template = ChatPromptTemplate.from_messages([("system", "You are a calculator that responds with math."),
                                             ("human", "Answer this math question: What is two plus two?"),
                                             ("ai", "2+2=4"),
                                             ("human", "Answer this math question: {math}")]) 

llm = ChatOpenAI(model="gpt-4o-mini")  
llm_chain = template | llm 
math='What is five times five?'  
response = llm_chain.invoke({"math": math}) 
print(response.content)