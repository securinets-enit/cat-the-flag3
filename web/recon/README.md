# recon

**Category:** Web
**Difficulty:** Warmup
**Port:** 80 (mapped to `8000` in `docker-compose.yml`)

## Story

A static site that says a little too much. Read what the server volunteers — robots entries, forgotten paths, and comments left in the source — and follow the trail to the flag.

## Files

- application source (see the folder) — served inside the image
- `flag.txt` — organizer flag; baked into the image
- `Dockerfile`, `docker-compose.yml` — container build and runner
- `hints.md` — tiered hints
- `writeup.md` — intended solution
- `solve/` — reference solver (`./solve/solve.sh http://HOST:8000`)

## Running

```bash
docker compose up -d --build   # serves on http://localhost:8000
```

## Flag format

```text
SecurinetsENIT{...}
```
