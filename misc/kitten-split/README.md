# Kitten Split

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Insane
**Points:** 1000 (dynamic, minimum 400)

## Description

You beat Mimi at Fish Heist. She was furious.
She came back with new rules, and she swears nobody will ever beat her again.

**Connection:** `nc <host> 1347`

## Files

| File | Who gets it |
|---|---|
| nothing | Players only get the `nc` command |
| `challenge.yml` | CTFd import (ctfcli). Update `connection_info` with the real host |
| `src/server.py`, `Dockerfile`, `docker-compose.yml` | Deployment |
| `flag.txt`, `solve.py` | Organizers only |

## Game

10 games in a row against a perfect opponent, 5 seconds per answer
(`GAMES`, `MAX_PILE`, `MOVE_TIME` in the Dockerfile). 3–6 piles of 1–60 fish.
A move: take 1, 3 or 4 fish from one pile, or split one pile into two
non-empty piles of different sizes. The last move wins. Before each game the
player chooses who starts, so every game can be won with perfect play.

## Deployment

```bash
cd misc/kitten-split
docker compose up --build -d
python3 solve.py localhost 1347   # wins 10 games (~15 s) and prints the flag
```
