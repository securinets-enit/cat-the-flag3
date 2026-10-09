## WALKTHROUGH: arcanedoor

## When The Firewall Vendor Gets Hacked

#### Difficulty: Medium

### Description

In early 2024, a customer reports strange behavior on their perimeter firewall appliance. The vendor's own security teams investigate and discover a state-sponsored espionage campaign quietly living inside their flagship security product, on government networks around the world.

Yes, the firewalls got hacked too.

**Reading list:** the vendor's threat-intelligence blog post, plus the vendor's own security event-response page for this campaign.

Answer the questions by connecting to: nc <PORT> <IP>

**Author:** Taha

### Sources

- **S1**: [Cisco Talos - ArcaneDoor: New espionage-focused campaign found targeting perimeter network devices (Apr 2024, updated Sep 2025)](https://blog.talosintelligence.com/arcanedoor-new-espionage-focused-campaign-found-targeting-perimeter-network-devices/)
- **S2**: [Cisco PSIRT - Event Response: Attacks Against Cisco Firewall Platforms](https://sec.cloudapps.cisco.com/security/center/resources/asa_ftd_attacks_event_response)

### Solution

Talos's ArcaneDoor post (S1) covers the actor names, both implants and the two CVEs that were used: CVE-2024-20353 (DoS used to force a reboot) and CVE-2024-20359 (persistent local code execution that loads Line Runner). The third CVE in the last question is *not* in the Talos post. It comes from Cisco's PSIRT event-response page (S2), which lists three advisories and says only 20353 and 20359 were used, so players have to check the vendor advisory page as well as the blog.

Changes from the first draft: the Line Runner question no longer says 'Lua-based', which gave away a later answer. The last question no longer claims Talos identified the third CVE. The product question accepts FTD too (S2: ASA and Firepower Threat Defense).

Re-verify before the event: S1 got an update on 2025-09-25 about new activity by the same actor (CVE-2025-20333, CVE-2025-20362, CVE-2025-20363). None of the current answers changed.

### Questions & Answers

The first answer is canonical; every listed answer is accepted (case-insensitive).

| # | Question | Accepted answers | Where to find it |
|---|---|---|---|
| 1 | What tracking designator did Cisco Talos assign to the threat actor behind this campaign? | `UAT4356` / `UAT-4356` | S1 - intro |
| 2 | What tracking designator did Microsoft Threat Intelligence Center assign to this same actor? | `STORM-1849` / `Storm 1849` | S1 - intro |
| 3 | Name one of the two Cisco product lines targeted in this campaign (give the abbreviation). | `ASA` / `FTD` | S1; S2 ('Cisco ASA ... or Cisco Firepower Threat Defense (FTD)') |
| 4 | What is the name of the memory-resident, in-memory shellcode-interpreter backdoor used by the actor? | `Line Dancer` / `LineDancer` | S1 - 'Line Dancer: In-Memory Implant Technical Details' |
| 5 | What is the name of the persistent backdoor that survives reboots and software upgrades? | `Line Runner` / `LineRunner` | S1 - 'Line Runner: Persistence Mechanism' |
| 6 | What CVE number is the denial-of-service vulnerability the actor abused to force a device reboot and trigger the persistent backdoor's installation? | `CVE-2024-20353` | S1 - 'Line Runner: Persistence Mechanism' |
| 7 | What CVE number covers the persistent local code execution flaw abused to install the persistent backdoor? | `CVE-2024-20359` | S1 - same section |
| 8 | The persistent backdoor abuses a legacy capability on the ASA originally meant for pre-loading what type of client software? | `VPN clients` / `VPN client` / `VPN` / `VPN clients and plugins` | S1 - same section |
| 9 | What scripting language does the persistent backdoor's malicious payload get written to and executed in? | `Lua` | S1 - same section (csco_config.lua, 'HTTP-based Lua backdoor') |
| 10 | Cisco's ArcaneDoor event-response page lists a third, related vulnerability that was NOT actually used in this specific campaign. What is its CVE number? | `CVE-2024-20358` | S2 - advisory table (only 20353 and 20359 'were used') |

To obtain the flag: `SecurinetsENIT{11af880ae7158baf603e08d682a977b1}`
