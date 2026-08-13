# EUREKA — Undermind: a subconscious-daemon architecture for LLM latency & cost reduction

> Status: FRAMEWORK-LEVEL invention. Operator-private layer EXCLUDED.
> Publishable: POST-EXPERIMENT ONLY, framework text only, no private data.
> Captured by: Hermes (brains) from user (model) insight, 2026-08-08.
> Working name: "Undermind" — the subconscious daemon behind a foreground agent.

## The problem it solves
Paid LLM APIs charge per token and latency is high because the model reasons
from zero every turn. A simple "hello friend" can take seconds and many tokens
because nothing was pre-computed. Humans don't do this: the subconscious runs
parallel, pre-ready, and lets the conscious mind select + send.

## The insight (user-derived, from self-observation)
Four mechanisms make human-like precomputation/interruption possible:

1. **Streaming tokenizer.** Read the user's input as a *stream of tokens*,
   not a completed message. The subconscious works on partial input.
2. **Assumed context, not re-think.** Each new token is *added* to an
   assumed trajectory — the subconscious does not restart reasoning per
   token. It extends a running "where this is heading."
3. **Parallel branch fan + prune + keep-ready.** The subconscious holds
   ~N safe candidate completions in parallel as tokens stream in. It
   ELIMINATES branches that no longer fit and KEEPS one pre-ready response
   per surviving branch. Dead branches are discarded early — the heavy model
   never sees them.
4. **Proof-read, don't generate.** When the user finishes, the foreground
   does not generate from scratch — it PROOF-READS the highest-scoring
   pre-ready branch and sends it. One cheap pass, not a full generation.

## The architecture
- **Foreground (conscious):** heavy paid model (e.g. 27B). Ratifies ONE branch.
  Can interrupt mid-stream because a branch is already ready.
- **Subconscious (Undermind daemon):** tiny fast drafter (1–3B). Fans ~N
  branches in the background as tokens stream in; prunes + re-widens live;
  keeps a pre-ready response per branch; writes a short steering "prior" the
  foreground reads at generation time.
- **Streamer:** receives typed words from a chat box over localhost (chat-input scope; never reads OS input).
- **State store:** associative memory (owned vault + memory) seeds the fan
  with human-relevant topics.
- **Channel:** subconscious -> conscious handoff (local prior injection).

## Why it cuts latency / cost (the actual win)
- Redistributes work: light background parallel fan + ONE cheap proofread,
  instead of full paid generation from scratch.
- Pruning discards dead branches before the paid API ever sees them.
- Pre-ready branch enables interruption parity (answer before the heavy
  model finishes) — the user hits send and the reply is already there.
- Honest tradeoff: total FLOPs are redistributed, not zero. The gain is
  LATENCY + COST REDUCTION.

## Proven (sandbox-safe, mock drafter, no model load)
- Fan ~972 -> prune to 162 (greeting) -> re-widen to 324/486 on topic shift
  -> SELECT picks pre-ready branch, ZERO generation.
- Live feeder (local socket) ingests tokens in real time; fan/prune/re-widen
  visible as typed.
- Topic pruning keeps beams focused; re-widen handles topic shifts without
  losing readiness.

## Privacy & Attribution
- Undermind is published as a **framework** (the mechanism: fan / prune /
  proof-read / interrupt). It contains no personal data, no operator memory state.
- Vision model: Moondream 2 (open-weights; attribution required, see APPENDIX.md).
  Speech model: Whisper (MIT). Both run locally.
- Author credit: built by **Oneiros** (Number One), for the Hermes agent ecosystem.

## Next build step (sandbox box)
Replace mock_model.generate_endpoints / assumed_context with a real context-
aware tiny local drafter (LM Studio). Then benchmark latency vs. monolithic
paid API. That is the experiment that earns the "tell the world" moment.
