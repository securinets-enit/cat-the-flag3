# Task 4 — The Implant

**Difficulty:** Hard

## Brief

The IR team recovered the second-stage binary, a network capture, and host-side
telemetry collected while the implant was running.

Correlate all three sources to answer the 30 analysis questions.

## Evidence

- `evidence/gh-completion` — ELF implant
- `evidence/traffic.pcapng` — network capture
- `evidence/filesystem/` — hash, size, permissions, cron
- `evidence/process/` — PID, PPID, cwd, exe path
- `evidence/network/` — sockets, FDs, DNS

## Running

    docker compose run --rm task-04

Inside:

    cd /case
    ./implant

Tools: `file`, `strings`, `readelf`, `tshark`, `openssl`.

## Flag format

`SecurinetsENIT{...}`
