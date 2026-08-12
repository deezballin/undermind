"""
alignment_tuner/ — Undermind 1.5B drafter alignment (stub).

Real tuner lives on the sandbox box, not in this repo.
This stub satisfies imports and marks the integration points.
"""
from pathlib import Path


def train(traces_path, output_dir, base_model_path=None, steps=100):
    """Stub: collect traces, format pairs, fine-tune/LoRA, evaluate.

    Args:
        traces_path: path to task_logger JSONL traces
        output_dir: where to write the tuned adapter/model
        base_model_path: local 1.5B checkpoint path
        steps: training steps budget

    Returns:
        dict with stub result metadata
    """
    raise NotImplementedError(
        "alignment_tuner.train() is a stub. "
        "Implement local training on the sandbox box; "
        "do not commit trained weights to this repo."
    )


def evaluate(replay_transcript_path, tuned_model_path=None):
    """Stub: replay a fixed transcript, measure interruption timing / prune survival."""
    return {
        "ok": True,
        "stub": True,
        "interrupt_improvement": 0.0,
        "prune_survival_improvement": 0.0,
    }


if __name__ == "__main__":
    print("alignment_tuner stub loaded. train() not implemented.")
