### Service 2: Detailed Cost of Living Data

# + This tool provides access to detailed cost of living
#   data from the specialized third-party API
#   provided by the user.
# + It requires the specific API key and host.
# + The tool node will call `get_cost_of_living_by_country`.
# + This tool provides a country-level summary of costs.

from langchain.tools import tool
import requests
import json

# Make sure your `utils.logger` path is correct
from utils.logger import get_logger

_logs = get_logger(__name__)

# --- RapidAPI Configuration (from user snippet) ---

# use this API key for testing, its hard to navigate for this exact dataset
# _RAPIDAPI_KEY = "2f63dfb106mshfbe1cd79b3eab1bp104ab7jsn65bb20699552"

_RAPIDAPI_KEY = "2f63dfb106mshfbe1cd79b3eab1bp104ab7jsn65bb20699552"
_RAPIDAPI_HOST = "cities-cost-of-living-and-average-prices-api.p.rapidapi.com"
_BASE_URL = "https://cities-cost-of-living-and-average-prices-api.p.rapidapi.com/cost_of_living"


@tool
def get_cost_of_living_by_country(country: str) -> str:
    """
    Fetches detailed cost of living data for a specific country.
    The API call is to https://cities-cost-of-living-and-average-prices-api.p.rapidapi.com/cost_of_living
    and takes 'country' as a parameter.
    Example: get_cost_of_living_by_country("Canada")
    """
    _logs.debug(f"Requesting cost of living data for country: '{country}'")
    
    if _RAPIDAPI_KEY == "YOUR_API_KEY_HERE":
        _logs.error("RapidAPI Key is not set in tools_living.py.")
        return "Error: The Cost of Living API key is not configured by the developer."
        
    response = get_living_cost_from_service(country)
    costs = get_living_cost_from_response(country, response)
    _logs.debug(f"Cost of living result: {costs}")
    return costs


def get_living_cost_from_service(country: str) -> requests.Response:
    """
    Hits the RapidAPI Cost of Living endpoint with 'country' parameter.
    """
    querystring = {"country": country}
    headers = {
        "X-RapidAPI-Key": _RAPIDAPI_KEY,
        "X-RapidAPI-Host": _RAPIDAPI_HOST
    }
    
    # This call is intentionally left without error handling
    # to match the provided get_horoscope_from_service style.
    response = requests.get(_BASE_URL, headers=headers, params=querystring)
    return response


def get_living_cost_from_response(country: str, response: requests.Response) -> str:
    """
    Parses the JSON response from the cost of living API.
    """
    # This parsing style matches the horoscope example.
    # It assumes the request was successful and the response is valid JSON.
    try:
        resp_dict_list = json.loads(response.text)
    except json.JSONDecodeError:
        _logs.error(f"Failed to decode JSON from response: {response.text}")
        return "Error: Received an invalid (non-JSON) response from the API."

    # The API returns a list. We'll check if it's a list and has items.
    if not isinstance(resp_dict_list, list) or len(resp_dict_list) == 0:
        return f"No data found for '{country}'. Please check the country name."
        
    # Get the first item, or an empty dict to prevent crashes
    data = resp_dict_list[0] or {}
    
    # Safe access using .get()
    country_name = data.get('country', country)
    rent1b = data.get('rent_1_bedroom_city_center', 'N/A')
    rent3b = data.get('rent_3_bedrooms_city_center', 'N/A')
    milk = data.get('milk_1_liter', 'N/A')
    bread = data.get('bread_1_loaf', 'N/A')
    salary = data.get('average_monthly_net_salary_after_tax', 'N/A')

    # Format the final string
    summary = [
        f"Cost of Living Summary for {country_name} (in USD):",
        
        f"\n  Average Monthly Rent:",
        f"    - 1 bedroom in city centre: ${rent1b}",
        f"    - 3 bedroom in city centre: ${rent3b}",
        
        f"\n  Groceries:",
        f"    - 1L Milk: ${milk}",
        f"    - Loaf of Bread: ${bread}",
        
        f"\n  - Average Monthly Net Salary (After Tax): ${salary}"
    ]
    return "\n".join(summary)