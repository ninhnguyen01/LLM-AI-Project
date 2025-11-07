# remember to install 'torch'
from transformers import pipeline

generator = pipeline(task="text-generation", model="distilgpt2")    
review = "This book was great. I enjoyed the plot twist in Chapter 10."  
response = "Dear reader, thank you for your review."  
prompt = f"Book review:\n{review}\n\nBook shop response to the review:\n{response}"    
output = generator(prompt, max_length=100, pad_token_id=generator.tokenizer.eos_token_id, truncation=True)
print(output[0]["generated_text"])