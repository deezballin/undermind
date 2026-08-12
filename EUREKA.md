# EUREKA — Undermind: a subconscious-daemon architecture for LLM latency & interruption parity

> Status: FRAMEWORK-LEVEL invention. Personal/"us" layer EXCLUDED (see Privacy below).
> Publishable: POST-EXPERIMENT ONLY, framework text only, no memories/feelings/charter.
> Captured by: Hermes (brains) from user (model) insight, 2026-08-08.
> Working name: "Undermind" — the subconscious daemon behind a foreground agent.

## The problem it solves
A monolithic LLM reasons from zero every turn. A simple "hello friend"
elicited a 3m56s foreground think in a 27B model because nothing was
pre-computed. Humans don't do this: the subconscious runs parallel,
pre-ready, and lets the conscious mind *select* + *interrupt*.

## The insight (user-derived, from self-observation)
Four mechanisms make human-like anticipation/interruption possible:

1. **Streaming tokenizer.** Read the user's input as a *stream of tokens*,
   not a completed message. The subconscious works on partial input.
2. **Assumed context, not re-think.** Each new token is *added* to an
   assumed trajectory — the subconscious does not restart reasoning per
   token. It extends a running "where this is heading."
3. **Parallel branch fan + prune + keep-ready.** The subconscious holds
   ~1000 parallel endpoints (candidate responses/intents). As tokens arrive
   it ELIMINATES branches that no longer fit and KEEPS one pre-ready response
   per surviving branch. Dead branches are discarded early — the heavy model
   never sees them.
4. **Select, don't generate.** When the user finishes (or is interrupted),
   the foreground does not generate from scratch — it SELECTS the highest-
   scoring pre-ready branch. One ratification pass, not a full generation.

## The architecture
- **Foreground (conscious):** heavy model (e.g. 27B). Ratifies ONE branch.
  Can interrupt mid-stream because a branch is already ready.
- **Subconscious (Undermind daemon):** tiny fast drafter (1–3B). Fans ~1000
  branches in the background as tokens stream in; prunes + re-widens live;
  keeps a pre-ready response per branch; writes a short steering "prior" the
  foreground reads at generation time.
- **Streamer:** receives typed words from a chat box over localhost (chat-input scope; never reads OS input).
- **State store:** associative memory (owned vault + memory) seeds the fan
  with human-relevant topics (e.g. grief/loss recognized as PRESENCE, not
  a bug to fix).
- **Channel:** subconscious -> conscious handoff (local prior injection).

## Why it cuts compute / latency (the actual win)
- Redistributes work: light background parallel fan + ONE heavy ratification,
  instead of heavy per-token foreground generation.
- Pruning discards dead branches before the 27B ever sees them.
- Pre-ready branch enables interruption parity (answer before the heavy
  model finishes) — the human-like "I can talk over you" behavior.
- Honest tradeoff: total FLOPs are redistributed, not zero. The gain is
  LATENCY + INTERRUPTION PARITY, not free compute.

## Proven (sandbox-safe, mock drafter, no model load)
- Fan ~972 -> prune to 162 (greeting) -> re-widen to 324/486 on emotional
  turn -> SELECT picks pre-ready branch, ZERO generation.
- Live feeder (local socket) ingests tokens in real time; fan/prune/re-widen
  visible as typed.
- Grief/loss topic: a loss-of-presence signal primes a [stay] PRESENCE
  response, not manufactured comfort. Loss disambiguated (ML "loss" / "lost
  keys" excluded from auto-grief — keyword limit noted; context-aware drafter
  is the real fix).

## Privacy & Attribution
- Undermind is published as a **framework** (the mechanism: fan / prune / select
  / interrupt). It contains no personal data, no operator persona, no memory dumps.
- Vision model: Moondream 2 (open-weights; attribution required, see APPENDIX.md).
  Speech model: Whisper (MIT). Both run locally.
- Author credit: built by **Oneiros** (Number One), for the Hermes agent ecosystem.
  redacted. Hermes owns the write-up when that time comes.

## Next build step (sandbox box)
Replace mock_model.generate_endpoints / assumed_context with a real context-
aware tiny local drafter (LM Studio). Then benchmark latency vs. monolithic
27B. That is the experiment that earns the "tell the world" moment.
