"""
chat_stream_listener.py - Local chat-input relay for the subconscious.

RECEIVER ONLY. This process binds a localhost socket and waits for a chat
frontend (the Hermes webui / TUI input box) to send words as the user types
them. It does NOT read keystrokes from the operating system - there is no
OS-input code here and none is imported. A webui extension or a local script
pushes tokens over 127.0.0.1; this file only receives them and feeds
Undermind.ingest_word() in real time.

Privacy: 127.0.0.1 only. Nothing leaves the box. No external connection,
no file capture, no OS-input surface.

INTERRUPT: as each token arrives, Undermind prunes/re-widens live. When the
best pre-ready branch's score crosses INTERRUPT_THRESHOLD before the user
submits, the listener emits an INTERRUPT line - the subconscious firing a
pre-ready response mid-type.

PERSISTENT: the listener re-accepts after every client drop. The Undermind
instance is created ONCE, so its state (the "dreams between turns" memory)
survives frontend reconnects - the subconscious never restarts.

Protocol (newline-delimited, from a chat frontend on localhost):
  <token>     one typed word
  SUBMIT      user finished the thought -> emit selected prior
  QUIT        close

Run:  python streamer/chat_stream_listener.py
A webui frontend connects to 127.0.0.1:9912 and streams typed words.
"""
import socket, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.undermind import Undermind

HOST = "127.0.0.1"
PORT = 9912
INTERRUPT_THRESHOLD = 3   # live overlap score that triggers a mid-type interrupt

def main():
    # ONE instance for the life of the process -> state persists across reconnects
    um = Undermind(fan_size=1000)
    print(f"[listener] chat-input relay live on {HOST}:{PORT}")
    print("[listener] local-only; receives typed words from a chat frontend")
    print("[listener] feed tokens as typed; SUBMIT to select; QUIT to exit")
    print("[listener] PERSISTENT - re-accepts after each client drop\n")

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(1)

    while True:
        # Persistent subconscious: keep serving across frontend blips.
        try:
            conn, addr = srv.accept()
        except OSError:
            continue
        print(f"[listener] chat frontend connected: {addr}\n")
        _serve_client(conn, um)
        print("[listener] client disconnected; waiting for next connection...\n")

def _serve_client(conn, um):
    """Handle one frontend session. Returns when the client leaves; the
    outer loop then re-accepts without recreating Undermind."""
    interrupted = False
    try:
        with conn:
            while True:
                conn.settimeout(0.2)
                try:
                    data = conn.recv(4096).decode("utf-8", "ignore")
                except socket.timeout:
                    continue
                if not data:
                    break
                for line in data.strip().splitlines():
                    tok = line.strip()
                    if not tok:
                        continue
                    if tok.upper() == "QUIT":
                        conn.sendall(b"bye\n"); print("[listener] client quit."); return
                    if tok.upper() == "SUBMIT":
                        sel = um.select()
                        out = (f"PRIOR -> branch={sel['chosen_branch']['id']} "
                               f"score={sel['chosen_branch']['score']} | "
                               f"response={sel['response']}\n")
                        print("[listener] " + out.strip()); conn.sendall(out.encode())
                        continue
                    # normal typed token -> ingest live
                    st = um.ingest_word(tok)
                    live = um.branches if um.branches else []
                    best = max(live, key=lambda b: b.get("score", 0)) if live else None
                    best_score = best.get("score", 0) if best else 0
                    msg = (f"+'{tok}' live_branches={st['live_branches']} "
                           f"assumed={st['assumed_context']} best={best['id'] if best else '-'}({best_score})")
                    if best_score >= INTERRUPT_THRESHOLD and not interrupted:
                        interrupted = True
                        intr = (f"INTERRUPT -> pre-ready branch={best['id']} "
                                f"score={best_score} | response={best['response']}\n")
                        print("[listener] " + intr.strip()); conn.sendall(intr.encode())
                    print("[listener] " + msg.strip())
                    conn.sendall(("OK " + msg + "\n").encode())
    except (ConnectionError, OSError) as e:
        # client dropped mid-stream (closed chat box / network blip) ->
        # we just return; the outer loop re-accepts. Subconscious stays up.
        print(f"[listener] client connection dropped ({e}); continuing.")

if __name__ == "__main__":
    main()
