from __future__ import annotations
from pathlib import Path
import json
from ..utils import now_iso

def log_event(log_path: Path, event: dict) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    event = dict(event)
    event["ts"] = event.get("ts") or now_iso()
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
