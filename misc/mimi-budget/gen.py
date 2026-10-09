#!/usr/bin/env python3
"""
Mimi's Budget - generator (organizers only, do NOT ship to players).

Builds dist/mimi_budget.xlsx, a normal-looking cat food budget hiding the flag
in three parts:
  1. a cell with the custom number format ';;;' (value invisible in the grid)
  2. a CHAR() formula in a hidden column (text never stored as plain letters)
  3. a 'veryHidden' sheet (not listed in Excel's Unhide menu)

Usage:
    python3 gen.py
Requires: openpyxl
"""
import datetime
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

HERE = os.path.dirname(os.path.abspath(__file__))

PARTS = ["SecurinetsENIT{c4t_f00d_", "1s_n3v3r_", "ch34p}"]

PURCHASES = [
    ("2026-09-01", "Whiskas Tuna", 6, 3.200),
    ("2026-09-03", "Felix Chicken", 4, 2.900),
    ("2026-09-07", "Litter (10 kg)", 1, 18.500),
    ("2026-09-10", "Royal Canin Indoor", 1, 46.000),
    ("2026-09-12", "Catnip toy", 1, 7.500),
    ("2026-09-15", "Whiskas Tuna", 6, 3.200),
    ("2026-09-18", "Sardines (market)", 2, 5.000),
    ("2026-09-21", "Felix Chicken", 4, 2.900),
    ("2026-09-24", "Vet check-up", 1, 40.000),
    ("2026-09-27", "Litter (10 kg)", 1, 18.500),
    ("2026-09-29", "Whiskas Tuna", 6, 3.200),
]

HEADER_FILL = PatternFill("solid", fgColor="2F6B2A")
HEADER_FONT = Font(bold=True, color="FFFFFF")


def header(ws, cols):
    for i, name in enumerate(cols, start=1):
        c = ws.cell(row=1, column=i, value=name)
        c.fill, c.font = HEADER_FILL, HEADER_FONT
        c.alignment = Alignment(horizontal="center")


def main():
    wb = Workbook()

    # ---------- Sheet 1: the budget ----------
    ws = wb.active
    ws.title = "September"
    header(ws, ["Date", "Item", "Qty", "Unit price (TND)", "Total (TND)", "", "", "Notes"])
    for r, (d, item, qty, price) in enumerate(PURCHASES, start=2):
        ws.cell(row=r, column=1, value=datetime.date.fromisoformat(d)).number_format = "dd/mm/yyyy"
        ws.cell(row=r, column=2, value=item)
        ws.cell(row=r, column=3, value=qty)
        ws.cell(row=r, column=4, value=price).number_format = "0.000"
        ws.cell(row=r, column=5, value=f"=C{r}*D{r}").number_format = "0.000"
    last = len(PURCHASES) + 1
    total_row = last + 2
    ws.cell(row=total_row, column=4, value="TOTAL").font = Font(bold=True)
    t = ws.cell(row=total_row, column=5, value=f"=SUM(E2:E{last})")
    t.number_format, t.font = "0.000", Font(bold=True)

    # Part 1: value in plain sight, but ';;;' makes the grid show nothing
    p1 = ws.cell(row=total_row + 3, column=2, value=PARTS[0])
    p1.number_format = ";;;"

    # Part 2: CHAR() formula in a hidden column H
    ws.cell(row=7, column=8, value="=" + "&".join(f"CHAR({ord(c)})" for c in PARTS[1]))
    ws.cell(row=3, column=8, value="ask Mimi")
    ws.column_dimensions["H"].hidden = True

    for col, width in zip("ABCDE", (12, 22, 6, 17, 13)):
        ws.column_dimensions[col].width = width

    # ---------- Sheet 2: a boring summary ----------
    summary = wb.create_sheet("Summary")
    header(summary, ["Category", "Spent (TND)"])
    rows = [("Food", "=SUMIF(September!B2:B{0},\"<>Litter (10 kg)\",September!E2:E{0})-September!E10-September!E6".format(last)),
            ("Litter", "=SUMIF(September!B2:B{0},\"Litter (10 kg)\",September!E2:E{0})".format(last)),
            ("Vet", "=September!E10"),
            ("Toys", "=September!E6")]
    for r, (cat, f) in enumerate(rows, start=2):
        summary.cell(row=r, column=1, value=cat)
        summary.cell(row=r, column=2, value=f).number_format = "0.000"
    summary.column_dimensions["A"].width = 14
    summary.column_dimensions["B"].width = 14

    # ---------- Sheet 3: very hidden ----------
    secret = wb.create_sheet("litter_box")
    secret["A1"] = "Mimi's private stash"
    secret["A3"] = "treats eaten behind the sofa"
    secret["B3"] = 42
    secret["D17"] = PARTS[2]
    secret.sheet_state = "veryHidden"

    wb.active = 0
    wb.calculation.fullCalcOnLoad = True

    out = os.path.join(HERE, "dist", "mimi_budget.xlsx")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    wb.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
