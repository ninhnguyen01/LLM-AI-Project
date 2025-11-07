import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key='')

# prompt
response = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=100, 
                                  messages=[{"role": "user",
                                             "content": "What websites do you recommend to learn Claude?"}])

print(response.content[0].text)