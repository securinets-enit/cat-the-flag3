# Copycat

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Easy
**Points:** 100

## Description

Mimi has an evil twin. They look exactly the same in every photo... almost.

## Files

| File | Who gets it |
|---|---|
| `dist/mimi.png`, `dist/copycat.png` | Players |
| `challenge.yml` | CTFd import (ctfcli) |
| `flag.txt`, `gen.py`, `solve.py` | Organizers only |

## Regenerating

Change the flag in `flag.txt` (and in `challenge.yml`), then:

```bash
pip install pillow
python3 gen.py      # rewrites both images
python3 solve.py    # writes diff.png, which shows the flag
```
