# Simple Chat Implementation

This simple chat app, establishes a connection with OpenAI's chat API, but using a local Gradio interface. The intent is to demonstrate how to interact with the Chat Interface provided by Gradio.

To run the server:
python animals_chat/app.py

2025-11-09 - Modification (Optional)
def should_continue(state: MessagesState) -> Literal["tool_node", END]: // Original line
def should_continue(state: MessagesState) -> Literal["tool_node", "END"]: // Modified line
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

✔