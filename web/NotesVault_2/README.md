# Notes Vault v3 — hard CSPT

Black-box, hard client-side path traversal (CSPT) challenge.

A notes portal validates a fragment-derived note slug with a naive client-side
sanitizer and a backend WAF. The slug is later resolved with the WHATWG `URL`
parser, which silently strips ASCII tab/LF/CR characters — so `.%09.` passes the
sanitizer and becomes `..` inside the parser. Chain it with the page's
attacker-controlled autosave body to make the admin bot change its own password,
then log in and read the flag.

- Difficulty: hard (requires knowing the WHATWG URL parser's control-char
  stripping and how the fragment is decoded by `URLSearchParams`).
- Style: self-contained; includes an admin bot and an egress-locked container, so
  the only way out is the state change.

## Run

```sh
docker compose up --build -d      # serves on http://localhost:3002
```

For local development you also need Chromium for the bot:

```sh
npm install
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser node server.js
```

## Solve

```sh
python3 solve/solve.py http://localhost:3002
# or
./solver.sh http://localhost:3002
```

See `writeup.md` for the full chain and `hints.md` for progressive hints.
