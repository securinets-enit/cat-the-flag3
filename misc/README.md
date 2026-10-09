# Misc

| Challenge | Folder | Author | Difficulty | Type | Give players |
|---|---|---|---|---|---|
| seeded_dreams | `seeded-dreams/` | Ahmed Salhi | Easy–medium | File | `seeded-dreams/dist/` |
| Signal Lost | `signal-lost/` | Ahmed Salhi | Medium | File | `signal-lost/dist/` |
| Silent Beacon | `silent-beacon/` | Ahmed Salhi | Medium | File | `silent-beacon/dist/` |
| Don't Whisper | `dont_whisper/` | MrXFuji | Medium | Web service, port 8005 | URL only |
| Captcha: Rats in a Maze | `captcha-maze/` | MrXFuji | Hard | TLS service, port 5000 | Host and port only |

Flag format: `SecurinetsENIT{...}`

## Rules for player files

- Upload **only** the contents of each challenge's `dist/` folder to CTFd.
- Never upload `flag.txt`, `flag`, `writeup.md`, `solve.py`, `solver.py`,
  `gen.py`, `generate_*` or `src/` folders. They contain the flag or the
  solution.

## Deploying the services

```bash
# Captcha: Rats in a Maze (TLS on 5000)
cd misc/captcha-maze && docker compose up --build -d

# Don't Whisper (HTTP on 8005)
cd misc/dont_whisper/src && docker build -t dont-whisper . && docker run -d -p 8005:8005 dont-whisper
```

Captcha: Rats in a Maze reads its flag from `flag.txt` at startup, so the flag
in that file is the one to register in CTFd.
