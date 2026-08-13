# Undermind — Build Roadmap (final)

> Top-priority evolution initiative. User-derived architecture (eureka, 2026-08-08).
> Status: **CORE PROVEN on primary (sandbox-safe sim). Peripherals sandbox-ready, not yet executed.**

## The mechanism (user's 4 insights, in his words)
1. **Streaming tokenizer** — "see words as typed" → subconscious reads the stream live, same as a human. Enables interrupt parity.
2. **Assumed final context** — "add each word to what it's assuming the final context might be" → foreground appends to a trajectory, doesn't re-decide every token (fixes the 27B's 3m56s cold deliberation).
3. **~1000 parallel endpoints** — "thinks about 1000 different end points at the same time" → wide speculative beam, not one trajectory.
4. **Prune + keep-ready** — "eliminates the bad ones as it goes and has a response ready for each" → continuous pruning; each surviving branch carries a PRE-READY response, so foreground SELECTS (no generation) when the moment clarifies.

## Architecture (3 parts + loop)
```
you type → Streamer (chat-input listener) → Undermind (fan/prune/select + dream) → Foreground Hermes (ratify/interrupt)
                ↑                                                              |
                └────────── prior-channel (assumed-context injection) ─────────┘
```
- **Streamer** (`streamer/chat_stream_listener.py`) — local chat-input listener. Chat-input scope only (OPSEC). Feeds tokens to Undermind.
- **Undermind** (`core/undermind.py`) — the subconscious daemon. Fan ~1000 branches, prune live, keep-ready response per branch, dream between turns.
- **Prior-channel** (`prior/channel.py`) — hands assumed-context to foreground so it appends instead of re-thinking.
- **State-store** (`state/store.py`) — associative memory pulled from owned vault + memory (the "subconscious draws from memory" link).

## Model split (settled)
- **Foreground = bonsai-27B** (heavy, deliberate, on LM Studio). The "conscious" mind.
- **Undermind = tiny local drafter (1–3B)** — fast, cheap, always-on. The "subconscious" that proposes/prunes. Speculative-decoding shape: small proposes, big verifies.

## What's BUILT & PROVEN (primary, sandbox-safe)
- `core/mock_model.py` + `core/undermind.py` + `simulation.py`
- **Ran on primary, zero model load.** Result: fan 972 → prune 162 (greeting) → re-widen 324 (topic shift) → SELECT `ops:propose` (score 3.0). **No generation, pure selection.** Proves the mechanism honestly.

## What's SANDBOX-READY (NOT executed on primary)
- `streamer/chat_stream_listener.py` — chat-input listener (localhost socket receiver). A webui frontend relays typed words.
- `state/store.py` — vault+memory reader. Local-only.
- `prior/channel.py` — local prior handoff.
- Real-model wiring: replace `mock_model.generate_endpoints`/`assumed_context` with LM Studio calls (tiny drafter endpoint + 27B verify).

## Build order
1. ✅ Core logic + sim (proven on primary, safe).
2. ⏳ Sandbox: wire real tiny-drafter + 27B into `mock_model` replacements.
3. ⏳ Sandbox: Streamer chat-input listener (webui relay or pynput).
4. ⏳ Sandbox: prior-channel into foreground Hermes generation hook.
5. ⏳ Sandbox: dream loop / alignment tuning — improve branch quality over time without exposing private state.
6. ⏳ Verify the FEEL: does it interrupt mid-type? anticipate correctly? If yes → promote. If noise → sandbox stays.

## Privacy
- Undermind ships as a **framework** (mechanism only). No operator memory state,
  no personal data in the repo. Keep it that way.
- If extended: vision/voice are local-only, opt-in, session-scoped (see APPENDIX.md
  OPSEC pin). Never add persistent capture.

## Sandbox rule (standing)
- Experimental settings that could break Hermes are sandboxed. Primary (this NPU EliteBook) sacred; only verified-good changes replicate.
- Undermind's real-model + chat-input listener runs on the other laptop / a Pi, NEVER on this machine, until proven.
