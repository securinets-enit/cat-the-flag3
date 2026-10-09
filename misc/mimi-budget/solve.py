#!/usr/bin/env python3
"""
Mimi's Budget - solver (organizers only, do NOT ship to players).

Reads every cell of every sheet (hidden, very hidden, ';;;'-formatted),
evaluates CHAR() formulas, and assembles the flag.

Usage:
    python3 solve.py [dist/mimi_budget.xlsx]
Requires: openpyxl
"""
import os
import re
import sys

import openpyxl

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist", "mimi_budget.xlsx")
wb = openpyxl.load_workbook(path)

found = []
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, str) and v.startswith("=") and "CHAR(" in v:
                v = "".join(chr(int(n)) for n in re.findall(r"CHAR\((\d+)\)", v))
            if isinstance(v, str):
                why = []
                if c.number_format == ";;;":
                    why.append("format ;;;")
                if ws.column_dimensions[c.column_letter].hidden:
                    why.append("hidden column")
                if ws.sheet_state != "visible":
                    why.append(f"sheet {ws.sheet_state}")
                if why:
                    print(f"[{ws.title}!{c.coordinate}] ({', '.join(why)}) {v}")
                    found.append(v)

parts = [p for p in found if re.fullmatch(r"[\w{}]+", p) and re.search(r"[_{}]", p)]
start = next(p for p in parts if p.startswith("SecurinetsENIT{"))
end = next(p for p in parts if p.endswith("}"))
middle = [p for p in parts if p not in (start, end)]
print("FLAG:", start + "".join(middle) + end)
