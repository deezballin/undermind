"""
channel.py — prior-injection channel (the subconscious->conscious handoff).

Undermind writes a short steering 'prior' to a shared local state; the
foreground Hermes reads it at generation time and appends to its assumed
context instead of re-deciding every token. This is the "add to assumed
final context, don't re-think each word" mechanism.

Local-only shared state (file or local socket). No cloud.
"""
import json, os

PRIOR_PATH = os.path.join(os.path.dirname(__file__), "latest_prior.json")

def write_prior(select_result):
    """Undermind calls this after SELECT to hand the prior to foreground."""
    payload = {
        "assumed_context": select_result.get("assumed_context"),
        "chosen_branch": select_result.get("chosen_branch", {}).get("id"),
        "pre_ready_response": select_result.get("response"),
        "surviving_branches": select_result.get("surviving_branches"),
    }
    with open(PRIOR_PATH, "w", encoding="utf-8") as fh:
        json.dump(payload, fh)
    return payload

def read_prior():
    """Foreground Hermes calls this at generation time to get the prior."""
    if not os.path.exists(PRIOR_PATH):
        return None
    with open(PRIOR_PATH, encoding="utf-8") as fh:
        return json.load(fh)

if __name__ == "__main__":
    print(f"prior channel at: {PRIOR_PATH} (local only)")
