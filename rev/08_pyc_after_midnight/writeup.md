# PYC After Midnight

**Difficulty:** intermediate  
**Artifact:** Python source suitable for bytecode compilation  
**Concept:** Disassemble and debug compiled Python.

## Tools

Use: **Python 3, `dis`, `py_compile`, and a Python debugger**

## Exact solve path

```sh
python3 -m dis attachments/challenge.py
python3 -m py_compile attachments/challenge.py
python3 solver/solve.py
```

Inspect `reveal()` in the disassembly, then run the solver. It replays the
task-specific bytecode logic and prints
`SecurinetsENIT{midnight_bytecode_is_still_code}`.

Do not brute-force the flag. The intended solution is to observe one runtime
value or repair one file-format invariant, then reproduce the operation.

## Flag

```text
SecurinetsENIT{midnight_bytecode_is_still_code}
```
