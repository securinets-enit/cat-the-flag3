# mirage

**Category:** Web
**Difficulty:** Hard
**Port:** 8010 (mapped to `8010` in `docker-compose.yml`)

## Story

A profile service signs sessions with a weak HS256 secret. Forge your way to admin, then abuse a profile-merge that pollutes `Object.prototype` to smuggle `execArgv` into a `fork()` — code execution that reads the flag.

## Files

- application source (see the folder) — served inside the image
- `flag.txt` — organizer flag; baked into the image
- `Dockerfile`, `docker-compose.yml` — container build and runner
- `hints.md` — tiered hints
- `writeup.md` — intended solution
- `solve/` — reference solver (`./solve/solve.sh http://HOST:8010`)

## Running

```bash
docker compose up -d --build   # serves on http://localhost:8010
```

## Flag format

```text
SecurinetsENIT{...}
```
