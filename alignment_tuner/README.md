# Alignment Tuner — Undermind 1.5B Drafter Alignment

Goal: align the local 1.5B drafter so its fan/prune/select behavior matches
the EUREKA mechanism without drifting into generic chat.

## Scope

- Fine-tune/adapt the 1.5B drafter on short prompt/response pairs shaped
  like candidate branches + chosen branch, not long dialogue.
- Keep the model local; hosted ratifier stays separate.

## Approach (current recommendation)

1. Collect `{stream_words -> top_branch_response}` traces from the live
   daemon via `task_logger`.
2. Convert traces to training pairs: input = stream tokens + branch metadata,
   target = selected branch response.
3. Fine-tune with a small-step local trainer or LoRA adapter on the 1.5B.
4. Evaluate by replaying a fixed transcript through the daemon and comparing
   interruption timing / prune survival to baseline.

## Safety

- Do not train on operator persona/feelings/private memories.
- Training data should be mechanism-shaped only: stream words, branch score,
  selected response. No identity state.

## Files

This directory is a placeholder for the tuner implementation. The real
tuner belongs in the sandbox environment, not in this public framework repo.
