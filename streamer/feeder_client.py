"""
feeder_client.py — type tokens into the live Undermind feeder.

Run AFTER feeder.py (separate terminal):
  python feeder_client.py
Then type one word/token per line. Each enter sends it to Undermind live.
  - 'SELECT'  -> pick the pre-ready branch (foreground selection, no generation)
  - 'QUIT'    -> exit

Pure local socket. No model, no OS-input code. Sandbox-safe.
"""
import socket, sys

HOST = "127.0.0.1"
PORT = 9911

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print("[client] connected. Type tokens (enter per token). 'SELECT' to pick, 'QUIT' to leave.\n")
    while True:
        tok = input("you> ").strip()
        if not tok:
            continue
        s.sendall((tok + "\n").encode())
        # read feeder's echo
        try:
            s.settimeout(1.0)
            while True:
                data = s.recv(1024).decode("utf-8", "ignore")
                if not data:
                    break
                print(data, end="")
                if data.endswith("\n"):
                    break
        except socket.timeout:
            pass
        if tok.upper() == "QUIT":
            break
    s.close()

if __name__ == "__main__":
    main()
