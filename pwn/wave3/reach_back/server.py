#!/usr/bin/python3

import base64
import binascii
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import tempfile

MAX_SO_BYTES = 256 * 1024
MAX_BASE64_BYTES = ((MAX_SO_BYTES + 2) // 3) * 4
MAX_OUTPUT_BYTES = 1024 * 1024
RUN_TIMEOUT_SECONDS = 5
BASE_DIR = Path(__file__).resolve().parent
HARNESS = BASE_DIR / "harness"


def emit(message: bytes) -> None:
    try:
        sys.stdout.buffer.write(message)
        sys.stdout.buffer.flush()
    except BrokenPipeError:
        raise SystemExit(0)


def child_limits() -> None:
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
    resource.setrlimit(resource.RLIMIT_FSIZE,
                       (MAX_OUTPUT_BYTES, MAX_OUTPUT_BYTES))
    resource.setrlimit(resource.RLIMIT_NOFILE, (16, 16))
    resource.setrlimit(resource.RLIMIT_NPROC, (1, 1))
    resource.setrlimit(resource.RLIMIT_AS,
                       (128 * 1024 * 1024, 128 * 1024 * 1024))


def receive_upload() -> bytes:
    emit(b"Send solve.so as one base64 line:\n")
    line = sys.stdin.buffer.readline(MAX_BASE64_BYTES + 2)
    if not line:
        raise ValueError("no upload received")
    if len(line) > MAX_BASE64_BYTES + 1:
        raise ValueError("upload is too large")

    encoded = line.rstrip(b"\r\n")
    if not encoded:
        raise ValueError("empty upload")
    if len(encoded) > MAX_BASE64_BYTES:
        raise ValueError("upload is too large")
    try:
        decoded = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as error:
        raise ValueError("malformed base64") from error
    if not decoded or len(decoded) > MAX_SO_BYTES:
        raise ValueError("decoded upload size is outside the allowed range")
    return decoded


def run_harness(upload: bytes) -> int:
    descriptor = -1
    upload_path = ""
    try:
        descriptor, upload_path = tempfile.mkstemp(
            prefix="reach-back-", suffix=".so", dir="/tmp"
        )
        os.fchmod(descriptor, 0o400)
        with os.fdopen(descriptor, "wb", closefd=True) as upload_file:
            descriptor = -1
            upload_file.write(upload)
            upload_file.flush()

        with tempfile.TemporaryFile(mode="w+b", dir="/tmp") as output_file:
            try:
                completed = subprocess.run(
                    [str(HARNESS), upload_path],
                    stdin=subprocess.DEVNULL,
                    stdout=output_file,
                    stderr=subprocess.STDOUT,
                    env={"PATH": "/usr/bin:/bin", "LANG": "C"},
                    timeout=RUN_TIMEOUT_SECONDS,
                    check=False,
                    close_fds=True,
                    start_new_session=True,
                    preexec_fn=child_limits,
                )
                timed_out = False
            except subprocess.TimeoutExpired:
                completed = None
                timed_out = True

            output_file.seek(0)
            remaining = MAX_OUTPUT_BYTES
            while remaining:
                chunk = output_file.read(min(65536, remaining))
                if not chunk:
                    break
                emit(chunk)
                remaining -= len(chunk)

        if timed_out:
            emit(b"\n[server] execution timed out.\n")
            return 1
        elif completed is not None and completed.returncode != 0:
            emit(f"\n[server] harness exited with status "
                 f"{completed.returncode}.\n".encode())
            return 1
        return 0
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if upload_path:
            try:
                os.unlink(upload_path)
            except FileNotFoundError:
                pass


def main() -> int:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    try:
        upload = receive_upload()
        return run_harness(upload)
    except ValueError as error:
        emit(f"[server] rejected: {error}.\n".encode())
        return 1
    except OSError as error:
        emit(f"[server] internal error: {error.strerror}.\n".encode())
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
