import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
load_dotenv(r"D:\DSI\deploying-ai\05_src\.secrets")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

from pydantic import BaseModel

class TacoInfo(BaseModel):
    answer_text: str                # <-- conversational explanation
    taco_name: str
    common_fillings: list[str]
    typical_location: str


client = OpenAI(api_key=OPENAI_API_KEY)

def ask_chatgpt(user_message):
    response = client.responses.parse(
        model="gpt-4o",
        input=[
            {"role": "system", "content": "You are TacoAI, an expert assistant in Taco. First, answer conversationally in a friendly tone then fill structured fields. If question not clear, ask to rephrase the question."},
            {"role": "user", "content": user_message}
        ],
        schema=TacoInfo,                      # <-- This is key
        temperature=0.3                       # Lower temp for reliability
    )
    return response.output

user = "What is a typical taco found in Toronto City?"

response = ask_chatgpt(user)
result = response.output_text

print("\n--- Structured Data ---\n")
print(result.model_dump_json(indent=2))