# Litter Shell

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Medium
**Points:** 250 (dynamic, minimum 100)

## Description

Mimi built a perfectly safe shell. Only harmless commands, no tricks allowed.
Somewhere on that machine, her treats are hidden.

**Connection:** `nc <host> 1345`

## Files

| File | Who gets it |
|---|---|
| nothing | Players only get the `nc` command |
| `challenge.yml` | CTFd import (ctfcli). Update `connection_info` with the real host |
| `src/shell.py`, `Dockerfile`, `docker-compose.yml` | Deployment |
| `flag.txt`, `solve.py` | Organizers only |

## Deployment

```bash
cd misc/litter-shell
docker compose up --build -d
python3 solve.py localhost 1345   # prints the flag
```
