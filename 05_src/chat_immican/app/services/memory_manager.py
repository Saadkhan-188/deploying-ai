# short-term memory + summarization hook# app/memory_manager.py
from app.config import settings
import time

def compress_messages(messages):
    # messages: list of dict {role,text,ts}
    if len(messages) <= settings.MAX_MESSAGES:
        return messages
    keep = messages[-settings.MAX_MESSAGES:]
    earlier = messages[:-settings.MAX_MESSAGES]
    # naive summary — join first phrases to create a compact note
    parts = []
    for m in earlier:
        txt = m.get("text","")
        parts.append(" ".join(txt.split()[:10]) + ("..." if len(txt.split())>10 else ""))
    summary = " | ".join(parts)
    note = {"role":"system", "text": f"[SUMMARY] {summary}", "ts": time.time()}
    return [note] + keep
