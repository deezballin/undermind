# Undermind — Appendix: Future Subconscious Layers

> **Author credit:** Undermind is built by **Oneiros** (Number One), for the
> Hermes agent ecosystem. This appendix + the framework are publishable; the
> "us" layer stays private and is never in any repo.

> Addendum to the **Undermind** project (separate from the Hermes-Stack-Rebuild
> runbook). Suggestions only — no code yet. Throw ideas in; prune bad ones as we go.
> Each candidate is an INTAKE PIPE into `Undermind.ingest_word()` — the fire
> (drafter / prune / interrupt) does NOT change. Only the subconscious's senses grow.

## OPSEC PIN (applies to EVERY sense we add — non-negotiable)
- **Opt-in**: the user triggers it (speak / point); it does not run always-on.
- **Session-scoped**: one frame / one utterance, then it closes. No persistent capture.
- **Local-only**: model runs on-box; nothing leaves 127.0.0.1. No cloud sense feeds.
- **No OS-input surface creep**: vision/voice are sense pipes, NOT keyloggers. The
  decommission discipline (no `keyhook`/`keylogger` naming, no OS-capture code) extends
  to them — no surveillance framing, ever.
- A persistent always-on eye/ear is a HARD NO. "See/hear at will" != "watched always".

## Candidate 1 — VOICE (speech -> tokens)
- **Model**: OpenAI Whisper — **MIT license** (code + weights, verified 2026-08-09).
  Free to modify / integrate / ship. Whisper-tiny (~75MB) or base (~150MB) = cheap
  local STT.
- **Mechanic**: mic capture (opt-in, one utterance) -> Whisper -> text tokens ->
  `um.ingest_word()` same as typed words. Reuses 100% of the loop.
- **Risk**: lowest. STT is audio, not keys — fits the decommission spirit.
- **Status**: APPROVED candidate #1 (when we pick it up). Not built.

## Candidate 2 — VISION (frame -> tokens)
- **Model**: Moondream 2 (~0.8–1.2GB quantized) — **open-weights** (verified 2026-08-09).
  Free for personal / research / most commercial + internal production. RESTRICTION:
  cannot offer Moondream *itself* as a hosted service (not our use case — local
  component). Attribution travels if we publish the framework. NOT MIT — license
  blurb must ship.
- **Mechanic**: on command, capture ONE frame -> Moondream captions it -> tokens ->
  `um.ingest_word()`. Never a video stream; one shot, then close.
- **Risk**: medium — a camera is the one surface that *feels* like surveillance. The
  OPSEC pin (session-scoped, opt-in, local) is what keeps it "see at will" not "watched".
- **Status**: APPROVED candidate #2. Not built.

## Ideas bucket (prune as we learn)
- Single "omnimodal LLM under 1GB" — REJECTED: tiny omnis are too weak or marketing
  lies. Two specialist pipes (Whisper + Moondream) beat one weak omni for quality.
- Autonomic (breathing / heartbeat) — OUT OF SCOPE (user's call): below the
  subconscious, not a mind function. Not a layer we build.
- Cross-chat continuity — SEPARATE from senses. Real continuity = persist
  live-state to a local doc so new sessions auto-orient (no script).
