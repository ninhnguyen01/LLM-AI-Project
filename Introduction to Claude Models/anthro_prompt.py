import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key='')

# Summarization prompt 
prompt = """Please summarize the  following text in 2-3 sentences: {project_report}. 
Focus on project  updates.
""" 
response = client.messages.create(model="claude-sonnet-4-20250514", 
                                  max_tokens= 150,
                                  temperature=0.7,
                                  messages=[{"role": "system", "content": prompt}, 
                                            {"role": "user", "content": "Rewrite: [content]"}], 
                                  system_message = """You are a professional editor who rewrites content in a clear, 
                                  engaging style."""  )
