import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key='')
 
classification_prompt = """ Classify this customer feedback into categories:  
Product Issue, Shipping Problem, Billing Question, or General Inquiry Feedback: 
"My order arrived damaged  and I need a replacement" """ 

response = client.messages.create( model="..", 
                                  max_tokens=150,  
                                  messages=[{"role": "user", "content": classification_prompt}])