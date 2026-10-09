#!/usr/bin/env python3
"""Regenerate every <challenge>/<name>_asker.go and <challenge>/WALKTHROUGH.md from tools/questions.py."""

import json
import re
from pathlib import Path

import banner
from questions import CHALLENGES

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
TEMPLATE = (TOOLS / "engine.go.tmpl").read_text()


def go_str(s):
    # JSON string literals are valid Go interpreted string literals.
    return json.dumps(s, ensure_ascii=False)


def header(description):
    title = re.search(r"^## (.+)$", description, re.M).group(1).strip()
    difficulty = re.search(r"^#### Difficulty: (.+)$", description, re.M).group(1).strip()
    author = re.search(r"^\*\*Author:\*\* (.+)$", description, re.M).group(1).strip()
    return banner.build(title, difficulty, author)


def render_go(ch, description):
    rows = []
    for text, answers, _ in ch["questions"]:
        rows.append("\t\t{%s, []string{%s}}," % (go_str(text), ", ".join(go_str(a) for a in answers)))
    return TEMPLATE.replace("{{QUESTIONS}}", "\n".join(rows)).replace("{{BANNER}}", go_str(ch["banner"])) \
        .replace("{{HEADER}}", go_str(header(description)))


def render_walkthrough(ch, description):
    out = [f"## WALKTHROUGH: {ch['dir']}", "", description.strip(), "", "### Sources", ""]
    for key, (title, url) in ch["sources"].items():
        out.append(f"- **{key}**: [{title}]({url})")
    out += ["", "### Solution", "", ch["solution"], "", "### Questions & Answers", "",
            "The first answer is canonical; every listed answer is accepted (case-insensitive).", "",
            "| # | Question | Accepted answers | Where to find it |", "|---|---|---|---|"]
    for i, (text, answers, where) in enumerate(ch["questions"], 1):
        cell = lambda s: s.replace("|", "\\|").replace("\n", " ")
        out.append(f"| {i} | {cell(text)} | {cell(' / '.join(f'`{a}`' for a in answers))} | {cell(where)} |")
    flag = (ROOT / ch["dir"] / "flag.txt").read_text().strip()
    out += ["", f"To obtain the flag: `{flag}`", ""]
    return "\n".join(out)


def main():
    for ch in CHALLENGES:
        d = ROOT / ch["dir"]
        description = (d / "description.md").read_text()
        (d / ch["gofile"]).write_text(render_go(ch, description))
        (d / "WALKTHROUGH.md").write_text(render_walkthrough(ch, description))
        print(f"{ch['dir']:<14} {len(ch['questions']):>2} questions")


if __name__ == "__main__":
    main()
