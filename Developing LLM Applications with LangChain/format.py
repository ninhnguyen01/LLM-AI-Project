from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate  
from dotenv import load_dotenv

load_dotenv()

example_prompt = PromptTemplate.from_template("Question: {question}\n{answer}") 
prompt = example_prompt.invoke({"question": "What is the capital of Italy?",
                                "answer": "Rome"}) 
print(prompt.text)