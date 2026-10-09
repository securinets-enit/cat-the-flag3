#!/usr/bin/env python3
"""
Adds the Cat the Flag v3 ASCII-art header (and a boxed flag) to every DFIR asker.

Only touches presentation: the questions and quiz logic in each asker.go stay as they are.
Safe to re-run: the generated block between the BEGIN/END markers is replaced each time.

    python3 tools/banner.py            # update all askers listed in CHALLENGES
    python3 tools/banner.py --preview  # print one header to the terminal

To add a new asker, add a line to CHALLENGES and re-run.
"""

import json
import re
import sys
from pathlib import Path

DFIR = Path(__file__).resolve().parent.parent

# path to asker dir, challenge name, difficulty, author, series
CHALLENGES = [
    ("mreya/02-the-recon/asker", "The Recon", "Medium", "Taha", "Mreya"),
    ("mreya/03-the-dropper/asker", "The Dropper", "Medium", "Taha", "Mreya"),
    ("mreya/04-the-implant/asker", "The Implant", "Hard", "Taha", "Mreya"),
    ("mreya/05-the-beacon/asker", "The Beacon", "Hard", "Taha", "Mreya"),
    ("cloud/01-cloudtrail/asker", "Leaked AWS Key", "Medium", "Taha", "Cloud"),
    ("cloud/02-ssrf/asker", "SSRF to IMDS", "Medium", "Taha", "Cloud"),
]

# "CAT THE" / "FLAG v3", rendered once with `toilet -f mono9` and stored inline.
TITLE = [
    "   ▄▄▄    ▄▄  ▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄ ▄    ▄ ▄▄▄▄▄▄",
    " ▄▀   ▀   ██     █             █    █    █ █",
    " █       █  █    █             █    █▄▄▄▄█ █▄▄▄▄▄",
    " █       █▄▄█    █             █    █    █ █",
    "  ▀▄▄▄▀ █    █   █             █    █    █ █▄▄▄▄▄",
    " ▄▄▄▄▄▄ ▄        ▄▄     ▄▄▄                 ▄▄▄▄",
    " █      █        ██   ▄▀   ▀        ▄   ▄  ▀   ▀█",
    " █▄▄▄▄▄ █       █  █  █   ▄▄        ▀▄ ▄▀    ▄▄▄▀",
    " █      █       █▄▄█  █    █         █▄█       ▀█",
    " █      █▄▄▄▄▄ █    █  ▀▄▄▄▀          █    ▀▄▄▄█▀",
]

# A cat planting the club's flag. Same height as TITLE.
CAT = [
    '  |~~~~~~~~~|',
    '  |  ENIT   |',
    '  |~~~~~~~~~|',
    '  |',
    '  |   /\\_/\\',
    '  |__( o.o )',
    '  |    > ^ <',
    '  |   /     \\',
    '  |  (_|   |_)',
    '~~^~~~~~~~~~~~~~',
]

RESET, BOLD, DIM = "\x1b[0m", "\x1b[1m", "\x1b[2m"
RED, GREEN, YELLOW, CYAN, MAGENTA = "\x1b[31m", "\x1b[32m", "\x1b[33m", "\x1b[36m", "\x1b[35m"
DIFF_COLOR = {"Easy": GREEN, "Medium": YELLOW, "Hard": RED}

TITLE_W = max(len(l) for l in TITLE)
WIDTH = 72  # inner width of the info box; whole banner stays under 80 columns


def build(title, difficulty, author, series):
    out = [""]
    for t, c in zip(TITLE, CAT):
        out.append(f"{BOLD}{RED}{t.ljust(TITLE_W)}{RESET}   {CYAN}{c}{RESET}")

    def row(label, value, color=""):
        text = f"  {label:<11}{value}"
        return f"{GREEN}║{RESET}{text[:2]}{DIM}{text[2:13]}{RESET}{color}{BOLD}{text[13:]}{RESET}{' ' * (WIDTH - len(text))}{GREEN}║{RESET}"

    club = f"Securinets ENIT  //  DFIR  //  {series}"
    out += [
        "",
        f"{GREEN}╔{'═' * WIDTH}╗{RESET}",
        f"{GREEN}║{RESET}{MAGENTA}{BOLD}{club.center(WIDTH)}{RESET}{GREEN}║{RESET}",
        f"{GREEN}╠{'═' * WIDTH}╣{RESET}",
        row("Challenge", title, YELLOW),
        row("Difficulty", difficulty, DIFF_COLOR.get(difficulty, "")),
        row("Author", author, CYAN),
        f"{GREEN}╚{'═' * WIDTH}╝{RESET}",
        "",
    ]
    return "\n".join(out) + "\n"


BEGIN = "// --- BEGIN GENERATED BANNER (tools/banner.py) ---"
END = "// --- END GENERATED BANNER ---"

GO_BLOCK = BEGIN + '''

const bannerHeader = {header}

// printFlag shows the flag inside a box matching the header's style.
func printFlag(flag string) {{
	const green, yellow, bold, reset = "\\x1b[32m", "\\x1b[33m", "\\x1b[1m", "\\x1b[0m"
	inner := len([]rune(flag)) + 6
	label := " Here is your flag "
	fill := inner - 2 - len(label)
	if fill < 0 {{
		fill = 0
	}}
	fmt.Println()
	fmt.Println(green + "╔══" + label + strings.Repeat("═", fill) + "╗" + reset)
	fmt.Println(green + "║" + reset + "   " + yellow + bold + flag + reset + "   " + green + "║" + reset)
	fmt.Println(green + "╚" + strings.Repeat("═", inner) + "╝" + reset)
	fmt.Println("   Securinets ENIT // Cat the Flag v3")
}}

''' + END

PRINT_HEADER = "\tfmt.Print(bannerHeader)\n"
OLD_FLAG = '\tfmt.Println("\\nHere is your flag:")\n\tfmt.Println(string(flagContent))\n'
NEW_FLAG = "\tprintFlag(strings.TrimSpace(string(flagContent)))\n"


def inject(src, header):
    block = GO_BLOCK.format(header=json.dumps(header, ensure_ascii=False))
    if BEGIN in src:
        src = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda _: block, src, flags=re.S)
    else:
        src = src.rstrip("\n") + "\n\n" + block + "\n"
    if PRINT_HEADER not in src:
        # print the header right before the asker's first greeting line
        i = src.index('\tfmt.Println("Hello future')
        src = src[:i] + PRINT_HEADER + src[i:]
    if OLD_FLAG in src:
        src = src.replace(OLD_FLAG, NEW_FLAG)
    elif NEW_FLAG not in src:
        raise SystemExit("could not find the flag-printing lines")
    return src


def main():
    if "--preview" in sys.argv:
        print(build(*CHALLENGES[0][1:]), end="")
        return
    for path, *info in CHALLENGES:
        f = DFIR / path / "asker.go"
        f.write_text(inject(f.read_text(), build(*info)))
        print(f"updated {f.relative_to(DFIR)}")


if __name__ == "__main__":
    main()
