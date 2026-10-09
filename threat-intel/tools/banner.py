"""Builds the ASCII-art header every asker prints on connect (pre-rendered here, so the Go binary has no dependencies)."""

# Title text rendered once with `toilet -f mono9` ("CAT THE" / "FLAG v3"), stored inline so
# regenerating never depends on toilet/figlet being installed.
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


def build(title, difficulty, author):
    out = [""]
    for t, c in zip(TITLE, CAT):
        out.append(f"{BOLD}{RED}{t.ljust(TITLE_W)}{RESET}   {CYAN}{c}{RESET}")

    def row(label, value, color=""):
        text = f"  {label:<11}{value}"
        return f"{GREEN}║{RESET}{text[:2]}{DIM}{text[2:13]}{RESET}{color}{BOLD}{text[13:]}{RESET}{' ' * (WIDTH - len(text))}{GREEN}║{RESET}"

    club = "Securinets ENIT  //  Threat Intelligence"
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
    return "\n".join(out)


if __name__ == "__main__":
    print(build("Hijacking The Internet's Phonebook", "Easy", "Taha"))
