## WALKTHROUGH: zebrocy

## A Zebra In Sheep's Clothing

#### Difficulty: Easy

### Description

Your organization, a diplomatic mission in Central Asia, keeps receiving spearphishing emails: fake embassy notes, invitation letters, archives with documents that aren't really documents. The volume is unusually high for a targeted attacker. Each time your team catches a sample, it is written in a different programming language than the last one. Delphi. Then AutoIt. Then something new.

Kaspersky has been tracking this exact pattern for years, as a distinctive subset of a much bigger and much more famous APT group.

Figure out who's really behind the zebra stripes.

**Reading list:** two Kaspersky Securelist posts from 2019.

Answer the questions by connecting to: nc <PORT> <IP>

**Author:** Taha

### Sources

- **S1**: [Kaspersky GReAT - A Zebrocy Go Downloader (Jan 2019)](https://securelist.com/a-zebrocy-go-downloader/89419/)
- **S2**: [Kaspersky GReAT - Zebrocy's Multilanguage Malware Salad (Jun 2019)](https://securelist.com/zebrocys-multilanguage-malware-salad/90680/)

### Solution

Searching Kaspersky + Delphi/AutoIt malware + diplomatic targets leads to Zebrocy. Two Securelist posts carry the challenge: the Go downloader post (S1), which also states where 'Masha and these Bears' was presented (SAS2018, Cancun), and the 'Multilanguage Malware Salad' (S2) for the lineage questions.

Changes from the first draft:
- Removed the Unit 42 question. Its premise was backwards: S1 does not credit Unit 42 with first spotting the Go variant. It says Unit 42 dated its first detection to 2018-10-11, while Kaspersky had already documented the same downloader with a first deployment on 2018-05-10.
- Fixed the BlackEnergy question. The bootkit that shares kernel code with BlackEnergy belongs to *Delphocy* (S2), not to Zebrocy.
- Removed 'what is the title of the report' (it tests copy-paste, not reading).
- The managed-language question now accepts every language S2 lists (Python, C#, Go).

### Questions & Answers

The first answer is canonical; every listed answer is accepted (case-insensitive).

| # | Question | Accepted answers | Where to find it |
|---|---|---|---|
| 1 | Zebrocy is described as a sub-cluster/subgroup of which larger, well-known Russian-speaking APT actor? | `Sofacy` / `APT28` / `Fancy Bear` | S1 - 'Attribution' ('a known subset of Sofacy activity') |
| 2 | In what year was Zebrocy first introduced as a Sofacy backdoor package? | `2015` | S1 - first paragraph |
| 3 | Kaspersky first publicly discussed Zebrocy at their Security Analyst Summit, in a talk titled 'Masha and these Bears'. In which city was that summit held? | `Cancun` / `Cancún` | S1 - first paragraph ('SAS2018 in Cancun, Mexico') |
| 4 | Name the earlier Delphi-based malware family (active 2013-2015) that shares lineage and code artifacts with Zebrocy's own Delphi backdoor. | `Delphocy` | S2 - 'Zebrocy Delphi backdoor shared artefacts rooted in Delphocy and BlackEnergy' |
| 5 | Delphocy's bootkit loader shares unique kernel code with which other well-known malware family? | `BlackEnergy` / `Black Energy` | S2 - same section |
| 6 | Besides Delphi and AutoIt, name one of the newer 'managed' programming languages Zebrocy expanded into. | `Go` / `Golang` / `C#` / `CSharp` / `C Sharp` / `Python` | S2 - 'new managed languages like Python, C#, and Go' |

To obtain the flag: `SecurinetsENIT{3a0f2c78ce068ab34590a0f8a05f26cd}`
