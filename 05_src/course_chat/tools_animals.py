### Service 1: API Calls

# + There are a few API calls that we implemented 
# throughout the course. They are organized in 
# tools_animals.py and tool_horoscope.py. 

# + Each tool is imported to main and included in 
# the list `tools`.

# + The tools node uses LangGraph's `ToolNode` class and 
# `tools_condition` is the standard tool stopping criteria.

# + All restrictions and tone requirements are 
# in the instructions prompt. You can find this in prompts.py.


from langchain.tools import tool
import json
import requests

from utils.logger import get_logger

_logs = get_logger(__name__)

@tool
def get_cat_facts(n: int = 1) -> str:
    """
    Fetches n cat facts from the Meowfacts API.
    """
    _logs.debug(f"Requesting {n} cat facts.")
    response = _get_cat_facts_from_service(n)
    facts = _extract_cat_facts_from_response(response)
    _logs.debug(f"Returning cat facts:\n{facts}")
    return facts


def _get_cat_facts_from_service(n: int):
    url = "https://meowfacts.herokuapp.com/"
    params = {"count": n}
    
    response = requests.get(url, params=params)
    return response


def _extract_cat_facts_from_response(response: requests.Response) -> str:
    try:
        resp_dict = json.loads(response.text)
        facts_list = resp_dict.get("data", [])
        facts = "\n".join([f"{i+1}. {fact}\n" for i, fact in enumerate(facts_list)])
        return facts if facts else "No cat facts found."
    except Exception as e:
        _logs.error(f"Error parsing cat facts: {e}")
        return "Unable to retrieve cat facts at this time."


@tool
def get_dog_facts(n: int = 1) -> str:
    """
    Fetches n dog facts from the Dog API.
    """
    _logs.debug(f"Requesting {n} dog facts.") 
    response = _get_dog_facts_from_service(n)
    facts = _extract_dog_facts_from_response(response)
    _logs.debug(f"Returning dog facts:\n{facts}")
    return facts


def _get_dog_facts_from_service(n: int):
    url = "http://dogapi.dog/api/v2/facts"
    params = {"limit": n}
    
    response = requests.get(url, params=params)
    return response


def _extract_dog_facts_from_response(response: requests.Response) -> str:
    try:
        resp_dict = json.loads(response.text)
        facts_list = resp_dict.get("data", [])
        facts = "\n".join([f"{i+1}. {fact['attributes']['body']}\n" for i, fact in enumerate(facts_list)])
        return facts if facts else "No dog facts found."
    except Exception as e:
        _logs.error(f"Error parsing dog facts: {e}")
        return "Unable to retrieve dog facts at this time."

# @tool
# def get_cat_facts(n:int=1):
#     """
#     Returns n cat facts from the Meowfacts API.
#     """
#     url = "https://meowfacts.herokuapp.com/"
#     params = {
#         "count": n
#     }
#     response = requests.get(url, params=params)
#     resp_dict = json.loads(response.text)
#     facts_list = resp_dict.get("data", [])
#     facts = "\n".join([f"{i+1}. {fact}\n" for i, fact in enumerate(facts_list)])
#     return facts

# @tool
# def get_dog_facts(n:int=1):
#     """
#     Returns n dog facts from the Dog API.
#     """
#     url = "http://dogapi.dog/api/v2/facts"
#     params = {
#         "limit": n
#     }
#     response = requests.get(url, params=params)
#     resp_dict = json.loads(response.text)
#     facts_list = resp_dict.get("data", [])
#     facts = "\n".join([f"{i+1}. {fact['attributes']['body']}\n" for i, fact in enumerate(facts_list)])
#     return facts
