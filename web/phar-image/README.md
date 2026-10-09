# phar-image

**Category:** Web
**Difficulty:** Hard
**Port:** 80 (mapped to `8004` in `docker-compose.yml`)

## Story

An image 'gallery' that inspects uploaded files. Nothing obviously runs your code — until you realise a Phar archive's metadata is deserialised, and the app ships just the right gadgets to turn that into a POP chain.

## Files

- application source (see the folder) — served inside the image
- `flag.txt` — organizer flag; baked into the image
- `Dockerfile`, `docker-compose.yml` — container build and runner
- `hints.md` — tiered hints
- `writeup.md` — intended solution
- `solve/` — reference solver (`./solve/solve.sh http://HOST:8004`)

## Running

```bash
docker compose up -d --build   # serves on http://localhost:8004
```

## Flag format

```text
SecurinetsENIT{...}
```
