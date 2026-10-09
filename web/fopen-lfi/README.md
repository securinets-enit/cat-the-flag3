# fopen-lfi

**Category:** Web
**Difficulty:** Easy
**Port:** 80 (mapped to `8001` in `docker-compose.yml`)

## Story

A small news site renders its articles with `?page=about`, turning your input
into a file it reads and includes. Nothing stops you from asking for a file that
isn't an article.

## Files

- `index.php`, `pages/`, `style.css` — the application source
- `flag.txt` — organizer flag; copied to `/flag.txt` in the image
- `Dockerfile`, `docker-compose.yml` — container build and runner
- `hints.md` — tiered hints
- `writeup.md` — intended solution
- `solve/solve.sh` — reference solver (`./solve/solve.sh http://HOST:8001`)

## Running

```bash
docker compose up -d --build   # serves on http://localhost:8001
```

## Flag format

```text
SecurinetsENIT{...}
```
