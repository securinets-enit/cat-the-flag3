## WALKTHROUGH: slingshot

## Slingshot

#### Difficulty: Easy

### Description

You are a network security analyst for an ISP-adjacent company. During a routine investigation of a suspected keylogger, your team stumbles on a malicious library able to interact with a virtual file system. That is not something an average keylogger does.

The trail leads all the way back to the router sitting at the edge of the network. Someone reached the administrator's computer *through the router itself*.

Kaspersky says this platform rivals Project Sauron and Regin in complexity. Dig into their research and map out how it actually worked.

**Reading list:** one Kaspersky publication answers everything. Read it fully.

Answer the questions by connecting to: nc <PORT> <IP>

**Author:** Taha

### Sources

- **S1**: [Kaspersky - The Slingshot APT FAQ (9 Mar 2018)](https://securelist.com/apt-slingshot/84312/)

### Solution

The description paraphrases the first sentence of Kaspersky's *Slingshot APT FAQ* (S1): suspected keylogger, virtual file system, routers. Every answer is in S1. Players need to separate the infection vector (MikroTik router -> Winbox Loader -> ipv4.dll) from the implant architecture (Cahnadr/Canhadr kernel module + GollumApp).

Changes from the first draft: removed the ChimayRed question. S1 says the router exploitation method 'is not yet clear', so that answer was speculation no source supports. 'Yemen' is now accepted alongside 'Kenya' (S1: 'Kenya and the Yemen account for most of the victims'). The kernel module's alternate spellings are accepted because S1 itself uses both 'Cahnadr' and 'Canhadr' (aka NDriver). The 'Security Analyst Summit' wording was removed from the year question because S1 doesn't mention SAS.

### Questions & Answers

The first answer is canonical; every listed answer is accepted (case-insensitive).

| # | Question | Accepted answers | Where to find it |
|---|---|---|---|
| 1 | Which router manufacturer's devices were abused as the initial infection vector? | `MikroTik` | S1 - intro |
| 2 | What is the name of the malicious DLL planted on the router that acted as a downloader for the rest of the toolset? | `ipv4.dll` | S1 - 'How exactly does infection happen?' |
| 3 | What legitimate MikroTik management software unknowingly downloads and loads this DLL onto the victim's computer? | `Winbox Loader` / `Winbox` / `WinboxLoader` | S1 - 'How exactly does infection happen?' |
| 4 | What is the name of Slingshot's kernel-mode module? | `Cahnadr` / `Canhadr` / `NDriver` | S1 - 'How exactly does infection happen?' (both spellings used) |
| 5 | What is the name of Slingshot's user-mode module, which alone contains nearly 1,500 functions? | `GollumApp` / `Gollum App` | S1 - same section |
| 6 | In what year did Kaspersky publicly reveal the Slingshot campaign? | `2018` | S1 - dated 09 Mar 2018 |
| 7 | Name one of the two African/Middle Eastern countries where most Slingshot victims were found. | `Kenya` / `Yemen` / `the Yemen` | S1 - 'What is the victim profile and target geography?' |
| 8 | According to Kaspersky's analysis, in what year was the very first Slingshot sample detected - years before the campaign was publicly disclosed? | `2012` | S1 - 'When was Slingshot active?' (earliest sample compiled in 2012) |

To obtain the flag: `SecurinetsENIT{fa3a19fe39a6dc6089241abb5cbb275d}`
