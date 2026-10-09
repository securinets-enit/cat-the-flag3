# AZERTY Cat

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Easy
**Points:** 100

## Description

My friend left her PC on and her cat Mimi took a walk across the keyboard.
Mimi didn't type much, but she managed to switch the keyboard layout to English.

My friend didn't notice and typed me the flag by hand anyway. All I got is this.

## Files

| File | Who gets it |
|---|---|
| `dist/message.txt` | Players |
| `challenge.yml` | CTFd import (ctfcli) |
| `flag.txt`, `gen.py`, `solve.py` | Organizers only |

## Regenerating

Change the flag in `flag.txt` (and in `challenge.yml`), then:

```bash
python3 gen.py      # rewrites dist/message.txt
python3 solve.py    # checks it decodes back to the flag
```
