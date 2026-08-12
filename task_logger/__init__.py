"""
task_logger/ — Undermind audit trail (local-only, sandbox-safe).

Records:
  - task dispatches
  - branch prune/re-widen events
  - selections / interruptions
  - dream cycles
  - errors / fallback switches

Output: JSONL by default, one JSON object per line. Rotates by default
when it exceeds MAX_BYTES; old files are renamed with a timestamp suffix.
"""
import json
import os
import time
from pathlib import Path
from threading import Lock

LOG_DIR = Path(os.environ.get("UNDERMIND_LOG_DIR", "<unset>"))
LOG_FILE = LOG_DIR / "undermind.jsonl"
MAX_BYTES = 5 * 1024 * 1024  # 5 MB
_lock = Lock()


def _ensure_log_dir():
    if str(LOG_DIR) == "<unset>" or not LOG_DIR.is_dir():
        raise RuntimeError(
            "UNDERMIND_LOG_DIR is not set or does not exist. "
            "Task logger MUST stay local; do not commit logs."
        )
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def _maybe_rotate():
    if not LOG_FILE.exists() or LOG_FILE.stat().st_size < MAX_BYTES:
        return
    stamp = time.strftime("%Y%m%d_%H%M%S")
    rotated = LOG_DIR / f"undermind_{stamp}.jsonl"
    LOG_FILE.replace(rotated)


def log(event_type, payload):
    """Append one structured event to the JSONL audit trail."""
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "type": event_type,
        "payload": payload,
    }
    with _lock:
        _ensure_log_dir()
        _maybe_rotate()
        with LOG_FILE.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def read_recent(limit=200):
    """Return the most recent `limit` records from the current log file."""
    if not LOG_FILE.exists():
        return []
    lines = []
    with LOG_FILE.open("r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                lines.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return lines[-limit:]


if __name__ == "__main__":
    try:
        log("smoke", {"msg": "task_logger verification"})
        print(f"wrote test event to {LOG_FILE}")
        print(f"recent records: {len(read_recent())}")
    except RuntimeError as exc:
        print(f"blocked: {exc}")
