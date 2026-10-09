# Cat Jail v3: Paws Off

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Very hard
**Points:** 600 (dynamic, minimum 200)

## Description

Mimi locked her catnip away and built her strictest jail yet.
This time, she says, you won't even be able to lift a paw.

**Connection:** `nc <host> 1346`

## Files

| File | Who gets it |
|---|---|
| nothing | Players only get the `nc` command |
| `challenge.yml` | CTFd import (ctfcli). Update `connection_info` with the real host |
| `src/jail.py`, `Dockerfile`, `docker-compose.yml` | Deployment (the flag is copied to `/app/catnip`) |
| `flag.txt`, `solve.py` | Organizers only |

## Deployment

```bash
cd misc/cat-jail-v3
docker compose up --build -d
python3 solve.py localhost 1346   # prints the flag
```

Same lockdown as v1 and v2: a new process per connection killed after 60 s,
non-root user, read-only filesystem, no Linux capabilities, 64 processes and
128 MB max. The image must use Python 3.9 or newer (lambda decorators).
