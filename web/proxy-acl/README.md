# proxy-acl

**Category:** Web
**Difficulty:** Hard
**Port:** 80 (mapped to `8005` in `docker-compose.yml`)

## Story

A reverse proxy guards a 'secret' area with an ACL. The rules look airtight, but nginx path normalization and an `alias` mismatch let a crafted request slip past the gate to the protected content.

## Files

- application source (see the folder) — served inside the image
- `flag.txt` — organizer flag; baked into the image
- `Dockerfile`, `docker-compose.yml` — container build and runner
- `hints.md` — tiered hints
- `writeup.md` — intended solution
- `solve/` — reference solver (`./solve/solve.sh http://HOST:8005`)

## Running

```bash
docker compose up -d --build   # serves on http://localhost:8005
```

## Flag format

```text
SecurinetsENIT{...}
```
