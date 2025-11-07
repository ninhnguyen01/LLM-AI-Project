# remember to install 'torch'
from transformers import pipeline

generator = pipeline(task="text-generation", model="distilgpt2")

prompt = "The Gion neighborhood in Kyoto is famous for"

output = generator(prompt, max_length=100, pad_token_id=generator.tokenizer.eos_token_id, truncation=True)

print(output[0]["generated_text"])
