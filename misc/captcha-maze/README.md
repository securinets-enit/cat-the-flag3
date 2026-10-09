# 🧀 Captcha: Rats in a Maze

> *"A simple captcha to prove you're not a robot — which, ironically, only a robot can solve."*

**Category:** Misc / Automation | **Difficulty:** ⭐⭐⭐ Hard  
**Author:** MrXFuji | **Points:** 400

---

## Description

To protect our top-secret laboratory against automated scraping, our security team implemented a foolproof CAPTCHA.

All you have to do is navigate through 100 randomly generated 11×11 mazes under a strict 5.0-second deadline per maze. The path tiles are littered with board-game relics: Chess pieces, Dice, Dominoes, Mahjong tiles, and Playing Cards. Each piece adds a specific toll to your passage.

Dijkstra guarantees there is one — and only one — cheapest route through the labyrinth. But can your script perceive the labyrinth through the haze of ANSI escapes and double-width Unicode glyphs before the timer expires?

Clear all 100 rounds, and the Oracle will project the flag into your terminal.

---

## Challenge Specifications

- **Network:** TLS socket with redpwn Proof-of-Work (`https://pwn.red/pow`)
- **Protocol:** 100 consecutive 11×11 weighted mazes
- **Time limit:** 5.0 seconds per maze
- **Move vocabulary:** `U` (Up), `D` (Down), `L` (Left), `R` (Right)
- **Flag Format:** `SecurinetsENIT{...}` (Case-sensitive!)

---

## Files

| File / Folder | Description |
|---|---|
| `src/server.py` | TLS server implementation & game loop |
| `src/maze_gen.py` | 11×11 maze generator with unique Dijkstra path guarantee |
| `src/pieces.py` | Board-game piece definitions & Unicode cost models |
| `src/pow_engine.py` | Pure Python redpwn-compatible VDF Proof-of-Work engine |
| `Dockerfile`, `docker-compose.yml` | Docker deployment (organizers only) |
| `flag.txt` | The flag read by the server (organizers only, never give to players) |
| `solve.py` | Complete educational automated solver |
| `WRITEUP.md` | Step-by-step challenge writeup |
| `CONCEPT_GUIDE.md` | Academic deep dive into Terminal emulation, UAX #11, Dijkstra & PoW |

---

## Deployment

To launch the challenge service locally:

```bash
cd misc/captcha-maze
docker compose up --build -d
```

The TLS service will listen on **port 5000**.

To test with OpenSSL s_client:
```bash
openssl s_client -connect localhost:5000 -quiet
```
