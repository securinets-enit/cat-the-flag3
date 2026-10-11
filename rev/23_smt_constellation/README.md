# SMT Constellation

**Category:** Reverse engineering  
**Difficulty:** Hard  
**Technique:** Bit-vector constraints and SMT solving

Players receive `attachments/checker.py`, a checker whose `check` function
contains independent arithmetic and bit-vector constraints. The intended
solution is to translate those constraints into Z3 rather than brute-force a
36-byte flag.

Offline only. Python 3.8+ is required; players may install `z3-solver`.
