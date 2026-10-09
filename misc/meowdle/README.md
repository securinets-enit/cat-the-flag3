# Meowdle

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Medium
**Points:** 250

## Description

Mimi got addicted to Wordle, so she made her own.
She says no human can beat her 30 times in a row.
She also gets grumpy when she's losing.

**Connection:** `nc <host> 1339`

## Files

| File | Who gets it |
|---|---|
| `dist/words.txt` | Players (all 4389 possible words) |
| `challenge.yml` | CTFd import (ctfcli). Update `connection_info` with the real host |
| `src/server.py`, `Dockerfile`, `docker-compose.yml` | Deployment |
| `flag.txt`, `solve.py` | Organizers only |

## Game settings

Set in the `Dockerfile` (environment variables):

| Variable | Default | Meaning |
|---|---|---|
| `ROUNDS` | 30 | Games to win in a row |
| `MAX_GUESSES` | 7 | Guesses per game |
| `TIME_LIMIT` | 60 | Seconds for the whole run |
| `LIE_FROM` | 21 | From this round on, one tile of one of the first 3 feedback rows is wrong. `0` = no lies |

## Deployment

```bash
cd misc/meowdle
docker compose up --build -d
python3 solve.py localhost 1339   # prints the flag (~5 s)
```

With lies on, the reference solver wins a full run about 7 times out of 10;
a lost run just means reconnecting. `python3 solve.py --sim 200` measures the
win rate of a single lying round offline.
