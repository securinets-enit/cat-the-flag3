# prepared-sqli

**Category:** Web
**Difficulty:** Medium
**Port:** 80 (mapped to `8008` in `docker-compose.yml`)

## Story

A shop that does everything right with PDO prepared statements — except one `ORDER BY` clause built from string concatenation. The app even serves its own source. Inject through the identifier the prepares never covered.

## Files

- application source (see the folder) — served inside the image
- `flag.txt` — organizer flag; baked into the image
- `Dockerfile`, `docker-compose.yml` — container build and runner
- `hints.md` — tiered hints
- `writeup.md` — intended solution
- `solve/` — reference solver (`./solve/solve.sh http://HOST:8008`)

## Running

```bash
docker compose up -d --build   # serves on http://localhost:8008
```

## Flag format

```text
SecurinetsENIT{...}
```
