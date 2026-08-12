"""
undermind.py — the Subconscious Daemon (core).

Implements the user-derived mechanism (2026-08-08):
  1. Streaming tokenizer feeds words as typed (Streamer -> ingest_word)
  2. MOCK drafter fans ~1000 parallel endpoints (assumed contexts)
  3. Each new word PRUNES branches whose signature no longer fits
  4. Each surviving branch carries a PRE-READY response
  5. On completion, foreground SELECTS the top branch (no generation, just pick)

State is persistent across turns (the "subconscious" that accumulates).
Real-model wiring (drafter + 27B) is deferred to the sandbox box; this
module proves the architecture with the mock model on the primary machine.
"""
from . import mock_model as mm

class Undermind:
    def __init__(self, fan_size=1000):
        self.fan_size = fan_size
        self.branches = []          # current parallel endpoints
        self.stream_words = []      # running typed stream (this turn)
        self.turn = 0
        self.last_select = None

    # ---- Streamer entry point: a word just got typed ----
    def ingest_word(self, word):
        word = word.strip().lower()
        if not word:
            return
        self.stream_words.append(word)
        if not self.branches:           # first word of turn: fan out
            self.branches = mm.generate_endpoints(self.stream_words, self.fan_size)
        else:
            self._prune()               # eliminate branches that no longer fit
        return self.status()

    # ---- continuous pruning as the stream arrives ----
    def _prune(self):
        words = set(self.stream_words)
        # map each word to the topic(s) it belongs to, for honest scoring
        word_topic = {}
        for w in words:
            for top, kws in mm.TOPICS.items():
                if w in kws:
                    word_topic.setdefault(w, set()).add(top)
        kept = []
        for b in self.branches:
            # a branch's score = how many CURRENT stream words match its topic
            # (not just any overlap) -> the dominant topic outranks others
            match = sum(1 for w in words if b["topic"] in word_topic.get(w, ()))
            if match > 0:
                b["score"] = match
                kept.append(b)
        # eliminate the rest (bad endpoints dropped, per user's mechanism)
        # RE-WIDEN: if a stream word introduces a topic with ZERO surviving
        # branches, re-fan that topic so a branch stays ready (subconscious
        # must keep an endpoint for a newly-relevant topic, not lose it).
        present_topics = set().union(*word_topic.values()) if word_topic else set()
        live_topics = {b["topic"] for b in kept}
        missing = present_topics - live_topics
        if missing:
            refill = mm.generate_endpoints(self.stream_words, self.fan_size)
            kept += [b for b in refill if b["topic"] in missing]
        # maintain fan width: if pruned too thin, re-fan from current stream
        if len(kept) < self.fan_size * 0.1 and self.stream_words:
            kept = mm.generate_endpoints(self.stream_words, self.fan_size)
        self.branches = kept

    # ---- foreground: select pre-ready response (no generation) ----
    def select(self):
        if not self.branches:
            self.branches = mm.generate_endpoints(self.stream_words, self.fan_size)
        ranked = sorted(self.branches, key=lambda b: b["score"], reverse=True)
        top = ranked[0] if ranked else None
        self.last_select = {
            "turn": self.turn,
            "stream": list(self.stream_words),
            "assumed_context": mm.assumed_context(self.stream_words),
            "surviving_branches": len(self.branches),
            "chosen_branch": top,
            "response": top["response"] if top else "[no branch]",
        }
        self.turn += 1
        self.stream_words = []      # reset for next turn (dream between turns)
        self.branches = []          # subconscious clears working fan; persists via memory
        return self.last_select

    def status(self):
        return {
            "turn": self.turn,
            "stream_len": len(self.stream_words),
            "live_branches": len(self.branches),
            "assumed_context": mm.assumed_context(self.stream_words),
        }

    # ---- dream loop stub (between turns) ----
    def dream(self):
        """Offline consolidation hook. Real version: feelings/soul skills.
        For the core proof this just logs that a dream cycle ran."""
        return {"dreamed": True, "turn": self.turn}
