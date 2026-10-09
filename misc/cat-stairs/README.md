# Cat Stairs

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Medium
**Points:** 250

## Description

Mimi climbs the stairs to the roof every night. She's picky about how far she jumps.
Tell her how many different ways she can get there... the buildings keep getting taller.

**Connection:** `nc <host> 1340`

## Files

| File | Who gets it |
|---|---|
| nothing | Players only get the `nc` command |
| `challenge.yml` | CTFd import (ctfcli). Update `connection_info` with the real host |
| `src/server.py`, `Dockerfile`, `docker-compose.yml` | Deployment |
| `flag.txt`, `solve.py` | Organizers only |

## Rounds

40 rounds, 3 seconds each (`ROUNDS`, `ROUND_TIME` in the Dockerfile).
Answers are modulo 1000000007. A wrong or late answer ends the game.

| Rounds | Jumps | Steps to the roof |
|---|---|---|
| 1–10 | simple sets like 1 2 3 | 5 to 30 |
| 11–20 | 2–4 jumps from 1–9 | 1,000 to 100,000 |
| 21–30 | 2–4 jumps from 1–10 | 200,000 to 1,000,000 |
| 31–40 | 2–4 jumps from 1–12 | 10^15 to 10^18 |

## Deployment

```bash
cd misc/cat-stairs
docker compose up --build -d
python3 solve.py localhost 1340   # plays all 40 rounds (~2 s) and prints the flag
python3 solve.py --check          # checks the math against a simple loop
```
