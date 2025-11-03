# simple external API wrappers + rewriter# app/services/api_service.py
import httpx
from typing import Tuple

OPEN_METEO = "https://api.open-meteo.com/v1/forecast"

async def fetch_weather(lat: float, lon: float, days:int=1) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,weathercode",
        "forecast_days": days,
        "timezone": "auto"
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(OPEN_METEO, params=params)
        r.raise_for_status()
        return r.json()

def rewrite_weather(api_json: dict) -> str:
    hourly = api_json.get("hourly", {})
    temps = hourly.get("temperature_2m", [])
    times = hourly.get("time", [])
    if not temps:
        return "No weather data."
    n = min(6, len(temps))
    sample = temps[:n]
    avg = sum(sample)/len(sample)
    return f"Short forecast: next {n} hours avg {avg:.1f}°C. Pack layers if temp swings are big."
