# Scattered Kittens

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Easy
**Points:** 100

## Description

Mimi had nine kittens and they never sit still.
They ran across my screen so fast I couldn't even count them.

## Files

| File | Who gets it |
|---|---|
| `dist/kittens.gif` | Players |
| `challenge.yml` | CTFd import (ctfcli) |
| `flag.txt`, `gen.py`, `solve.py` | Organizers only |

## Regenerating

Change the flag in `flag.txt` (and in `challenge.yml`), then:

```bash
pip install opencv-python pillow
python3 gen.py      # rewrites dist/kittens.gif
python3 solve.py    # checks it decodes back to the flag
```
