## WALKTHROUGH: moonbounce

## The Implant That Survives A Format

#### Difficulty: Medium

### Description

IT wiped and reinstalled a "compromised" machine from scratch: new disk image, clean OS, the works. A week later, it's still phoning home.

Something on that machine survived a full disk wipe. Something that isn't even stored *on* the disk.

Kaspersky's own Firmware Scanner caught this one. Go find out exactly where it was hiding, and how it got there.

**Reading list:** one Kaspersky Securelist report.

Answer the questions by connecting to: nc <PORT> <IP>

**Author:** Taha

### Sources

- **S1**: [Kaspersky - MoonBounce: the dark side of UEFI firmware (Jan 2022)](https://securelist.com/moonbounce-the-dark-side-of-uefi-firmware/105468/)

### Solution

'Survives a disk wipe' + 'Kaspersky Firmware Scanner' leads to MoonBounce (S1), which answers every question: the implant lives in CORE_DXE on the SPI flash, hooks EFI Boot Services, and injects into svchost.exe once Windows boots.

Changes from the first draft: the Boot Services question listed all three functions and then accepted only AllocatePool. It now lists none and accepts all three. The 'earlier bootkits' question now accepts MosaicRegressor as well as LoJax. Removed the 'Spring 2021' question because S1 contradicts itself ('detected in spring 2021' vs 'made aware... at the end of 2021'), so no answer is unambiguous.

### Questions & Answers

The first answer is canonical; every listed answer is accepted (case-insensitive).

| # | Question | Accepted answers | Where to find it |
|---|---|---|---|
| 1 | What type of firmware does this implant infect (4-letter acronym)? | `UEFI` | S1 - title / 'What happened?' |
| 2 | Name the specific firmware component the implant modifies, which is invoked early in the UEFI boot sequence. | `CORE_DXE` / `CORE DXE` / `DXE Foundation` | S1 - 'Our discovery' |
| 3 | On what physical storage location on the motherboard is the implant actually written? | `SPI flash` / `SPI` / `SPI flash memory` | S1 - 'What happened?' |
| 4 | Which Kaspersky product feature/component first detected this implant's activity? | `Firmware Scanner` / `Kaspersky Firmware Scanner` | S1 - 'What happened?' |
| 5 | Name one of the three EFI Boot Services functions the implant hooks. | `AllocatePool` / `CreateEventEx` / `ExitBootServices` | S1 - 'Our discovery' |
| 6 | Into which legitimate Windows process does the implant inject its user-mode payload during boot? | `svchost.exe` / `svchost` | S1 - 'Our discovery' |
| 7 | This was the third known UEFI firmware implant found in the wild. Name one of the two earlier ones. | `LoJax` / `MosaicRegressor` | S1 - 'Revisiting the current state of the art' |
| 8 | Kaspersky attributed this implant with considerable confidence to which Chinese-speaking threat actor? | `APT41` / `APT 41` | S1 - 'Who is behind the MoonBounce attack?' |

To obtain the flag: `SecurinetsENIT{e6a71bf9c67620bc6d9865cc089d9bc7}`
