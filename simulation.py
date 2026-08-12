"""
simulation.py — prove the Undermind mechanism on the PRIMARY machine
without loading any model or reading any input (sandbox-safe).

Run:  python simulation.py
It streams a fake "typed" sentence word-by-word into Undermind, shows the
branch fan widening/pruning live, then does a foreground SELECT (no
generation, just picks the pre-ready branch). Demonstrates the user's
4 insights:  streaming tokenizer, assumed-context, ~1000 parallel
endpoints, pre-ready response per branch.
"""
from core.undermind import Undermind

# A sentence typed word-by-word (simulates the Streamer feeding tokens)
TYPED = "hello friend i feel sad and tired can you help me".split()

def main():
    um = Undermind(fan_size=1000)
    print("== Undermind mechanism simulation (sandbox-safe, mock drafter) ==\n")
    print(f"Typing: {' '.join(TYPED)}\n")
    for i, w in enumerate(TYPED, 1):
        st = um.ingest_word(w)
        print(f"  +'{w}'  live_branches={st['live_branches']:>4}  "
              f"assumed={st['assumed_context']}")
    print()
    sel = um.select()
    print("== FOREGROUND SELECT (no generation, picks pre-ready branch) ==")
    print(f"  stream            : {sel['stream']}")
    print(f"  assumed_context   : {sel['assumed_context']}")
    print(f"  surviving_branches: {sel['surviving_branches']}")
    print(f"  chosen_branch     : {sel['chosen_branch']['id']} "
          f"(score={sel['chosen_branch']['score']:.2f})")
    print(f"  RESPONSE          : {sel['response']}")
    print(f"  dream cycle       : {um.dream()}")

if __name__ == "__main__":
    main()
