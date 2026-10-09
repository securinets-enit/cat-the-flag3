# Threat Intelligence — Cat the Flag v3

10 challenges in the same format as last year: a Go asker served with socat, 3 attempts per question, and running out of attempts ends the session. Challenges are ordered from easiest to hardest (ports 5010 to 5019 follow that order). See `INDEX.md` for ports, difficulty and sources.

## Deploy & test

    make up                         # build + start all 10 askers (ports 5010-5019)
    make up TASK="zebrocy triton"   # only some tasks
    make ps                         # status
    make test                       # play every task with its answer key, check the flag (HOST=... for a remote box)
    make logs TASK=zebrocy          # logs
    make down                       # stop

## How it's built

```
tools/questions.py     <- the ONLY place to edit questions/answers/sources
tools/engine.go.tmpl   <- shared asker engine
tools/gen.py           <- writes every <name>_asker.go and WALKTHROUGH.md
tools/banner.py        <- the ASCII-art header (title, cat, info box); run it to preview
tools/smoke_test.py    <- `make test`: end-to-end check of every running asker
```

The header's challenge name, difficulty and author come from each `description.md` (`## Title`, `#### Difficulty:`, `**Author:**`), so they always match what players read on the CTF platform.

After changing anything in `tools/questions.py`:

```sh
make gen
make up
nc localhost 5010   # easiest (sea-turtle) ... 5019 hardest (triangulation)
```

Don't hand-edit `*_asker.go` or `WALKTHROUGH.md`; they get overwritten. `description.md` files are hand-written and are copied into each walkthrough.

### Answer matching

Each question accepts a list of answers. Before comparing, the engine:
- ignores case, surrounding spaces and quotes, and trailing `.`/`!`/`/`
- accepts defanged input (`[.]`, `hxxp`)
- ignores `http(s)://` and `www.`

Leading dots are kept, so if both `.iso` and `iso` should work, list both (as `bluenoroff` does).

## Before the event

1. **Re-verify answers.** Every row of each walkthrough's Q&A table says where the answer is. Vendors edit posts: ArcaneDoor's Talos post got a new update on 2025-09-25, and Mandiant's blog has moved domains before.
2. **TRITON's "Saudi Arabia" answer** isn't in any of the challenge's official sources (DOJ only says "a foreign refinery"). It comes from press coverage and the UK government. Keep it or drop it.
3. **Test** with `make up && make test`.

## What changed from the first draft

All of this was checked against the linked reports. Per-challenge details are in each `WALKTHROUGH.md` under "Changes from the first draft".

- **"Name one of…" questions now accept every valid answer.** Before, they accepted one: MoonBounce's Boot Services (named all three, accepted only AllocatePool), Sea Turtle's CVEs (1 of 7), Slingshot's Kenya/Yemen, BlueNoroff's impersonated banks (1 of 13), ArcaneDoor's ASA/FTD.
- **Removed questions whose answers were wrong or unsourced:** ChimayRed (Slingshot; Kaspersky says the router exploit is unknown), the Unit 42 "first spotted" question (Zebrocy; the report says the opposite), and MoonBounce's "Spring 2021" (the report contradicts itself).
- **Fixed a wrong premise.** The BlackEnergy-linked bootkit belongs to Delphocy, not Zebrocy, and ArcaneDoor's CVE-2024-20358 comes from Cisco's event-response page, not from Talos.
- **Removed trivia and copy-paste questions:** TA0011, "Cryptocurrency", "DNS", and blog-post titles.
- **Removed giveaways.** ArcaneDoor no longer says "Lua-based" before asking for the language, and SUNBURST asks about FireEye before the questions that mention FireEye.
- **Fixed links.** The Sea Turtle URL was a 404, BlueNoroff was missing its article ID, and Triangulation's canvas-fingerprint answer lives in an article that wasn't linked.
- **Descriptions:** corrected inaccurate story details and added a reading-list hint so players know how many sources to look for.
- **Ordering:** challenges, ports and the question bank (`ORDER` in `tools/questions.py`) go from easiest to hardest, and each description has a `Difficulty:` line.
- **Engine:** one shared, generated engine instead of 10 hand-copied ones, with multi-answer matching and a clean exit on disconnect.
