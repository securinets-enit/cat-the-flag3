# Admin Mimi

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Easy
**Points:** 150 (dynamic, minimum 100)

## Description

Welcome to Catbook, the social network for cats.
Only the admin can open the admin panel, and the name "admin" is already taken.

**Connection:** `nc <host> 1344`

## Files

| File | Who gets it |
|---|---|
| nothing | Players only get the `nc` command |
| `challenge.yml` | CTFd import (ctfcli). Update `connection_info` with the real host |
| `src/server.py`, `Dockerfile`, `docker-compose.yml` | Deployment |
| `flag.txt`, `solve.py` | Organizers only |

## Deployment

```bash
cd misc/admin-mimi
docker compose up --build -d
python3 solve.py localhost 1344   # prints the flag
```
