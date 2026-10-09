# Fish Heist

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Medium
**Points:** 250

## Description

You and Mimi share piles of fish. You take turns stealing from one pile at a time.
Mimi has never lost a game. Beat her 20 times in a row.

**Connection:** `nc <host> 1341`

## Files

| File | Who gets it |
|---|---|
| nothing | Players only get the `nc` command |
| `challenge.yml` | CTFd import (ctfcli). Update `connection_info` with the real host |
| `src/server.py`, `Dockerfile`, `docker-compose.yml` | Deployment |
| `flag.txt`, `solve.py` | Organizers only |

## Games

20 games in a row, 10 seconds per answer (`GAMES`, `MISERE_FROM`, `MOVE_TIME`
in the Dockerfile). Before each game the player chooses who starts, so every
game can be won with perfect play. Mimi always plays perfectly.

| Games | Piles | Rule |
|---|---|---|
| 1–5 | 2–3 piles, 1–9 fish | Last fish wins |
| 6–15 | 4–8 piles, up to 1000 fish | Last fish wins |
| 16–20 | 3–6 piles, up to 60 fish | Last fish **loses** |

## Deployment

```bash
cd misc/fish-heist
docker compose up --build -d
python3 solve.py localhost 1341   # wins all 20 games and prints the flag
```
