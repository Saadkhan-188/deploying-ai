from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
load_dotenv(r"D:\DSI\deploying-ai\05_src\.secrets")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_chatgpt(messages):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages = messages,
        temperature = 0.7
    )
    response_model = response.model_dump()
    print(json.dumps(response_model, indent = 4))

    return response.choices[0].message.content


messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is a typical taco found in Mexico City?"},
    {"role": "assistant", "content": "A typical taco found in Mexico City is the 'Taco al Pastor', which features marinated pork, pineapple, onions, and cilantro on a corn tortilla."},
    {"role": "user", "content": "Can you give me a recipe for it?"}
]

response = ask_chatgpt(messages)
print(response)