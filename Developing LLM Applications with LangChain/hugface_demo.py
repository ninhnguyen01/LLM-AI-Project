from langchain_huggingface import HuggingFacePipeline  
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFacePipeline.from_model_id(model_id="",
                                        task="text-generation",
                                        pipeline_kwargs={"max_new_tokens": 100} )

response = llm.invoke("What is Hugging Face?")
print(response)  