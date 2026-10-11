from __future__ import annotations

import signal
import sys

EXPECTED = bytes([
    50, 239, 208, 169, 119, 71, 57, 229, 221, 161, 190, 106,
    4, 34, 228, 187, 157, 117, 55, 51, 246, 199, 132, 124,
    92, 17, 212, 223, 184, 99, 95, 7, 238, 198, 183, 163,
    81, 60, 2, 212, 161, 143
])
slots: list[int | None] = [None] * len(EXPECTED)
cursor = 0
epoch = 0


def noisy_signal(signum: int, frame: object) -> None:
    print(f"[noise:{signum}:{epoch & 3}]", file=sys.stderr)


signal.signal(signal.SIGINT, noisy_signal)
if hasattr(signal, "SIGTERM"):
    signal.signal(signal.SIGTERM, noisy_signal)


def push() -> None:
    global cursor
    raw = sys.stdin.buffer.read(1)
    if raw == b"":
        raise EOFError
    sys.stdin.buffer.readline()
    slots[cursor] = raw[0]
    cursor = (cursor + 1) % len(EXPECTED)


def rewind() -> None:
    global cursor, epoch
    cursor = (cursor + 4) % len(EXPECTED)
    epoch += 1


def verify() -> None:
    if epoch < len(EXPECTED) or cursor != 12:
        print("rejected")
        return
    ordered = bytes(
        (slots[(index * 5) % len(EXPECTED)] or 0)
        for index in range(len(EXPECTED))
    )
    print("accepted" if ordered == EXPECTED else "rejected")


def main() -> int:
    global epoch
    while True:
        print("[slot-pusher] 1=push 2=rewind 3=inspect 4=verify", flush=True)
        choice = sys.stdin.buffer.readline()
        if choice == b"":
            return 0
        try:
            command = int(choice.strip())
        except ValueError:
            print("bad command", flush=True)
            continue
        if command == 1:
            push()
        elif command == 2:
            rewind()
        elif command == 3:
            print(f"cursor={cursor} epoch={epoch}", flush=True)
        elif command == 4:
            verify()
            return 0
        else:
            print("bad command", flush=True)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EOFError:
        print("input ended")
