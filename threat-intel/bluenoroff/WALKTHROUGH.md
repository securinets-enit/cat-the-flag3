## WALKTHROUGH: bluenoroff

## Snatch and Grab

#### Difficulty: Medium

### Description

You are brought in to investigate a crypto startup whose hot wallet was drained days after receiving a "partnership deck" from a supposed investor. The file didn't trigger the usual "downloaded from the internet, are you sure?" warning that Windows normally shows. It just opened.

Kaspersky has been tracking the crew behind this for years: a financially motivated unit of a much larger, much more infamous nation-state group, one that started out robbing banks.

**Reading list:** two Kaspersky reports from 2022 (one from January, one from December), plus MITRE ATT&CK for the other names this group goes by.

Answer the questions by connecting to: nc <PORT> <IP>

**Author:** Taha

### Sources

- **S1**: [Kaspersky - BlueNoroff introduces new methods bypassing MoTW (Dec 2022)](https://securelist.com/bluenoroff-methods-bypass-motw/108383/)
- **S2**: [Kaspersky - The BlueNoroff cryptocurrency hunt is still on (Jan 2022)](https://securelist.com/the-bluenoroff-cryptocurrency-hunt-is-still-on/105488/)
- **S3**: [MITRE ATT&CK - APT38 (G0082)](https://attack.mitre.org/groups/G0082/)

### Solution

The description's 'no downloaded-from-the-internet warning' points to the December 2022 report on Mark-of-the-Web bypasses (S1). The group's background (Lazarus link, Bangladesh Bank origin) is in the intro of the January 2022 SnatchCrypto report (S2), which also tells the 'drained wallet' story from the description. MITRE (S3) maps BlueNoroff to APT38 and its other vendor names.

Changes from the first draft: the 'name one impersonated institution' question now accepts every company in S1's lookalike-domain table instead of only Mitsubishi UFJ. The disk-image question accepts both formats with or without the dot. The alias question accepts every associated group MITRE lists.

### Questions & Answers

The first answer is canonical; every listed answer is accepted (case-insensitive).

| # | Question | Accepted answers | Where to find it |
|---|---|---|---|
| 1 | BlueNoroff is described by Kaspersky as a sub-cluster of which larger threat actor? | `Lazarus` / `Lazarus Group` | S2 - intro ('a unit within a larger formation of Lazarus attackers') |
| 2 | BlueNoroff is also tracked under another name by other vendors - name it. | `APT38` / `Stardust Chollima` / `Nickel Gladstone` / `BeagleBoyz` / `Sapphire Sleet` / `COPERNICIUM` | S3 - Associated Groups |
| 3 | What Windows security feature (usually referred to by a 4-letter abbreviation) did BlueNoroff's new late-2022 delivery techniques bypass? | `MOTW` / `Mark-of-the-Web` / `Mark of the Web` | S1 - intro |
| 4 | Name one of the two container/disk-image file formats BlueNoroff adopted to evade this protection. | `ISO` / `.ISO` / `VHD` / `.VHD` | S1 - intro ('.iso' and '.vhd') |
| 5 | BlueNoroff's fake domains mostly impersonated venture capital companies and banks located in which country? | `Japan` | S1 - intro / 'Infrastructure' |
| 6 | Historically, BlueNoroff has been linked to a major cyber-heist against a national bank conducted via the SWIFT network. Which bank? | `Bangladesh Bank` / `Bangladesh Central Bank` / `Central Bank of Bangladesh` / `Bank of Bangladesh` | S2 - intro; S3 |
| 7 | Name one legitimate financial institution whose name/branding BlueNoroff's fake domains impersonated. | `Mitsubishi UFJ Financial Group` / `MUFG` / `Sumitomo Mitsui Banking Corporation` / `SMBC` / `Mizuho Financial Group` / `Mizuho` / `Bank of America` / `Beyond Next Ventures` / `ANOBAKA` / `Z Venture Capital` / `ABF Capital` / `Angel Bridge` / `Trans-Pacific Technology Fund` | S1 - 'Infrastructure' table (Genuine company column) |

To obtain the flag: `SecurinetsENIT{e2509077d2fc0be3f908e671e89f5f34}`
