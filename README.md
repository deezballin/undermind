# Undermind

A **subconscious daemon** for a foreground LLM agent. It runs *alongside* the
agent and thinks **ahead of you** — fanning candidate branches as you type,
pruning them by live stream overlap, and **interrupting mid-type** with a
pre-ready response when its confidence crosses a threshold. The heavy model
only ratifies the one branch the subconscious already chose — so the foreground
stays fast and cheap while the daemon does the speculative work locally.

## How it works
1. **Fan** — a tiny local drafter proposes ~N candidate branches in parallel.
2. **Prune** — as each word arrives, branches whose topic doesn't match the
   live stream are dropped; the beam re-widens when the topic shifts.
3. **Interrupt** — when the best surviving branch's overlap score crosses
   `INTERRUPT_THRESHOLD`, the daemon fires a pre-ready response *before* you
   submit. (The "subconscious spoke first" moment.)
4. **Select** — on submit, the chosen branch + its pre-ready response are handed
   to the foreground via `prior/channel.py`.

## Token/Cost Optimization
- **Small AI = Local** — A tiny 1-1.5B model runs locally (Ollama on :11434, or any OpenAI-compatible local endpoint). Zero token cost, no network latency.
- **Large AI = Hosted** — Only the verification/ratification step uses a larger hosted model. Dramatically reduces token consumption and cost since only one refined branch is sent externally vs. N raw candidate branches.

This split architecture keeps you in control: local intelligence for speed and cost, hosted brains for quality when it matters most.

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
- This repo is the **framework** — mechanism only. No operator persona, no
  memor y dumps, no personal data.

## Models & attribution
- **Drafter:** any local LLM (default `qwen2.5:1.5b`, MIT / Apache).
- **Vision (candidate):** Moondream 2 — open-weights; attribution required,
  see `APPENDIX.md`. Cannot be offered as a standalone hosted service.
- **Speech (candidate):** Whisper — MIT.

## Author
Built by **Oneiros** (Number One), for the Hermes agent ecosystem.