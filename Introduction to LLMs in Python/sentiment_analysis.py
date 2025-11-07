# remember to install 'torch'
from transformers import pipeline  

generator = pipeline(task="sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

input_text = """ Classify the sentiment of this sentence as either Positive or Negative. 
Example: Text: "I'm feeling great today!" Sentiment: Positive 
Text: "The weather today is lovely." Sentiment:
"""  

result = generator(input_text, max_length=100, truncation=True) 
print(result[0]["label"]) 
