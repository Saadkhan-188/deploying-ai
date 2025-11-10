import asyncio
import gradio as gr
from fastmcp import Client
from dotenv import load_dotenv
import os
from utils.logger import get_logger

load_dotenv()
_logs = get_logger(__name__)

# MCP client
mcp_url = os.getenv("MCP_URL")
client = Client(mcp_url)


async def fetch_weather(city: str):
    """Call the MCP weather_service tool and return a user-friendly string."""
    async with client:
        result = await client.call_tool("weather_service", {"location": city})
        data = result.data
        return f"The weather in {city}:\n🌡 Temperature: {data.temperature}°C\n💧 Humidity: {data.humidity}%\n💨 Wind Speed: {data.wind_speed} m/s"


def chatbot_interface(user_message, history):
    """Gradio callback for the chatbot interface."""
    if history is None:
        history = []

    # First message: greeting
    if not history:
        greeting = (
            "Hi! I am your Weather Bot 🌤️, here to enhance your living experience. "
            "Which city would you like the weather for?"
        )
        history.append(("Weather Bot", greeting))
        return "", history

    # Fetch weather for user input
    city = user_message.strip()
    weather_text = asyncio.run(fetch_weather(city))
    history.append((user_message, weather_text))
    return "", history


# Gradio interface
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox(
        label="Enter city",
        placeholder="Type your city here...",
    )
    msg.submit(chatbot_interface, [msg, chatbot], [msg, chatbot])

demo.launch()
