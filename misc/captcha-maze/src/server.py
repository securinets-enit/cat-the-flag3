"""
SecurinetsENIT CTF 2026 - Misc Challenge: Captcha: Rats in a Maze
Author: MrXFuji

TLS Server that serves 100 dynamic 11x11 weighted mazes with a 5.0s per-round deadline.
Protected by redpwn Proof-of-Work (VDF).
Outputs ASCII FIGlet flag with typographic ambiguity trap upon completion.
"""

import socket
import ssl
import threading
import time
import os
import sys

from maze_gen import Maze
from pow_engine import generate_challenge, verify_solution

try:
    import pyfiglet
except ImportError:
    pyfiglet = None

def _load_flag():
    """Read the flag from flag.txt next to the server (or $FLAG_PATH), so the
    deployed flag always matches the one registered in CTFd."""
    path = os.environ.get("FLAG_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), "flag.txt"))
    try:
        with open(path) as f:
            return f.read().strip()
    except OSError:
        print(f"[-] Warning: could not read flag from {path}")
        return "SecurinetsENIT{flag_missing_contact_admin}"


FLAG = _load_flag()
TOTAL_ROUNDS = int(os.environ.get("ROUNDS", 100))
ROUND_TIMEOUT = 5.0
POW_DIFFICULTY = 100  # ~1.0s in pure Python, instantaneous in C/Go

def render_flag_figlet(flag: str) -> str:
    """Renders the flag in FIGlet standard font where 'O' and '0' look identical."""
    if pyfiglet:
        f = pyfiglet.Figlet(font='standard')
        art = f.renderText(flag)
        return art
    else:
        # Fallback pre-rendered ASCII art for standard FIGlet font
        return (
            " ____                           _             _          \n"
            "/ ___|  ___  ___ _   _ _ __ ___| |_ ___  __ _| |__   ___ \n"
            "\\___ \\ / _ \\/ __| | | | '__/ __| __/ __|/ _` | '_ \\ / _ \\\n"
            " ___) |  __/ (__| |_| | | | (__| || (__| (_| | |_) |  __/\n"
            "|____/ \\___|\\___|\\__,_|_|  \\___|\\__\\___|\\__,_|_.__/ \\___|\n"
            f"\n[FLAG FIGLET BANNER: {flag}]\n"
        )

def handle_client(tls_sock, addr):
    try:
        tls_sock.settimeout(60.0)
        sock_file = tls_sock.makefile('rw', encoding='utf-8', buffering=1)

        sock_file.write("============================================================\n")
        sock_file.write("    SecurinetsENIT CTF - Captcha: Rats in a Maze v1.0       \n")
        sock_file.write("============================================================\n")
        sock_file.write("Welcome, user.\n")
        sock_file.write("A simple captcha to prove you're not a robot.\n")
        sock_file.write(f"Clear {TOTAL_ROUNDS} consecutive 11x11 maze rounds within {ROUND_TIMEOUT}s each.\n\n")

        # 1. Proof of Work (redpwnpow)
        chal = generate_challenge(difficulty=POW_DIFFICULTY)
        sock_file.write(f"proof of work: curl -sSfL https://pwn.red/pow | sh -s {chal}\n")
        sock_file.write("solution:\n")
        sock_file.flush()

        sol = sock_file.readline()
        if not sol:
            return
        sol = sol.strip()

        if not verify_solution(chal, sol):
            sock_file.write("[-] Proof of work invalid or expired. Connection terminated.\n")
            sock_file.flush()
            return

        sock_file.write("[+] Proof of work verified! Initializing maze sequence...\n\n")
        sock_file.flush()

        # 2. Maze rounds
        for round_idx in range(1, TOTAL_ROUNDS + 1):
            m = Maze(11)
            m.generate()

            sock_file.write(f"--- [ROUND {round_idx}/{TOTAL_ROUNDS}] ---\n")
            sock_file.write(m.render_terminal())
            sock_file.write(f"Submit move sequence (max {ROUND_TIMEOUT}s):\n")
            sock_file.flush()

            tls_sock.settimeout(ROUND_TIMEOUT)
            start_t = time.time()
            line = sock_file.readline()
            elapsed = time.time() - start_t

            if not line:
                sock_file.write("\n[-] Connection closed.\n")
                sock_file.flush()
                return

            moves = line.strip().upper()

            if moves != m.solution_moves:
                sock_file.write(f"\n[-] INCORRECT PATH! Move validation failed.\n")
                sock_file.write(f"[-] Your path:     {moves}\n")
                sock_file.write(f"[-] Expected path: {m.solution_moves}\n")
                sock_file.write("[-] Security protocol triggered: Access Denied.\n")
                sock_file.flush()
                return

            sock_file.write(f"[+] Round {round_idx} cleared! Cost: {m.solution_cost} (Time: {elapsed:.3f}s)\n\n")
            sock_file.flush()

        # 3. Success & Flag banner
        sock_file.write("\n" + "=" * 60 + "\n")
        sock_file.write(f"[+] ALL {TOTAL_ROUNDS} ROUNDS CLEARED!\n")
        sock_file.write("[+] You have successfully solved the Captcha.\n")
        sock_file.write("=" * 60 + "\n\n")
        sock_file.write(render_flag_figlet(FLAG))
        sock_file.write("\n[Lyric Note]: Despite all our rage, we're all just rats in a maze.\n")
        sock_file.flush()

    except socket.timeout:
        try:
            sock_file.write(f"\n[-] TIMEOUT! You exceeded the {ROUND_TIMEOUT}s limit.\n")
            sock_file.flush()
        except Exception:
            pass
    except Exception as e:
        pass
    finally:
        try:
            tls_sock.close()
        except Exception:
            pass

def main():
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 5000))

    cert_file = os.path.join(os.path.dirname(__file__), "cert.pem")
    key_file = os.path.join(os.path.dirname(__file__), "key.pem")

    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print("[-] Error: cert.pem or key.pem missing! Run gen_cert.py first.")
        sys.exit(1)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file)

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(128)

    print(f"[+] Captcha Maze TLS server listening on {host}:{port}...")

    while True:
        try:
            client_sock, client_addr = server_sock.accept()
            tls_client = ssl_context.wrap_socket(client_sock, server_side=True)
            t = threading.Thread(target=handle_client, args=(tls_client, client_addr), daemon=True)
            t.start()
        except Exception as e:
            pass

if __name__ == "__main__":
    main()
