#!/usr/bin/env python3
"""
verify.py — connect to each asker over TCP, feed answers, confirm flag.

Usage:
    python3 verify.py
    python3 verify.py --task task-02-the-recon
    python3 verify.py --verbose
"""

import argparse
import socket
import sys
import time

TASKS = {
    "task-02-the-recon": {
        "host": "localhost",
        "port": 9999,
        "answers": [
            "2026-04-30",
            "godaddy",
            "carl.ns.cloudflare.com,ivy.ns.cloudflare.com",
            "104.21.95.116,172.67.144.188",
            "cloudflare",
            "ye1",
            "letsencrypt",
            "2026-09-16",
            "2026-12-15",
            "90",
            "*.cdnjs-mirror.net,cdnjs-mirror.net",
            "a3f54b3a3cf50036d8448e6b26c6ef71f14bae603e5f7f7d6bd318f3cf89d8dd",
            "technology / web & hosting",
            "suspicious",
        ],
        "expected_flag": "SecurinetsENIT{9b6d946fc44eb755d906b366c7c794f1}",
        "timeout": 30,
    },
    "task-03-the-dropper": {
        "host": "localhost",
        "port": 9998,
        "answers": [
            "gh-completion",
            "curl",
            "https://cdnjs-mirror.net/assets/gh-2.42.1-shell-helper.bin?build=75efb0959defbc4b1bdcc6247381b437",
            "75efb0959defbc4b1bdcc6247381b437",
            "build",
            "~/.local/share/gh-cli/gh-completion",
            "cron",
            "*/30 * * * *",
            "@reboot",
            "crontab",
            "nohup",
            "suppress errors",
        ],
        "expected_flag": "SecurinetsENIT{75efb0959defbc4b1bdcc6247381b437}",
        "timeout": 30,
    },
    "task-04-the-implant": {
        "host": "localhost",
        "port": 9997,
        "answers": [
            "elf",
            "x86-64",
            "yes",
            "19969992",
            "afad825988139b2ab9a72611d4717ce5",
            "13352c0c87c485a1616d6bde5037005cd4f68249f5061d51273a2f8af5403f93",
            "root",
            "0755",
            "2552",
            "1",
            "/tmp/gh-extract/gh_2.42.1_linux_amd64",
            "/root/.local/share/gh-cli/gh-completion",
            "2",
            "*/30 * * * *",
            "@reboot",
            "cdnjs-mirror.net",
            "gh-actions-runner.xyz",
            "443",
            "10",
            "cloudflare",
            "T1071.001",
            "T1053.003",
            "TLS1.2",
            "20b279993ae2e137e62b9647c6d768fb",
            "11",
            "3",
            "h2",
            "10",
            "yes",
            "5",
        ],
        "expected_flag": "SecurinetsENIT{5398f82818903750fc0d72e94c5f3304}",
        "timeout": 30,
    },
}


def run_task(name, spec, verbose=False):
    print(f"\n\033[1;34m▶ {name}\033[0m  ({spec['host']}:{spec['port']})")
    print(f"  feeding {len(spec['answers'])} answers")

    t0 = time.time()
    try:
        s = socket.create_connection(
            (spec["host"], spec["port"]),
            timeout=spec["timeout"],
        )
    except (socket.error, OSError) as e:
        print(f"  \033[1;31m✗ cannot connect: {e}\033[0m")
        return False

    s.settimeout(spec["timeout"])
    all_output = b""

    try:
        for ans in spec["answers"]:
            # Read until the server asks for input (or has finished).
            buf = b""
            deadline = time.time() + spec["timeout"]
            while time.time() < deadline:
                if b"Your Answer:" in buf or b"Here is your flag" in buf:
                    break
                try:
                    chunk = s.recv(4096)
                except socket.timeout:
                    break
                if not chunk:
                    break
                buf += chunk

            all_output += buf

            # Send the answer.
            try:
                s.sendall((ans + "\n").encode())
            except (socket.error, OSError):
                break

        # Drain the tail.
        while True:
            try:
                chunk = s.recv(4096)
            except socket.timeout:
                break
            if not chunk:
                break
            all_output += chunk
    except Exception as e:
        print(f"  \033[1;31m✗ socket error: {e}\033[0m")
        s.close()
        return False

    s.close()
    elapsed = time.time() - t0
    output = all_output.decode(errors="replace")

    if verbose:
        print("  ─── output ───")
        for line in output.splitlines():
            print(f"  {line}")
        print("  ──────────────")

    expected = spec["expected_flag"]
    if expected in output:
        print(f"  \033[1;32m✓ PASS\033[0m  ({elapsed:.1f}s)")
        print(f"  flag: {expected}")
        return True

    print(f"  \033[1;31m✗ FAIL\033[0m  ({elapsed:.1f}s)")
    print(f"  expected: {expected}")
    for line in output.splitlines()[-10:]:
        print(f"    {line}")
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", help="run a single task by folder name")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.task:
        if args.task not in TASKS:
            print(f"unknown task: {args.task}")
            print(f"available: {', '.join(TASKS.keys())}")
            return 1
        selected = {args.task: TASKS[args.task]}
    else:
        selected = TASKS

    passed = 0
    failed = 0
    for name, spec in selected.items():
        if run_task(name, spec, verbose=args.verbose):
            passed += 1
        else:
            failed += 1

    print()
    print("=" * 50)
    print(f"  \033[1;32m{passed} passed\033[0m   "
          f"\033[1;31m{failed} failed\033[0m   "
          f"total {passed + failed}")
    print("=" * 50)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
