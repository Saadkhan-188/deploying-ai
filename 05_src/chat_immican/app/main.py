# FastAPI entry
# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.semantic_service import SemanticService
from app.services.api_service import fetch_weather, rewrite_weather
from app.services.function_service import execute
from app.memory_manager import compress_messages
import asyncio

app = FastAPI(title="Immican Chat Backend")

semantic = SemanticService()

class ChatReq(BaseModel):
    session_id: str
    message: str

class WeatherReq(BaseModel):
    lat: float
    lon: float

class ActionReq(BaseModel):
    action: dict

# in-memory sessions for demo
SESSIONS = {}

def get_session(sid):
    if sid not in SESSIONS:
        SESSIONS[sid] = {"messages": []}
    return SESSIONS[sid]

@app.post("/chat")
async def chat(req: ChatReq):
    sess = get_session(req.session_id)
    sess["messages"].append({"role":"user","text":req.message})
    # compress if needed
    sess["messages"] = compress_messages(sess["messages"])
    # route intents (naive)
    txt = req.message.lower()
    if txt.startswith("weather"):
        # expects "weather lat lon"
        parts = txt.split()
        try:
            lat = float(parts[1]); lon=float(parts[2])
        except:
            raise HTTPException(status_code=400, detail="invalid coords")
        api_j = await fetch_weather(lat, lon)
        rep = rewrite_weather(api_j)
        sess["messages"].append({"role":"assistant","text":rep})
        return {"reply": rep}
    if txt.startswith("schedule"):
        # simulate assistant producing function action: here we parse and execute directly
        action = {"action":"schedule_appointment","title":"Appointment","when":"2025-11-10T14:00","duration_minutes":30}
        res = execute(action)
        sess["messages"].append({"role":"assistant","text":str(res)})
        return {"reply": res}
    # fallback -> semantic
    ans = semantic.answer(req.message)
    sess["messages"].append({"role":"assistant","text":ans})
    return {"reply": ans}

@app.post("/semantic/query")
async def semantic_query(q: str):
    return semantic.query(q, k=3)

@app.post("/function/execute")
async def function_execute(req: ActionReq):
    return execute(req.action)
