import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
load_dotenv(r"D:\DSI\deploying-ai\05_src\.secrets")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_chatgpt(user_message):
    response = client.responses.create(
        model = "gpt-4o",
        input = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        temperature = 0.7
    )
    return response

user = "What is a typical taco found in Mexico City?"

response = ask_chatgpt(user)
print(response.output_text)