#!/usr/bin/env python3
"""
SecurinetsENIT CTF 2026 - Misc Challenge: Captcha: Rats in a Maze
Author: MrXFuji

Educational Solution Script
===========================

Challenge Overview:
-------------------
The challenge presents "A simple captcha to prove you're not a robot" — requiring
the participant to clear 100 consecutive 11x11 dynamically generated mazes over
a TLS socket under a strict 5.0-second deadline per maze.

The challenge introduces several sophisticated layers:
1. Proof of Work Gate:
   - A non-parallelizable VDF challenge (redpwn/pow).
   - Can be solved in Python using big-integer arithmetic or via the official runner.

2. ANSI Terminal Escapes & Color-Coded Entrances:
   - The Entrance is indicated by Green text (\x1b[92m) on the border.
   - The Exit is indicated by Red text (\x1b[91m) on the border.
   - Naively stripping ANSI codes before parsing destroys the entrance/exit coordinates!

3. East Asian Width & Double-Width Unicode (UAX #11):
   - Cells contain various board-game pieces (Chess, Dice, Dominoes, Mahjong, Cards).
   - Dominoes (U+1F063..), Mahjong (U+1F010..), and Playing Cards (U+1F0A1..) are WIDE (width=2 columns).
   - In the terminal, every cell occupies 2 display columns.
   - A wide character occupies 1 code point in Python but 2 terminal columns.
   - If a parser splits by character index, every column after a wide character shifts out of alignment!

4. Compact Cost Valuation Model:
   - Moving onto a tile costs: 1 + weight(tile).
   - Chess pieces: Pawn 1, Knight 3, Bishop 3, Rook 5, Queen 9, King 100.
   - Playing cards: Ace 1, 2-10 face value, J/Q/K 10.
   - Dice (U+2680..U+2685): 1 to 6.
   - Dominoes (U+1F063..): left + right where left, right = divmod(ord(c) - 0x1F063, 7).
   - Mahjong: tile rank 1 to 9.

5. Weighted Shortest Path (Dijkstra):
   - The maze guarantees a strictly unique minimum-cost path.
   - Run Dijkstra's algorithm from entrance to exit.

6. FIGlet Typography Trap:
   - The flag is rendered in FIGlet standard font where 'O' (capital O) and '0' (digit zero)
     render identically.
   - The lyric clue ("despite all our rage, we're all just rats in a maze") confirms the word
     is "OuR", yielding the final flag:
     Securinets{d3sp1t3_all_OuR_rag3_w3_ar3_all_ju5t_rat5_1n_a_maz3}
"""

import socket
import ssl
import re
import heapq
import base64
import time
import unicodedata
import subprocess

# Target configuration
HOST = "localhost"
PORT = 5000

# ANSI color codes
ANSI_REGEX = re.compile(r'\x1b\[[0-9;]*m')

DIRECTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

# ============================================================================
# 1. Piece Valuation Engine
# ============================================================================
CHESS_PIECES = {
    '\u2659': 1, '\u2658': 3, '\u2657': 3, '\u2656': 5, '\u2655': 9, '\u2654': 100,
    '\u265F': 1, '\u265E': 3, '\u265D': 3, '\u265C': 5, '\u265B': 9, '\u265A': 100,
}

def is_wide(char: str) -> bool:
    """Checks if character takes 2 terminal columns (East Asian Width)."""
    cp = ord(char)
    if 0x1F000 <= cp <= 0x1F0FF:
        return True
    return unicodedata.east_asian_width(char) in ('W', 'F')

def get_piece_cost(char: str) -> int:
    """Calculates the movement cost weight of a tile piece."""
    if not char or char in (' ', '·', '#', '█'):
        return 0

    # 1. Chess
    if char in CHESS_PIECES:
        return CHESS_PIECES[char]

    cp = ord(char)

    # 2. Dice (U+2680 .. U+2685)
    if 0x2680 <= cp <= 0x2685:
        return cp - 0x2680 + 1

    # 3. Dominoes (U+1F063 .. U+1F08F)
    # left, right = divmod(ord(c) - 0x1F063, 7); cost = left + right
    if 0x1F063 <= cp <= 0x1F08F:
        left, right = divmod(cp - 0x1F063, 7)
        return left + right

    # 4. Mahjong (Bamboo, Chars, Dots)
    if 0x1F010 <= cp <= 0x1F018:  # Bamboo 1-9
        return cp - 0x1F010 + 1
    if 0x1F007 <= cp <= 0x1F00F:  # Chars 1-9
        return cp - 0x1F007 + 1
    if 0x1F019 <= cp <= 0x1F021:  # Dots 1-9
        return cp - 0x1F019 + 1

    # 5. Playing Cards (U+1F0A1 .. U+1F0DE)
    for suit_base in (0x1F0A0, 0x1F0B0, 0x1F0C0, 0x1F0D0):
        if suit_base + 1 <= cp <= suit_base + 0xE:
            rank = cp - suit_base
            if rank == 1:
                return 1
            elif 2 <= rank <= 10:
                return rank
            elif rank in (11, 12, 13, 14):
                return 10

    return 0

# ============================================================================
# 2. Redpwn Proof of Work Solver (Pure Python VDF)
# ============================================================================
MOD = (1 << 1279) - 1
EXP = (1 << 1277)

def solve_redpwn_pow(chal_str: str) -> str:
    """Solves redpwn VDF challenge directly in pure Python in ~0.2s."""
    parts = chal_str.strip().split('.')
    d_bytes = base64.b64decode(parts[1])
    d_bytes = b'\x00' * (4 - len(d_bytes)) + d_bytes
    d = int.from_bytes(d_bytes, 'big')
    x_bytes = base64.b64decode(parts[2])
    x = int.from_bytes(x_bytes, 'big')

    for _ in range(d):
        x = pow(x, EXP, MOD) ^ 1

    x_bytes = x.to_bytes((x.bit_length() + 7) // 8 or 1, 'big')
    return f"s.{base64.b64encode(x_bytes).decode()}"

# ============================================================================
# 3. ANSI-Aware Terminal Line Parser
# ============================================================================
def tokenize_ansi_line(line: str):
    """
    Splits an ANSI terminal line into character tokens while maintaining
    the active color state (detecting green entrance and red exit).
    """
    tokens = []
    i = 0
    active_color = None
    while i < len(line):
        if line[i] == '\x1b':
            m = ANSI_REGEX.match(line, i)
            if m:
                code = m.group(0)
                if '92m' in code:
                    active_color = 'green'
                elif '91m' in code:
                    active_color = 'red'
                elif '0m' in code:
                    active_color = None
                i = m.end()
                continue
        tokens.append((line[i], active_color))
        i += 1
    return tokens

def parse_terminal_maze(maze_lines):
    """
    Parses the 13 lines of the terminal maze (Top border, 11 rows, Bottom border).
    Correctly accounts for East Asian Width (wide characters taking 2 terminal columns).
    Returns (grid, enter_info, exit_info) where:
      enter_info = (side, (r, c), enter_direction)
      exit_info  = (side, (r, c), exit_direction)
    """
    enter_info = None
    exit_info = None

    # Line 0: Top border (╔═ [11 segments of 2 cols] ╗)
    top_toks = tokenize_ansi_line(maze_lines[0])
    idx = 2
    for c in range(11):
        if idx < len(top_toks):
            colr = top_toks[idx][1]
            if colr == 'green':
                enter_info = ('T', (0, c), 'D')
            elif colr == 'red':
                exit_info = ('T', (0, c), 'U')
        idx += 2

    # Line 12: Bottom border (╚═ [11 segments of 2 cols] ╝)
    bot_toks = tokenize_ansi_line(maze_lines[12])
    idx = 2
    for c in range(11):
        if idx < len(bot_toks):
            colr = bot_toks[idx][1]
            if colr == 'green':
                enter_info = ('B', (10, c), 'U')
            elif colr == 'red':
                exit_info = ('B', (10, c), 'D')
        idx += 2

    # Lines 1 to 11: Interior grid rows
    grid = {}
    for r in range(11):
        row_toks = tokenize_ansi_line(maze_lines[r + 1])

        # Left border check
        if row_toks[0][1] == 'green' or row_toks[1][1] == 'green':
            enter_info = ('L', (r, 0), 'R')
        elif row_toks[0][1] == 'red' or row_toks[1][1] == 'red':
            exit_info = ('L', (r, 0), 'L')

        # Parse the 11 cell tokens accounting for wide characters
        idx = 2  # skip left border
        for c in range(11):
            ch, _ = row_toks[idx]
            if is_wide(ch):
                grid[(r, c)] = ch
                idx += 1  # Wide character occupies the entire 2-column cell!
            else:
                grid[(r, c)] = ch
                idx += 2  # Narrow character occupies 1 column + 1 trailing space!

        # Right border check
        if idx < len(row_toks):
            colr = row_toks[idx][1]
            if colr == 'green':
                enter_info = ('R', (r, 10), 'L')
            elif colr == 'red':
                exit_info = ('R', (r, 10), 'R')

    return grid, enter_info, exit_info

# ============================================================================
# 4. Dijkstra Shortest Path Solver
# ============================================================================
def solve_dijkstra(grid, enter_info, exit_info):
    """Computes the unique minimum-cost move sequence."""
    start_pos = enter_info[1]
    target_pos = exit_info[1]

    initial_cost = 1 + get_piece_cost(grid[start_pos])
    dist = {start_pos: initial_cost}
    parent = {}
    pq = [(initial_cost, start_pos[0], start_pos[1])]

    while pq:
        cost, r, c = heapq.heappop(pq)
        if cost > dist[(r, c)]:
            continue
        if (r, c) == target_pos:
            break

        for move_name, (dr, dc) in DIRECTIONS.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < 11 and 0 <= nc < 11 and grid[(nr, nc)] != '#':
                edge_cost = 1 + get_piece_cost(grid[(nr, nc)])
                nxt_cost = cost + edge_cost
                if (nr, nc) not in dist or nxt_cost < dist[(nr, nc)]:
                    dist[(nr, nc)] = nxt_cost
                    parent[(nr, nc)] = ((r, c), move_name)
                    heapq.heappush(pq, (nxt_cost, nr, nc))

    # Reconstruct path
    curr = target_pos
    path = []
    while curr != start_pos:
        p_node, move = parent[curr]
        path.append(move)
        curr = p_node
    path.reverse()

    # Prepend mandatory entrance move, append mandatory exit move
    full_moves = enter_info[2] + "".join(path) + exit_info[2]
    return full_moves

# ============================================================================
# 5. Main Exploit Flow
# ============================================================================
def main():
    print("=" * 60)
    print("  SecurinetsENIT CTF - Captcha: Rats in a Maze Solver")
    print("  Author: MrXFuji")
    print("=" * 60)

    # Establish TLS connection
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    print(f"[*] Connecting to {HOST}:{PORT} over TLS...")
    raw_sock = socket.create_connection((HOST, PORT))
    tls_sock = context.wrap_socket(raw_sock)
    f = tls_sock.makefile('rw', encoding='utf-8', buffering=1)

    # Read banner and Proof of Work prompt
    while True:
        line = f.readline()
        if not line:
            break
        print(line.strip())
        if "proof of work: curl -sSfL https://pwn.red/pow | sh -s" in line:
            chal = line.split("sh -s")[-1].strip()
            print(f"[*] Extracting PoW challenge: {chal}")
            t0 = time.time()
            sol = solve_redpwn_pow(chal)
            print(f"[+] PoW solved in {time.time() - t0:.3f}s: {sol}")
            # Wait for 'solution: '
            f.readline() # solution:
            f.write(sol + "\n")
            f.flush()
            break

    # Loop through maze rounds dynamically until completion banner
    total_start = time.time()
    round_num = 0

    while True:
        line = f.readline()
        if not line:
            break
        if "ALL" in line and "ROUNDS CLEARED" in line:
            print(f"\n[+] {line.strip()}")
            break
        if "[ROUND " in line:
            round_num += 1
            # Read the 13 lines of the maze
            maze_lines = [f.readline().rstrip('\r\n') for _ in range(13)]
            # Read prompt line ("Submit move sequence...")
            prompt = f.readline()

            # Parse maze with ANSI colors and East Asian Width
            grid, enter_info, exit_info = parse_terminal_maze(maze_lines)

            # Solve path via Dijkstra
            moves = solve_dijkstra(grid, enter_info, exit_info)

            # Send solution
            f.write(moves + "\n")
            f.flush()

            # Read validation response
            res = f.readline().strip()
            print(f"[*] Round {round_num:3d} | Path: {moves:<25} | {res}")

    total_elapsed = time.time() - total_start
    if round_num > 0:
        print(f"\n[+] {round_num} ROUNDS SOLVED in {total_elapsed:.2f} seconds! (~{total_elapsed/round_num:.3f}s per round)")

    # Read final banner and flag
    print("\n" + "=" * 60)
    print("  FINAL FLAG OUTPUT:")
    print("=" * 60)
    while True:
        line = f.readline()
        if not line:
            break
        print(line, end='')

    print("\n" + "=" * 60)
    print("DISAMBIGUATION NOTE:")
    print("In FIGlet standard font, capital 'O' and digit '0' are visually identical.")
    print("From the lyric clue: 'despite all our rage, we are all just rats in a maze'")
    print("The word 'our' disambiguates as 'OuR'.")
    print("Correct Flag: Securinets{d3sp1t3_all_OuR_rag3_w3_ar3_all_ju5t_rat5_1n_a_maz3}")
    print("=" * 60)

    tls_sock.close()

if __name__ == '__main__':
    main()
