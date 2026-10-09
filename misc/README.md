# Misc

| Challenge | Folder | Author | Difficulty | Type | Give players |
|---|---|---|---|---|---|
| seeded_dreams | `seeded-dreams/` | Ahmed Salhi | Easy–medium | File | `seeded-dreams/dist/` |
| Signal Lost | `signal-lost/` | Ahmed Salhi | Medium | File | `signal-lost/dist/` |
| Silent Beacon | `silent-beacon/` | Ahmed Salhi | Medium | File | `silent-beacon/dist/` |
| Don't Whisper | `dont_whisper/` | MrXFuji | Medium | Web service, port 8005 | URL only |
| Captcha: Rats in a Maze | `captcha-maze/` | MrXFuji | Hard | TLS service, port 5000 | Host and port only |
| AZERTY Cat | `azerty-cat/` | r3t0x | Easy (100) | File | `azerty-cat/dist/` |
| Cat Jail v1 | `cat-jail-v1/` | r3t0x | Easy–medium (200) | nc service, port 1337 | Host and port only |
| Cat Jail v2 | `cat-jail-v2/` | r3t0x | Hard (400) | nc service, port 1338 | Host and port only |
| Scattered Kittens | `scattered-kittens/` | r3t0x | Easy (100) | File | `scattered-kittens/dist/` |
| Mimi's Budget | `mimi-budget/` | r3t0x | Easy–medium (150) | File | `mimi-budget/dist/` |
| Meowdle | `meowdle/` | r3t0x | Medium (250) | nc service, port 1339 | `meowdle/dist/words.txt` + host and port |
| Copycat | `copycat/` | r3t0x | Easy (100) | File | `copycat/dist/` |
| Cat Stairs | `cat-stairs/` | r3t0x | Medium (250) | nc service, port 1340 | Host and port only |
| Fish Heist | `fish-heist/` | r3t0x | Medium (250) | nc service, port 1341 | Host and port only |

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

# Cat Jail v1 (nc on 1337)
cd misc/cat-jail-v1 && docker compose up --build -d

# Cat Jail v2 (nc on 1338)
cd misc/cat-jail-v2 && docker compose up --build -d

# Meowdle (nc on 1339)
cd misc/meowdle && docker compose up --build -d

# Cat Stairs (nc on 1340)
cd misc/cat-stairs && docker compose up --build -d

# Fish Heist (nc on 1341)
cd misc/fish-heist && docker compose up --build -d

# Don't Whisper (HTTP on 8005)
cd misc/dont_whisper/src && docker build -t dont-whisper . && docker run -d -p 8005:8005 dont-whisper
```

Captcha: Rats in a Maze reads its flag from `flag.txt` at startup, so the flag
in that file is the one to register in CTFd.
