# Liar's Treat

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Very hard
**Points:** 800 (dynamic, minimum 300)

## Description

Mimi hides a treat in one of her many boxes and lets you ask questions.
She never said she would tell the truth.

**Connection:** `nc <host> 1343`

## Files

| File | Who gets it |
|---|---|
| nothing | Players only get the `nc` command |
| `challenge.yml` | CTFd import (ctfcli). Update `connection_info` with the real host |
| `src/server.py`, `Dockerfile`, `docker-compose.yml` | Deployment |
| `flag.txt`, `solve.py` | Organizers only |

## Game

10 rounds, 30 seconds each (`ROUNDS`, `QUESTIONS`, `LIES`, `ROUND_TIME` in
the Dockerfile). Each round: a box 0–65535, at most 26 parity questions,
2 of which are answered with a lie, then one guess.

## Deployment

```bash
cd misc/liars-treat
docker compose up --build -d
pip install numpy                  # solver only
python3 solve.py --check           # proves the code corrects any 2 lies
python3 solve.py localhost 1343    # plays 10 rounds (~12 s) and prints the flag
```
