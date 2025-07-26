import requests
import os
from dotenv import load_dotenv

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
    "Content-Type": "application/json"
}

data = {
    "model": "gemma2-9b-it",

    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
}

response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

print(response.status_code)
print(response.text)
