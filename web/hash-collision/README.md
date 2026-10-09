# hash-collision

**Category:** Web
**Difficulty:** Medium
**Port:** 80 (mapped to `8009` in `docker-compose.yml`)

## Story

A login that compares password hashes with PHP's loose `==`. Find the input whose MD5 starts with `0e` and the rest digits, and let type juggling treat two different strings as equal.

## Files

- application source (see the folder) — served inside the image
- `flag.txt` — organizer flag; baked into the image
- `Dockerfile`, `docker-compose.yml` — container build and runner
- `hints.md` — tiered hints
- `writeup.md` — intended solution
- `solve/` — reference solver (`./solve/solve.sh http://HOST:8009`)

## Running

```bash
docker compose up -d --build   # serves on http://localhost:8009
```

## Flag format

```text
SecurinetsENIT{...}
```
