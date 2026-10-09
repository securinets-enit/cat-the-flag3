## WALKTHROUGH: triangulation

## Zero Clicks, Zero Chances

#### Difficulty: Hard

### Description

While monitoring their own corporate Wi-Fi network, Kaspersky's researchers noticed something odd about their own employees' iPhones. No phishing link was clicked. No app was installed. Nobody did anything wrong.

That is exactly what makes this campaign one of the most technically complex mobile attacks ever documented.

Trace the chain: from the very first invisible message, all the way down to an undocumented feature buried in the phone's own hardware.

**Reading list:** this one is a series. Kaspersky published several Securelist articles about it during 2023, and you'll need four of them. Stopping at the first one won't get you the flag.

Answer the questions by connecting to: nc <PORT> <IP>

**Author:** Taha

### Sources

- **S1**: [Kaspersky - Operation Triangulation: iOS devices targeted with previously unknown malware (Jun 2023)](https://securelist.com/operation-triangulation/109842/)
- **S2**: [Kaspersky - Dissecting TriangleDB, a Triangulation spyware implant (Jun 2023)](https://securelist.com/triangledb-triangulation-implant/110050/)
- **S3**: [Kaspersky - Two more Triangulation pieces: validators and modules (Oct 2023)](https://securelist.com/triangulation-validators-modules/110847/)
- **S4**: [Kaspersky - Operation Triangulation: The last (hardware) mystery (Dec 2023)](https://securelist.com/operation-triangulation-the-last-hardware-mystery/111669/)

### Solution

This challenge spans a series of Securelist articles (all tagged 'Operation Triangulation'). The first article (S1) covers the discovery via KUMA, iMessage delivery, the 2019 start date and the 2023 disclosure. The implant write-up (S2) covers TriangleDB. The validators article (S3) is where the yellow-triangle canvas fingerprint, and therefore the campaign's name, is explained. The 37C3 write-up (S4) lists the full exploit chain with its CVEs and the MMIO hardware feature.

Changes from the first draft: the old walkthrough said KUMA and the canvas fingerprint were in the 'last hardware mystery' article. KUMA is in S1, and the canvas fingerprint is only in S3, which the old challenge never pointed to. The INDEX now lists S3 instead of the 'catching a wild triangle' article, which none of the answers need.

### Questions & Answers

The first answer is canonical; every listed answer is accepted (case-insensitive).

| # | Question | Accepted answers | Where to find it |
|---|---|---|---|
| 1 | What internal Kaspersky monitoring platform first flagged the anomalous traffic on their own corporate Wi-Fi network? (spell out the acronym or give the acronym) | `KUMA` / `Kaspersky Unified Monitoring and Analysis Platform` | S1 - attack overview |
| 2 | What is the name of the core backdoor/implant deployed in this campaign? | `TriangleDB` | S2 |
| 3 | What Apple messaging application delivered the invisible, zero-click initial exploit attachment? | `iMessage` | S1 - attack overview |
| 4 | What CVE number covers the remote code execution vulnerability in Apple's undocumented ADJUST TrueType font instruction? | `CVE-2023-41990` | S4 - attack chain rundown |
| 5 | What web-based fingerprinting technique, which draws a specific shape on the page to uniquely identify victims and gave the whole campaign its name, was used? | `Canvas fingerprinting` / `Canvas` | S3 - 'JavaScript Validator' |
| 6 | Since what year has this campaign reportedly been active, according to Kaspersky's investigation? | `2019` | S1 - 'The oldest traces of infection that we discovered happened in 2019' |
| 7 | In what year was this campaign publicly disclosed by Kaspersky? | `2023` | S1 - dated June 2023 |
| 8 | What 4-letter acronym describes the type of undocumented hardware feature (memory-mapped I/O registers) in Apple's chips that the attackers abused to bypass hardware memory protections? | `MMIO` | S4 - attack chain rundown |
| 9 | What CVE number is the kernel vulnerability used to escalate to root privileges? | `CVE-2023-32434` | S4 - attack chain rundown |

To obtain the flag: `SecurinetsENIT{6effc1105377c8d104817dc5317f859e}`
