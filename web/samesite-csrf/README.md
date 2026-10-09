# samesite-csrf

**Category:** Web
**Difficulty:** Medium
**Port:** 8007 (mapped to `8007` in `docker-compose.yml`)

## Story

A note-taking app with an admin bot. SameSite cookies are supposed to stop cross-site requests, but a stored input becomes DOM XSS, and the right CSP pivot lets you ride the admin's session to the flag.

## Files

- application source (see the folder) — served inside the image
- `flag.txt` — organizer flag; baked into the image
- `Dockerfile`, `docker-compose.yml` — container build and runner
- `hints.md` — tiered hints
- `writeup.md` — intended solution
- `solve/` — reference solver (`./solve/solve.sh http://HOST:8007`)

## Running

```bash
docker compose up -d --build   # serves on http://localhost:8007
```

## Flag format

```text
SecurinetsENIT{...}
```
