from langchain_core.prompts import PromptTemplate  
from dotenv import load_dotenv

load_dotenv()

template = "Expain this concept simply and concisely: {concept}"  
prompt_template = PromptTemplate.from_template(template=template)   
prompt = prompt_template.invoke({"concept": "Prompting LLMs"}) 
print(prompt)