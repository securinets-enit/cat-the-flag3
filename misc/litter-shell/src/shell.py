#!/usr/bin/env python3
# Litter Shell - SecurinetsENIT Cat The Flag v3
# Author: r3t0x
#
# A "safe" shell: only a few harmless-looking commands, no chaining, no
# redirections, and a list of forbidden words. Some allowed tools can still
# read files (e.g. `date -f FILE` prints every line it cannot parse).

import glob
import re
import shlex
import subprocess
import sys

ALLOWED = {"ls", "echo", "find", "date", "wc", "id", "pwd", "whoami"}
FORBIDDEN_CHARS = set(";|&$`<>\\\n")
# "flag" is blocked anywhere; the others only as whole words (so /usr/share is fine)
FORBIDDEN_ANYWHERE = ["flag"]
FORBIDDEN_WORDS = [
    "cat", "sh", "bash", "dash", "less", "more", "head", "tail", "nl", "tac", "grep",
    "sed", "awk", "sort", "uniq", "cut", "paste", "rev", "tee", "xargs", "env",
    "python3", "python", "perl", "ruby", "php", "lua", "base64", "base32", "xxd", "od",
    "hexdump", "strings", "dd", "cp", "mv", "vi", "vim", "nano", "ed", "diff", "cmp",
    "iconv", "busybox", "exec", "execdir", "ok", "okdir", "fprintf", "fls", "fprint",
]
WORD_RE = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(map(re.escape, FORBIDDEN_WORDS)) + r")(?![A-Za-z0-9])", re.I)
MAX_COMMANDS = 60
HOME = "/home/mimi"

BANNER = r"""
   /\_/\    MIMI'S LITTER SHELL
  ( o.o )   A perfectly safe shell. Mimi checked it herself.
   > ^ <    Allowed commands: ls echo find date wc id pwd whoami
"""


def say(msg=""):
    sys.stdout.write(msg + ("\n" if not msg.endswith("\n") else ""))
    sys.stdout.flush()


def expand(args):
    """Shell-style wildcards (*, ?, [..]) are expanded after the word check, like a real shell."""
    out = []
    for a in args:
        if any(ch in a for ch in "*?["):
            out.extend(sorted(glob.glob(a, root_dir=HOME)) or [a])
        else:
            out.append(a)
    return out


def main():
    say(BANNER)
    for _ in range(MAX_COMMANDS):
        sys.stdout.write("mimi@litter:~$ ")
        sys.stdout.flush()
        line = sys.stdin.readline()
        if not line:
            return
        line = line.strip()
        if not line:
            continue
        if line in ("exit", "quit", "logout"):
            say("Mimi buries the shell in the litter. Bye.")
            return

        if FORBIDDEN_CHARS & set(line):
            say("Mimi hisses: no special characters in her litter box.")
            continue
        low = line.lower()
        bad = next((w for w in FORBIDDEN_ANYWHERE if w in low), None)
        m = WORD_RE.search(line)
        bad = bad or (m.group(1).lower() if m else None)
        if bad:
            say(f"Mimi hisses: '{bad}' is not allowed.")
            continue
        try:
            args = shlex.split(line)
        except ValueError:
            say("Mimi can't read that.")
            continue
        if args[0] not in ALLOWED:
            say(f"{args[0]}: command not allowed")
            continue

        try:
            res = subprocess.run(expand(args), cwd=HOME, capture_output=True, text=True,
                                 timeout=5, env={"PATH": "/usr/bin:/bin", "HOME": HOME, "LANG": "C"})
            out = (res.stdout + res.stderr)[:8000]
            if out:
                say(out)
        except subprocess.TimeoutExpired:
            say("Mimi got bored waiting.")
        except FileNotFoundError:
            say(f"{args[0]}: not found")
    say("Mimi is tired. The litter shell closes.")


if __name__ == "__main__":
    main()
