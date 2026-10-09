# Mimi's Vending Machine

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Easy
**Points:** 150 (dynamic, minimum 100)

## Description

Mimi opened a vending machine with the finest cat products.
The Golden Flag is right there on the menu. Too bad you only have 50 coins.

**Connection:** `nc <host> 1342`

## Files

| File | Who gets it |
|---|---|
| nothing | Players only get the `nc` command |
| `challenge.yml` | CTFd import (ctfcli). Update `connection_info` with the real host |
| `src/server.py`, `Dockerfile`, `docker-compose.yml` | Deployment |
| `flag.txt`, `solve.py` | Organizers only |

## Deployment

```bash
cd misc/vending-machine
docker compose up --build -d
python3 solve.py localhost 1342   # prints the flag
```
