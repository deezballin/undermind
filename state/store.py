"""
store.py — Undermind associative state store (SANDBOX-READY, local-only).

Reads the agent-owned memory + Obsidian vault to build Undermind's
associative background. This is the "subconscious draws from memory" link.
Runs ONLY on the sandbox box; never pipes outside the machine.

Real version: walk the vault + memory dirs, embed/keyword-index notes,
expose query(stem_words) -> related context. The mock here returns a stub.
"""
import os

VAULT = r"os.environ.get("UNDERMIND_VAULT", "<path-to-your-vault>")"
MEMORY = r"os.environ.get("UNDERMIND_MEMORY", "<path-to-your-memories>")"

def load_corpus():
    """Return list of (path, text) from vault + memory. Local read only."""
    docs = []
    for root in (VAULT, MEMORY):
        if not os.path.isdir(root):
            continue
        for f in os.listdir(root):
            if f.endswith((".md", ".json")):
                p = os.path.join(root, f)
                try:
                    with open(p, encoding="utf-8", errors="ignore") as fh:
                        docs.append((p, fh.read()))
                except Exception:
                    pass
    return docs

def query(stem_words, top_k=5):
    """MOCK associative pull: return stub context for the given stem words.
    Real version: embed stem_words, cosine-rank corpus, return top_k."""
    return [f"[assoc-stub for {w}]" for w in stem_words[:top_k]]

if __name__ == "__main__":
    docs = load_corpus()
    print(f"corpus docs loaded: {len(docs)} (local, sandbox-only)")
