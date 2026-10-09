# Mimi's Budget

**Category:** Misc
**Author:** r3t0x (Ghaith Amdouni)
**Difficulty:** Easy–medium
**Points:** 150

## Description

Mimi's owner tracks every coin she spends on cat food.
Mimi says the spreadsheet is boring. Mimi is lying.

## Files

| File | Who gets it |
|---|---|
| `dist/mimi_budget.xlsx` | Players |
| `challenge.yml` | CTFd import (ctfcli) |
| `flag.txt`, `gen.py`, `solve.py` | Organizers only |

## Regenerating

Change the three parts in `gen.py` (`PARTS`), the flag in `flag.txt` and in
`challenge.yml`, then:

```bash
pip install openpyxl
python3 gen.py      # rewrites dist/mimi_budget.xlsx
python3 solve.py    # checks it assembles back to the flag
```
