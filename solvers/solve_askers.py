#!/usr/bin/env python3
"""
End-to-end solver for every TCP asker (threat-intel + dfir) on a deployed server.

For each asker it reads the questions/answers straight from the asker's Go source and the
port from its Dockerfile, then plays the quiz one question at a time and checks:
  - every correct answer is accepted ("Correct!"),
  - the flag printed at the end matches flag.txt,
  - with --wrong: a wrong answer to question 1 is rejected ("Incorrect").

Usage (from anywhere inside the repo):
    python3 solvers/solve_askers.py                       # all askers on asker.securinets-enit.club
    python3 solvers/solve_askers.py --host 35.184.21.49
    python3 solvers/solve_askers.py zebrocy recon         # only askers whose folder matches
    python3 solvers/solve_askers.py --wrong               # also check wrong answers are rejected
    python3 solvers/solve_askers.py --list                # show discovered askers, no network

Exit code is 0 only if every tested asker passes.
"""

import argparse
import json
import re
import socket
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_HOST = "asker.securinets-enit.club"
PROMPT = b"Your Answer: "

GO_STR = r'"(?:[^"\\]|\\.)*"'
# threat-intel style:  {"question", []string{"a", "b"}},
MULTI = re.compile(r"^\s*\{(" + GO_STR + r"),\s*\[\]string\{(.*)\}\},\s*$", re.M)
# dfir style:          {"question", "answer"},
SINGLE = re.compile(r"^\s*\{(" + GO_STR + r"),\s*(" + GO_STR + r")\},\s*$", re.M)


def go_unquote(lit):
    # Go interpreted string literals used here are valid JSON strings.
    return json.loads(lit)


def discover():
    askers = []
    for dockerfile in sorted(REPO.rglob("Dockerfile")):
        d = dockerfile.parent
        port = re.search(r"^EXPOSE\s+(\d+)", dockerfile.read_text(), re.M)
        if not port or not (d / "flag.txt").exists():
            continue
        for go in sorted(d.glob("*.go")):
            src = go.read_text()
            qa = [(go_unquote(q), go_unquote(re.match(GO_STR, a.strip()).group(0))) for q, a in MULTI.findall(src)]
            qa = qa or [(go_unquote(q), go_unquote(a)) for q, a in SINGLE.findall(src)]
            if qa:
                rel = d.relative_to(REPO)
                name = rel.parent.name if rel.name == "asker" else rel.name
                askers.append(dict(name=name, path=str(rel), port=int(port.group(1)),
                                   qa=qa, flag=(d / "flag.txt").read_text().strip()))
                break
    return sorted(askers, key=lambda a: a["port"])


class Session:
    def __init__(self, host, port, timeout):
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.buf = b""

    def read_until_prompt(self):
        """Return everything up to the next answer prompt, or until the server closes."""
        while PROMPT not in self.buf:
            chunk = self.sock.recv(65536)
            if not chunk:
                out, self.buf = self.buf, b""
                return out.decode(errors="replace"), False
            self.buf += chunk
        out, self.buf = self.buf.split(PROMPT, 1)
        return out.decode(errors="replace"), True

    def send(self, line):
        self.sock.sendall(line.encode() + b"\n")

    def close(self):
        self.sock.close()


def strip_ansi(s):
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


def solve(a, host, timeout, wrong):
    s = Session(host, a["port"], timeout)
    try:
        _, more = s.read_until_prompt()
        if not more:
            return False, "server closed before the first question"
        if wrong:
            s.send("definitely-not-the-answer-1337")
            reply, more = s.read_until_prompt()
            if "Incorrect" not in reply:
                return False, f"wrong answer to Q1 was not rejected: {strip_ansi(reply)[:150]!r}"
        for i, (question, answer) in enumerate(a["qa"], 1):
            s.send(answer)
            reply, more = s.read_until_prompt()
            if "Correct!" not in reply:
                return False, f"Q{i} rejected answer {answer!r}\n         question: {question}\n         server:   {strip_ansi(reply).strip()[:200]!r}"
        if more:
            return False, "server asked more questions than the source defines (stale deployment?)"
        if a["flag"] not in reply:
            return False, f"flag mismatch: expected {a['flag']}, got {strip_ansi(reply).strip()[-200:]!r}"
        return True, f"{len(a['qa'])}/{len(a['qa'])} answers accepted, flag OK"
    finally:
        s.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("only", nargs="*", help="only test askers whose folder path contains one of these")
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--timeout", type=float, default=15)
    ap.add_argument("--wrong", action="store_true", help="also check that a wrong answer is rejected")
    ap.add_argument("--list", action="store_true", help="list discovered askers and exit")
    args = ap.parse_args()

    askers = [a for a in discover() if not args.only or any(o in a["path"] for o in args.only)]
    if args.list:
        for a in askers:
            print(f"{a['port']}  {a['name']:<16} {len(a['qa']):>2} questions  {a['path']}")
        return
    if not askers:
        sys.exit("no askers matched")

    print(f"Testing {len(askers)} asker(s) on {args.host}\n")
    failed = 0
    for a in askers:
        try:
            ok, msg = solve(a, args.host, args.timeout, args.wrong)
        except OSError as e:
            ok, msg = False, f"connection error: {e}"
        failed += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {a['port']}  {a['name']:<16} {msg}")
    print(f"\n{len(askers) - failed}/{len(askers)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
