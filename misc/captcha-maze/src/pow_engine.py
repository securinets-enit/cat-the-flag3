"""
SecurinetsENIT CTF 2026 - Misc Challenge: Captcha: Rats in a Maze
Author: MrXFuji

Redpwn Proof-of-Work (VDF) implementation in pure Python.
Compatible with https://pwn.red/pow and https://github.com/redpwn/pow
"""

import base64
import os

MOD = (1 << 1279) - 1
EXP = (1 << 1277)
ONE = 1
TWO = 2
VERSION = "s"

def generate_challenge(difficulty: int = 1500) -> str:
    """Generates a standard redpwnpow challenge string."""
    b = os.urandom(16)
    d_bytes = difficulty.to_bytes(4, 'big')
    return f"{VERSION}.{base64.b64encode(d_bytes).decode()}.{base64.b64encode(b).decode()}"

def solve_challenge(chal_str: str) -> str:
    """Solves a redpwnpow challenge string in Python."""
    parts = chal_str.strip().split('.')
    if len(parts) != 3 or parts[0] != VERSION:
        raise ValueError("Invalid challenge format")
    d_bytes = base64.b64decode(parts[1])
    d_bytes = b'\x00' * (4 - len(d_bytes)) + d_bytes
    d = int.from_bytes(d_bytes, 'big')
    x = int.from_bytes(base64.b64decode(parts[2]), 'big')

    for _ in range(d):
        x = pow(x, EXP, MOD) ^ ONE

    x_bytes = x.to_bytes((x.bit_length() + 7) // 8 or 1, 'big')
    return f"{VERSION}.{base64.b64encode(x_bytes).decode()}"

def verify_solution(chal_str: str, sol_str: str) -> bool:
    """Verifies a redpwnpow solution string."""
    try:
        parts = chal_str.strip().split('.')
        if len(parts) != 3 or parts[0] != VERSION:
            return False
        d_bytes = base64.b64decode(parts[1])
        d_bytes = b'\x00' * (4 - len(d_bytes)) + d_bytes
        d = int.from_bytes(d_bytes, 'big')
        x = int.from_bytes(base64.b64decode(parts[2]), 'big')

        sol_parts = sol_str.strip().split('.')
        if len(sol_parts) != 2 or sol_parts[0] != VERSION:
            return False
        y = int.from_bytes(base64.b64decode(sol_parts[1]), 'big')

        for _ in range(d):
            y = y ^ ONE
            y = pow(y, TWO, MOD)

        return (x == y) or ((MOD - x) == y)
    except Exception:
        return False
