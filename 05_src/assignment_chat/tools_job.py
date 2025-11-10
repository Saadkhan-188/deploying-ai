### Service 2: Official Canadian Wage Data

# + This tool provides access to the Government of Canada's
#   official wage data, published on the Open Data portal.
# + It queries the CKAN API for the "Wages - 2024" dataset.
# + The tool node will call `get_canadian_wage_data`.
# + This tool is more advanced as it queries a specific,
#   non-obvious government database (CKAN) and parses
#   its specific JSON structure.

from langchain.tools import tool
import requests
import json
import urllib.parse

# Make sure your `utils.logger` path is correct
from utils.logger import get_logger

_logs = get_logger(__name__)

# --- CKAN API Configuration ---
# This is the unique ID for the "2024 Wages" data table
# Found on: https://open.canada.ca/data/en/dataset/adad580f-76b0-4502-bd05-20c125de9116

_RESOURCE_ID = "d16e10ea-77bf-4db8-bdb5-adc709e6cada"
_BASE_URL = "https://open.canada.ca/data/api/3/action/datastore_search"


@tool
def get_canadian_wage_data(job_title: str, province_abbr: str) -> str:
    """
    Fetches official wage data (low, median, high, average) for a specific 
    job title and province from the Government of Canada's Open Data portal.
    The API call is to https://open.canada.ca/data/api/3/action/datastore_search
    and takes parameters 'resource_id', 'q' (for job_title), and 'filters' (for province_abbr).
    Accepted values for province_abbr are 2-letter codes (e.g., 'ON', 'BC', 'QC').
    Example: get_canadian_wage_data("Software developer", "BC")
    """
    _logs.debug(f"Requesting wage data for '{job_title}' in {province_abbr}")
    response = _get_wages_from_service(job_title, province_abbr)
    wages = _get_wages_from_response(job_title, province_abbr, response)
    _logs.debug(f"Wage data result: {wages}")
    return wages


def _get_wages_from_service(job_title: str, province_abbr: str):
    """
    Hits the Government of Canada's CKAN API for wage data.
    """
    # CKAN API requires filters to be a JSON string,
    # and 'q' for full-text search.
    params = {
        "resource_id": _RESOURCE_ID,
        "limit": 5,  # Get top 5 matches
        "filters": json.dumps({
            "prov": province_abbr.upper()
        }),
        "q": job_title  # The full-text search query
    }
    
    response = requests.get(_BASE_URL, params=params)
    return response


def _get_wages_from_response(job_title: str, province_abbr: str, response: requests.Response) -> str:
    """
    Parses the complex JSON response from the CKAN API.
    """
    try:
        resp_dict = json.loads(response.text)
        
        if not resp_dict.get("success"):
            _logs.error(f"CKAN API error: {resp_dict.get('error')}")
            return f"Error from data portal: {resp_dict.get('error')}"
            
        records = resp_dict.get("result", {}).get("records", [])
        
        if not records:
            return f"No wage data found for '{job_title}' in {province_abbr}. Try a broader job title (e.g., 'developer')."
        
        # Format the results nicely
        results = [
            f"Wage data for '{job_title}' in {province_abbr.upper()} (closest matches):"
        ]
        
        for record in records:
            # These field names come from the dataset's data dictionary
            title = record.get('NOC_Title_eng')
            noc = record.get('NOC_CNP')
            low = record.get('Low_Wage_Salaire_Minium', 'N/A')
            median = record.get('Median_Wage_Salaire_Median', 'N/A')
            high = record.get('High_Wage_Salaire_Maximal', 'N/A')
            avg = record.get('Average_Wage_Salaire_Moyen', 'N/A')
            
            results.append(
                f"\n  - Title: {title} (NOC: {noc})"
                f"\n    Hourly Wages: Low: ${low}, Median: ${median}, High: ${high}, Average: ${avg}"
            )
            
        return "\n".join(results)
        
    except Exception as e:
        _logs.error(f"Error parsing wage data: {e}")
        return "Unable to retrieve wage data at this time."