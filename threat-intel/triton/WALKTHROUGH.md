## WALKTHROUGH: triton

## Not Just Data, Safety Systems

#### Difficulty: Hard

### Description

You work SOC for a petrochemical plant. Your Safety Instrumented Systems, the ones whose entire job is to physically shut things down before something catastrophic happens, start behaving strangely.

This isn't a ransomware note or a stolen customer database. Someone wanted access to the systems that exist specifically to prevent physical disaster.

The first report on this attack didn't name anyone. It took years, several reports and a courtroom to find out who was behind it.

**Reading list:** the original 2017 incident report, the same vendor's 2018 attribution follow-up, MITRE ATT&CK, and a 2022 US Department of Justice press release.

Answer the questions by connecting to: nc <PORT> <IP>

**Author:** Taha

### Sources

- **S1**: [Mandiant/FireEye - Attackers Deploy New ICS Attack Framework 'TRITON' (14 Dec 2017)](https://cloud.google.com/blog/topics/threat-intelligence/attackers-deploy-new-ics-attack-framework-triton)
- **S2**: [Mandiant/FireEye - TRITON Attribution: Russian Government-Owned Lab Most Likely Built Custom Intrusion Tools (Oct 2018)](https://cloud.google.com/blog/topics/threat-intelligence/triton-attribution-russian-government-owned-lab-most-likely-built-tools)
- **S3**: [MITRE ATT&CK - Triton (S1009) and TEMP.Veles (G0088)](https://attack.mitre.org/software/S1009/)
- **S4**: [US DOJ - Four Russian Government Employees Charged in Two Historical Hacking Campaigns Targeting Critical Infrastructure (Mar 2022)](https://www.justice.gov/archives/opa/pr/four-russian-government-employees-charged-two-historical-hacking-campaigns-targeting-critical)

### Solution

This challenge is about how attribution evolves. Mandiant's original December 2017 report (S1) describes the malware, the target (Schneider Electric Triconex SIS), the TriStation protocol and the intrusion via an SIS engineering workstation, but it does *not* attribute the attack to anyone. In October 2018 Mandiant named the activity TEMP.Veles and tied it to a Russian government-owned institute (S2). MITRE (S3) lists the other names (TRISIS, HatMan) and Dragos's XENOTIME. The 2022 DOJ release (S4) names the indicted programmer, Gladkikh.

Author note: no primary source (Mandiant, MITRE, DOJ) names the victim country. DOJ only says 'a foreign refinery'. 'Saudi Arabia' comes from widespread press coverage and the UK government statement, so players will find it, but it is the one answer here not backed by a vendor/government report.

### Questions & Answers

The first answer is canonical; every listed answer is accepted (case-insensitive).

| # | Question | Accepted answers | Where to find it |
|---|---|---|---|
| 1 | Which vendor's Safety Instrumented System (SIS) did this malware specifically target? | `Schneider Electric` / `Schneider` | S1; S4 |
| 2 | Name the specific Schneider Electric SIS product line that was targeted. | `Triconex` | S1 - Introduction |
| 3 | What undocumented, proprietary engineering protocol did the attackers have to reverse-engineer in order to talk to the SIS controllers? | `TriStation` | S1 - 'Attribution' / 'Technical Analysis' |
| 4 | In what year did the first publicly known attack using this malware take place? | `2017` | S1; S4 ('between May and September 2017') |
| 5 | In which country did this first publicly known attack take place? | `Saudi Arabia` / `KSA` | Press coverage / UK government statement (not in S1-S4, see note) |
| 6 | Besides TRITON and TRISIS, what other name is this malware also known by in ICS security circles? | `HatMan` | S3 - Associated Software |
| 7 | What tracking name does Dragos use for the threat group behind this malware? | `XENOTIME` | S3 - TEMP.Veles Associated Groups |
| 8 | What tracking name does Mandiant/FireEye use for this same threat group? | `TEMP.Veles` / `TEMP Veles` | S2 - Overview |
| 9 | Where did the attacker gain the remote access they used to deploy the attack framework and reprogram the SIS controllers? | `SIS engineering workstation` / `an SIS engineering workstation` / `engineering workstation` / `the SIS engineering workstation` | S1 - 'Incident Summary' |
| 10 | The US Department of Justice indicted a Russian national linked to the development of this malware. What is his surname? | `Gladkikh` | S4 |

To obtain the flag: `SecurinetsENIT{f2cde5d17e96a268b564f174db45b20d}`
