# Cat Jail v2

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Hard
**Points:** 400

## Description

Mimi read every writeup of her first jail. She is not amused.
The treats are still in there, and so is she.

**Connection:** `nc <host> 1338`

## Files

| File | Who gets it |
|---|---|
| nothing | Players only get the `nc` command |
| `challenge.yml` | CTFd import (ctfcli). Update `connection_info` with the real host |
| `src/jail.py`, `Dockerfile`, `docker-compose.yml` | Deployment |
| `flag.txt`, `solve.py` | Organizers only |

## Deployment

```bash
cd misc/cat-jail-v2
docker compose up --build -d
python3 solve.py localhost 1338   # should print the flag
```

Same lockdown as v1: a new process per connection killed after 60 s,
non-root user, read-only filesystem, no Linux capabilities,
64 processes and 128 MB max.
