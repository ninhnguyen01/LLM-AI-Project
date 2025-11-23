from langchain_openai import ChatOpenAI 
from langchain_core.prompts import PromptTemplate  
from dotenv import load_dotenv

load_dotenv()

destination_prompt = PromptTemplate(input_variables=["destination"],
                                    template="I am planning a trip to {destination}. \
                                        Can you suggest some activities to do there?" )   

activities_prompt = PromptTemplate(input_variables=["activities"],
                                   template="I only have one day, \
                                    so can you create an itinerary from your top three activities: {activities}." )   
 
llm = ChatOpenAI(model="gpt-4.1-mini"
                 )    
seq_chain = ({"activities": destination_prompt | llm }  
    | activities_prompt | llm) 

print(seq_chain.invoke({"destination": "Rome"}))