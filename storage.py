import json
import os
from datetime import datetime

LOG_FILE = "attendance_logs.json"


def load_logs() -> list:
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def add_log(name: str, speaker_id: str, status: str, details: dict) -> None:
    logs = load_logs()
    logs.insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "speaker_id": speaker_id,
        "status": status,
        "details": details,
    })
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)