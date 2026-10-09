## WALKTHROUGH: applejeus

## AppleJeus

#### Difficulty: Hard

### Description

You work incident response for a cryptocurrency exchange. An employee installed what looked like a perfectly legitimate all-in-one trading application from a vendor's professional-looking website, complete with a valid code-signing certificate and a registered domain. Weeks later, your SOC starts seeing strange outbound connections from that employee's workstation.

Kaspersky's GReAT team has seen this exact playbook before, and it has a name. Your job: identify the operation, the fake company behind it, the malware it dropped, and the threat actor pulling the strings.

**Reading list:** the original vendor report, its sequel published about a year and a half later, and one government advisory. MITRE ATT&CK will help too.

Answer the questions by connecting to: nc <PORT> <IP>

**Author:** Taha

### Sources

- **S1**: [Kaspersky GReAT - Operation AppleJeus (Aug 2018)](https://securelist.com/operation-applejeus/87553/)
- **S2**: [Kaspersky GReAT - Operation AppleJeus Sequel (Jan 2020)](https://securelist.com/operation-applejeus-sequel/95596/)
- **S3**: [US-CERT/CISA - HIDDEN COBRA: FALLCHILL (TA17-318A, Nov 2017)](https://www.cisa.gov/news-events/cybersecurity-advisories/aa17-318a)
- **S4**: [MITRE ATT&CK - Lazarus Group (G0032)](https://attack.mitre.org/groups/G0032/)

### Solution

The description (crypto exchange, trojanized all-in-one trading app, valid signature, Kaspersky GReAT) leads to *Operation AppleJeus* on Securelist (S1). S1 answers most questions. It mentions US-CERT's reporting on Fallchill, which leads to the government alert (S3). The Telegram question requires the 2020 follow-up (S2), because APT reporting is often a series, not a single article.

Changes from the first draft: removed 'TA0011 = Command and Control' (generic ATT&CK trivia, not about this operation) and 'what was the goal: Cryptocurrency' (answerable from the description alone). Added the alternate spellings the reports themselves use.

### Questions & Answers

The first answer is canonical; every listed answer is accepted (case-insensitive).

| # | Question | Accepted answers | Where to find it |
|---|---|---|---|
| 1 | Kaspersky published a report on this operation. What is the full link to that report? | `https://securelist.com/operation-applejeus/87553/` | S1 URL (scheme, www and trailing slash optional) |
| 2 | What name did Kaspersky give to this operation? (without the word 'Operation') | `AppleJeus` | S1 - title |
| 3 | Which APT group is behind this operation? (one word) | `Lazarus` | S1 - title / Overview |
| 4 | What country is this APT group believed to originate from? | `North Korea` / `DPRK` / `Democratic People's Republic of Korea` | S4 (S1 does not name the country) |
| 5 | What is the name of the fake company that distributed the trojanized cryptocurrency trading application? | `Celas Limited` / `Celas LLC` / `Celas` | S1 - 'Celas Trade Pro from Celas Limited' / 'Celas LLC' |
| 6 | What was the name of the trojanized all-in-one trading application itself? | `Celas Trade Pro` / `CelasTradePro` | S1 - 'Trojanized trading application for Windows' |
| 7 | What previously-known Lazarus malware family was delivered as the final payload? | `Fallchill` | S1 - Overview / 'Fallchill backdoor loader' |
| 8 | In what year did Kaspersky first publish its report on Operation AppleJeus? | `2018` | S1 - dated 23 Aug 2018 |
| 9 | Which other security agency published about Fallchill? (format: XX-XXXX) | `US-CERT` | S1 - 'including one from US-CERT'; S3 |
| 10 | In what year did that agency publish its report on Fallchill? | `2017` | S3 - November 2017 |
| 11 | This was the first time Kaspersky observed Lazarus distributing malware for which operating system? | `macOS` / `mac os` / `OS X` / `osx` | S1 - Overview |
| 12 | What is the MITRE ATT&CK Group ID assigned to Lazarus Group? | `G0032` | S4 |
| 13 | In the 2019/2020 'sequel' AppleJeus operation, what messaging app did Lazarus start abusing as a delivery vector? | `Telegram` | S2 - 'Windows version of UnionCryptoTrader' |
| 14 | On the Windows side, what file name did the FallChill-delivering payload use inside C:\Recovery\ ? | `msn.exe` | S1 - 'Downloaded payload' (Known file name: C:\Recovery\msn.exe) |

To obtain the flag: `SecurinetsENIT{88f163c4f0458a42d82f91dc6e39553f}`
