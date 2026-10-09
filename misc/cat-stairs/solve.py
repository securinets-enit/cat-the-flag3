#!/usr/bin/env python3
"""
Cat Stairs - solver (organizers only, do NOT ship to players).

ways(n) = sum of ways(n - s) for each allowed jump s, ways(0) = 1.
Written as a k x k matrix (k = biggest jump) and raised to the power n by
repeated squaring, so even n = 1e18 takes about 60 matrix multiplications.

Usage:
    python3 solve.py [host] [port]      # default localhost 1340
    python3 solve.py --check            # compare with the simple loop on small cases
"""
import random
import re
import socket
import sys

MOD = 1_000_000_007


def mat_mul(A, B):
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col)) % MOD for col in Bt] for row in A]


def mat_pow(M, p):
    n = len(M)
    R = [[int(i == j) for j in range(n)] for i in range(n)]   # identity
    while p:
        if p & 1:
            R = mat_mul(R, M)
        M = mat_mul(M, M)
        p >>= 1
    return R


def ways(n, jumps):
    k = max(jumps)
    M = [[0] * k for _ in range(k)]
    for s in jumps:
        M[0][s - 1] = 1          # first row: which earlier steps add up
    for i in range(1, k):
        M[i][i - 1] = 1          # other rows: shift the window down
    return mat_pow(M, n)[0][0]


def ways_loop(n, jumps):
    w = [1] + [0] * n
    for i in range(1, n + 1):
        w[i] = sum(w[i - s] for s in jumps if i - s >= 0) % MOD
    return w[n]


def check():
    assert ways(10, [1, 2, 3]) == 274
    assert ways(4, [1, 3, 5]) == 3
    assert ways(30, [1, 2]) == 1346269
    rng = random.Random(0)
    for _ in range(300):
        jumps = sorted(rng.sample(range(1, 13), rng.randint(1, 4)))
        n = rng.randint(0, 3000)
        assert ways(n, jumps) == ways_loop(n, jumps), (n, jumps)
    print("matrix method matches the simple loop on 300 random cases")


def remote(host, port):
    s = socket.create_connection((host, port), timeout=10)
    buf = ""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        buf += chunk.decode(errors="replace")
        m = re.search(r"Mimi can jump: ([\d ]+)\nSteps to the roof: (\d+)\nAnswer \(mod \d+\):\n> $", buf)
        if m:
            jumps = list(map(int, m.group(1).split()))
            n = int(m.group(2))
            s.sendall(f"{ways(n, jumps)}\n".encode())
            rnd = re.findall(r"Round (\d+)/", buf)[-1]
            print(f"round {rnd}: jumps={jumps} n={n}")
            buf = ""
    flag = re.search(r"SecurinetsENIT\{[^}]*\}", buf)
    print(flag.group(0) if flag else buf)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    else:
        remote(sys.argv[1] if len(sys.argv) > 1 else "localhost",
               int(sys.argv[2]) if len(sys.argv) > 2 else 1340)
