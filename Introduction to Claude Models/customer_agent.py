import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key='')

system_msg = """ You're a helpful customer service agent.
Be polite, concise, and  always end with asking if there's anything else you can help with."""  
customer_query = "I can't log into my account and getting an error message"  

response = client.messages.create( model="..", 
                                  max_tokens=150,  
                                  system=system_msg, 
                                  messages=[{"role": "user", "content": customer_query}])