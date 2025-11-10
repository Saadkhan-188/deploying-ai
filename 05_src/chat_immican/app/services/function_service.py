# execute structured actions (calendar, CRUD)# app/services/function_service.py
from datetime import datetime, timedelta

def validate_schedule(action: dict):
    # Basic validation
    if "when" not in action:
        return False, "missing 'when'"
    try:
        dt = datetime.fromisoformat(action["when"])
    except Exception:
        return False, "invalid datetime"
    return True, ""

def execute(action: dict):
    ok, reason = validate_schedule(action)
    if not ok:
        return {"status":"error","reason":reason}
    dt = datetime.fromisoformat(action["when"])
    dur = int(action.get("duration_minutes", 30))
    end = dt + timedelta(minutes=dur)
    return {
        "status":"ok",
        "id": f"bk_{int(dt.timestamp())}",
        "title": action.get("title","Appointment"),
        "start": dt.isoformat(),
        "end": end.isoformat()
    }
