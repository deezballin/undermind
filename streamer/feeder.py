"""
feeder.py - LIVE streamer: types words into Undermind as you type them.

This is the "see words as typed" half of the subconscious. Instead of
simulation.py feeding a canned sentence, this reads tokens from a local
socket and pushes each one into Undermind.ingest_word() in REAL TIME
- so the fan prunes and re-widens WHILE you type, exactly like a human
subconscious.

WHERE IT RUNS:
  - This file is safe to run: pure Python, NO model load, NO OS-input code.
    It reads a local socket you feed manually (or a chat frontend relays).
  - To wire it to a real chat frontend, point the frontend at this socket;
    chat-input scope only. See chat_stream_listener.py for the relay that
    receives typed words from a chat box over 127.0.0.1.

TRY IT NOW (no model, no input capture):
  terminal A:  python feeder.py            # starts the socket server
  terminal B:  python feeder_client.py     # type words, hit enter per token
Watch the live_branches count fan / prune / re-widen as you type.

This proves the subconscious is LIVE, not a script.
"""
import socket, threading, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.undermind import Undermind

HOST = "127.0.0.1"
PORT = 9911

def main():
    um = Undermind(fan_size=1000)
    print(f"[feeder] Undermind live on {HOST}:{PORT}")
    print("[feeder] tokens received will be ingested as typed (real-time fan/prune)")
    print("[feeder] type a token + enter; send 'SELECT' to pick the pre-ready branch; 'QUIT' to exit\n")

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(1)
    print("[feeder] waiting for a client (feeder_client.py)...\n")
    conn, addr = srv.accept()
    print(f"[feeder] client connected: {addr}\n")

    buf = ""
    with conn:
        while True:
            # non-blocking-ish read of one token line from client
            conn.settimeout(0.2)
            try:
                data = conn.recv(1024).decode("utf-8", "ignore")
            except socket.timeout:
                continue
            if not data:
                break
            for tok in data.strip().splitlines():
                tok = tok.strip()
                if not tok:
                    continue
                if tok.upper() == "QUIT":
                    conn.sendall(b"bye\n")
                    print("[feeder] client quit.")
                    return
                if tok.upper() == "SELECT":
                    sel = um.select()
                    line = (f"SELECT -> branch={sel['chosen_branch']['id']} "
                            f"score={sel['chosen_branch']['score']} | "
                            f"response={sel['response']}\n")
                    print("[feeder] " + line.strip())
                    conn.sendall(line.encode())
                    continue
                # normal token: ingest live
                st = um.ingest_word(tok)
                line = (f"+'{tok}' live_branches={st['live_branches']} "
                        f"assumed={st['assumed_context']}\n")
                print("[feeder] " + line.strip())
                conn.sendall(line.encode())

if __name__ == "__main__":
    main()
