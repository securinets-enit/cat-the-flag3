# gh-cli-supply-chain

A five-task chain. A fake GitHub CLI download site, a Mythic C2, and a
sequence of correlated evidence artifacts.

## Overview

A developer visited what looked like a GitHub CLI update page. They
downloaded a tarball, ran its bundled installer, and unknowingly dropped a
Mythic Poseidon beacon that persisted via cron and phoned home over HTTPS.

The chain walks through the entire intrusion lifecycle:

1. Initial contact and download (browser history)
2. Passive reconnaissance of the delivery domain
3. Installer code review
4. Binary and host telemetry analysis
5. Network traffic analysis of the beacon

## Tasks

| # | Name | Category | Difficulty | Port | Flag |
|---|---|---|---|---|---|
| 1 | The Bait | Browser Forensics | Easy | — | SecurinetsENIT{aa24756f4410809ecc650d58404ee1f7} |
| 2 | The Recon | Domain Intelligence | Medium | 9999 | SecurinetsENIT{9b6d946fc44eb755d906b366c7c794f1} |
| 3 | The Dropper | Malware Analysis | Medium | 9998 | SecurinetsENIT{75efb0959defbc4b1bdcc6247381b437} |
| 4 | The Implant | Binary + Network Forensics | Hard | 9997 | SecurinetsENIT{5398f82818903750fc0d72e94c5f3304} |
| 5 | The Beacon | Network Forensics | Hard | 9996 | SecurinetsENIT{4b094f5e62c3ca3257c2571d8ab1d059} |

## Handout

Evidence is served from the fake site at cdnjs-mirror.net/evidence/.
Each task's writeup lists exactly which files are needed.

Task 2, 3, 4, and 5 interact via a TCP asker:

    nc <ctf-host> 9999   # Task 2
    nc <ctf-host> 9998   # Task 3
    nc <ctf-host> 9997   # Task 4
    nc <ctf-host> 9996   # Task 5

## Domains in play

| Domain | Purpose |
|---|---|
| cdnjs-mirror.net | Fake GitHub CLI download site |
| gh-actions-runner.xyz | Mythic C2 |

## Skills taught

- Browser forensics with SQLite
- Passive domain intelligence (WHOIS, DNS, TLS)
- Static analysis of shell installers
- Binary and host telemetry correlation
- Network forensics on packet captures
- MITRE ATT&CK mapping

## Flag format

SecurinetsENIT{...}
