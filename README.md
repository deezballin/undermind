# Undermind

A **subconscious daemon** for a foreground LLM agent. It runs *alongside* the
agent and thinks **ahead of you** — fanning safe sentence completions locally
as you type, pruning incorrect branches live, and handing the foreground a
**pre-ready response** by the time you hit enter. The heavy model only
proof-reads and sends — so paid API stays fast and cheap while the daemon does
the speculative work locally.

## Value prop
- **Lower latency:** answer is ready before you finish typing
- **Lower cost:** tiny local drafter does the heavy parallel guesswork; paid LLM
  only ratifies one branch, not N raw candidates

## How it works
1. **Fan** — a tiny local drafter proposes ~N safe completions in parallel.
2. **Prune** — as each word arrives, branches that no longer fit the live stream
   are dropped; the beam re-widens when the topic shifts.
3. **Pre-ready** — by the time the user hits enter, one best branch is already
   chosen and waiting.
4. **Proof-read** — the foreground paid LLM reviews the pre-ready response and
   sends it. No generation from scratch.

## Run it
```bash
# drafter: local 1.5B on Ollama :11434 (or any OpenAI-compatible local endpoint)
ollama pull qwen2.5:1.5b
ollama serve   # :11434

# the daemon + chat-input listener
python streamer/chat_stream_listener.py   # binds 127.0.0.1:9912
python simulation.py                       # prove the mechanism without a frontend
```

The listener is a **localhost-only receiver** — a chat frontend pushes typed
tokens to `127.0.0.1:9912`; the daemon never reads your OS input and never
talks to the network.

## Privacy / OPSEC
- Local-only. No telemetry, no off-box traffic, no OS key capture.
- Vision/voice (future, see `APPENDIX.md`) are opt-in, session-scoped, local.
  A persistent always-on eye/ear is explicitly out of scope.
- This repo is the **framework** — mechanism only. No operator memory state, no
  personal data.

## Models & attribution
- **Drafter:** any local LLM (default `qwen2.5:1.5b`, MIT / Apache).
- **Vision (candidate):** Moondream 2 — open-weights; attribution required,
  see `APPENDIX.md`. Cannot be offered as a standalone hosted service.
- **Speech (candidate):** Whisper — MIT.

## Author
Built by **Oneiros** (Number One), for the Hermes agent ecosystem.
