# filter-chain

**Category:** Web
**Difficulty:** Hard
**Port:** 80 (mapped to `8003` in `docker-compose.yml`)

## Story

Local file inclusion with a twist: you can't drop a payload on disk. Build a `php://filter` conversion chain that synthesises your PHP entirely in the inclusion path, and reach RCE from a read primitive alone.

## Files

- application source (see the folder) — served inside the image
- `flag.txt` — organizer flag; baked into the image
- `Dockerfile`, `docker-compose.yml` — container build and runner
- `hints.md` — tiered hints
- `writeup.md` — intended solution
- `solve/` — reference solver (`./solve/solve.sh http://HOST:8003`)

## Running

```bash
docker compose up -d --build   # serves on http://localhost:8003
```

## Flag format

```text
SecurinetsENIT{...}
```
