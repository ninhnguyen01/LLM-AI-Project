# remember to install 'torch'
from transformers import pipeline

translator = pipeline(task="translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es")  
text = "Walking amid Gion's Machiya wooden houses was a mesmerizing experience."  
output = translator(text, clean_up_tokenization_spaces=True)  
print(output[0]["translation_text"])