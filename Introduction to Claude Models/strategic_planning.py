import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key='')

user_prompt = "Think through this business decision: Should we launch our new product in Q1 or Q2?" 
response = client.messages.create(model="claude-2",
                                  messages=[{"role": "user",
                                             "content": user_prompt}],
                                             thinking={"type": "enabled",
                                                       "budget_tokens": 1024}, 
                                                       max_tokens=1300)