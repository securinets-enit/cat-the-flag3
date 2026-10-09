## WALKTHROUGH: sunburst

## The Update That Wasn't

#### Difficulty: Medium

### Description

You're on the incident response team for a government contractor. Your organization runs a popular IT monitoring platform and, like clockwork, applies its vendor's signed software updates.

One of those updates wasn't so innocent. It had already been sitting quietly on your network for months before anyone suspected something was wrong, and the company that first discovered it only found out because *they themselves* got breached.

**Reading list:** the discovering company's original blog post. Read all of it, including any updates added at the top since.

Answer the questions by connecting to: nc <PORT> <IP>

**Author:** Taha

### Sources

- **S1**: [Mandiant/FireEye - Highly Evasive Attacker Leverages SolarWinds Supply Chain to Compromise Multiple Global Victims With SUNBURST Backdoor (13 Dec 2020)](https://cloud.google.com/blog/topics/threat-intelligence/evasive-attacker-leverages-solarwinds-supply-chain-compromises-with-sunburst-backdoor)
- **S2**: [Mandiant - Assembling the Russian Nesting Doll: UNC2452 Merged into APT29 (Apr 2022)](https://cloud.google.com/blog/topics/threat-intelligence/unc2452-merged-into-apt29)

### Solution

IT monitoring platform + signed update + 'the company that discovered it got breached itself' leads to SolarWinds Orion / SUNBURST and FireEye's original post (S1). The UPDATE banner at the very top of S1 says UNC2452 was merged into APT29 (detailed in S2), which is easy to miss if you skip straight to the body.

Changes from the first draft: the FireEye question is now first. In the old order, two earlier questions already said 'FireEye', which gave the answer away. The dormancy question accepts '12-14' and 'two weeks' too, because S1 says 'up to two weeks' and 'at least 12 to 14 days... selected randomly from an interval'.

### Questions & Answers

The first answer is canonical; every listed answer is accepted (case-insensitive).

| # | Question | Accepted answers | Where to find it |
|---|---|---|---|
| 1 | Which cybersecurity company discovered this campaign while investigating the theft of its own internal (red team) tools, disclosed on December 8, 2020? | `FireEye` / `Mandiant` | S1 - authorship / Executive Summary |
| 2 | What is the exact file name of the trojanized SolarWinds Orion DLL that contained the backdoor? | `SolarWinds.Orion.Core.BusinessLayer.dll` | S1 - 'SUNBURST Backdoor' |
| 3 | What did FireEye/Mandiant name this trojanized backdoor? | `SUNBURST` | S1 - Executive Summary |
| 4 | What tracking designator did FireEye initially assign to the threat actor behind this campaign? | `UNC2452` | S1 - Executive Summary |
| 5 | In a May 2022 update to their original blog post, Mandiant merged this tracking designator into which well-known, previously-identified APT group? | `APT29` | S1 - UPDATE (May 2022) banner; S2 |
| 6 | What is the C2 domain used by the backdoor, resolved via a domain generation algorithm? | `avsvmcloud.com` | S1 - 'DGA and Blocklists' |
| 7 | For roughly how many days did the backdoor lie dormant before it would start retrieving and executing commands? | `14` / `12-14` / `12 to 14` / `two weeks` / `2 weeks` | S1 - 'up to two weeks'; 'Initialization' (12 to 14 days) |
| 8 | What is the name of the memory-only second-stage dropper Mandiant documented, used to deploy a Cobalt Strike Beacon? | `TEARDROP` | S1 - 'TEARDROP and BEACON Malware Used' |

To obtain the flag: `SecurinetsENIT{cc0da61c3ae2a3202d1a1afcc126781b}`
