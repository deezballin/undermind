# Task Logger — Undermind Audit Trail

Structured event log for the daemon lifecycle.

## What it records

- Task dispatch / selection
- Branch prune / re-widen counts
- Interruptions / pre-ready responses
- NPU fallback events
- Dream cycles
- Errors

## Storage

- Format: JSONL, one JSON object per line
- Location: `UNDERMIND_LOG_DIR` env var
- Default filename: `undermind.jsonl`
- Auto-rotation at 5 MB, with timestamped archives

## Usage

```python
from task_logger import log, read_recent

log("prune", {
    "turn": 12,
    "before": 972,
    "after": 162,
    "topic": "grief",
})

records = read_recent(limit=50)
```

## OPSEC

- Logs stay local. Do not commit `UNDERMIND_LOG_DIR` contents to git.
- Default state is unset; daemon can still run without logging.
