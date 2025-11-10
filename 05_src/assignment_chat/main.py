from langgraph.graph import StateGraph, MessagesState, START
from langchain.chat_models import init_chat_model
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langchain_core.messages import SystemMessage,  HumanMessage

from dotenv import load_dotenv
import json
import requests
import os

from assignment_chat.prompts import return_instructions
from assignment_chat.tools_job import get_canadian_wage_data
from assignment_chat.tools_living import get_cost_of_living
from assignment_chat.tools_music import recommend_albums

from utils.logger import get_logger


_logs = get_logger(__name__)
load_dotenv(".env")
load_dotenv(".secrets")


chat_agent = init_chat_model(
    "openai:gpt-4o-mini",
)
tools = [get_canadian_wage_data, get_cost_of_living, recommend_albums]

instructions = return_instructions()



# @traceable(run_type="llm")
def call_model(state: MessagesState):
    """LLM decides whether to call a tool or not"""
    response = chat_agent.bind_tools(tools).invoke( [SystemMessage(content=instructions)] + state["messages"])
    return {
        "messages": [response]
    }

def get_graph():
    
    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_node(ToolNode(tools))
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges(
        "call_model",
        tools_condition,
        )
    builder.add_edge("tools", "call_model")
    graph = builder.compile()
    return graph

