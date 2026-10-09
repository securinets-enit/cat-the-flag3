# log-poison

**Category:** Web
**Difficulty:** Medium
**Port:** 80 (mapped to `8002` in `docker-compose.yml`)

## Story

The same page-including news app, but this time the flag isn't a file you can read directly. Poison something the server writes, then make it include that — turning file read into code execution.

## Files

- application source (see the folder) — served inside the image
- `flag.txt` — organizer flag; baked into the image
- `Dockerfile`, `docker-compose.yml` — container build and runner
- `hints.md` — tiered hints
- `writeup.md` — intended solution
- `solve/` — reference solver (`./solve/solve.sh http://HOST:8002`)

## Running

```bash
docker compose up -d --build   # serves on http://localhost:8002
```

## Flag format

```text
SecurinetsENIT{...}
```
