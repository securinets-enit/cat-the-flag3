# Cat Jail v1

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Easy–medium
**Points:** 200

## Description

Mimi built a sandbox to keep humans away from her treats.
She'll happily run your Python... as long as you don't say any of the words she hates.

**Connection:** `nc <host> 1337`

## Files

| File | Who gets it |
|---|---|
| nothing | Players only get the `nc` command |
| `challenge.yml` | CTFd import (ctfcli). Update `connection_info` with the real host |
| `src/jail.py`, `Dockerfile`, `docker-compose.yml` | Deployment |
| `flag.txt`, `solve.py` | Organizers only |

## Deployment

```bash
cd misc/cat-jail-v1
docker compose up --build -d
nc localhost 1337
python3 solve.py localhost 1337   # should print the flag
```

Players get real code execution, so the container is locked down: a new
process per connection killed after 60 s, non-root user, read-only
filesystem, no Linux capabilities, 64 processes and 128 MB max.
