# upload-htaccess

**Category:** Web
**Difficulty:** Medium/Hard
**Port:** 80 (mapped to `8006` in `docker-compose.yml`)

## Story

An upload form filters what you can send — but not carefully enough. Reconfigure how the server treats the upload directory with a file of your own, and make it execute what it should have rejected.

## Files

- application source (see the folder) — served inside the image
- `flag.txt` — organizer flag; baked into the image
- `Dockerfile`, `docker-compose.yml` — container build and runner
- `hints.md` — tiered hints
- `writeup.md` — intended solution
- `solve/` — reference solver (`./solve/solve.sh http://HOST:8006`)

## Running

```bash
docker compose up -d --build   # serves on http://localhost:8006
```

## Flag format

```text
SecurinetsENIT{...}
```
