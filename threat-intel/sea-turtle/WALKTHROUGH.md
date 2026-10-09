## WALKTHROUGH: sea-turtle

## Hijacking The Internet's Phonebook

#### Difficulty: Easy

### Description

Users trying to reach your organization's legitimate domain keep landing on a fake login page. Your actual web server hasn't been touched. Nothing on your infrastructure was breached.

So how are your own users ending up somewhere else entirely?

Cisco Talos has a name for the actor that doesn't bother breaking into the target directly, and instead goes after the internet's phonebook itself.

**Reading list:** one Cisco Talos blog post from April 2019.

Answer the questions by connecting to: nc <PORT> <IP>

**Author:** Taha

### Sources

- **S1**: [Cisco Talos - DNS Hijacking Abuses Trust In Core Internet Service (Apr 2019)](https://blog.talosintelligence.com/seaturtle/)
- **S2**: [Cisco Talos - Sea Turtle keeps on swimming (Jul 2019)](https://blog.talosintelligence.com/sea-turtle-keeps-on-swimming/)

### Solution

Talos's original Sea Turtle post (S1) answers every question. The follow-up (S2) shows the actor continuing after disclosure. Note that the URL in the old INDEX (`/dns-hijacking-abuses-trust-in-core-internet-service/`) is a 404. The post lives at `/seaturtle/`.

Changes from the first draft: removed 'what infrastructure did it target? DNS' (answered by the description) and 'exact title of the blog post' (copy-paste, and fragile to match). The CVE question accepts all seven CVEs Talos lists. The region and registry answers accept natural variants (MENA, 'domain registry' without 'a'). The registry question is still precise about registry vs registrar, which is the point of it.

### Questions & Answers

The first answer is canonical; every listed answer is accepted (case-insensitive).

| # | Question | Accepted answers | Where to find it |
|---|---|---|---|
| 1 | Approximately how many organizations did Talos say were compromised during this campaign? Just give the number. | `40` | S1 - Executive Summary |
| 2 | Since what year had this campaign reportedly been active before its public disclosure? | `2017` | S1 - 'likely began as early as January 2017' |
| 3 | Name the Swedish DNS provider that Talos confirmed was compromised as part of this campaign. | `Netnod` | S1 - 'Credential harvesting with compromised SSL certificates' |
| 4 | What region of the world was primarily targeted by this campaign (governments, ministries, energy firms)? | `Middle East and North Africa` / `MENA` / `Middle East & North Africa` / `the Middle East and North Africa` | S1 - Executive Summary |
| 5 | This was the first known case of attackers compromising what type of organization - the entity that manages an entire top-level domain - for cyber-espionage purposes? | `a domain registry` / `domain registry` / `registry` / `a registry` / `domain name registry` / `a domain name registry` | S1 - 'How is this tradecraft different?' |
| 6 | Name one CVE number the actors exploited to initially breach their victims' infrastructure. | `CVE-2009-1151` / `CVE-2014-6271` / `CVE-2017-3881` / `CVE-2017-6736` / `CVE-2017-12617` / `CVE-2018-0296` / `CVE-2018-7600` | S1 - 'Initial access' |

To obtain the flag: `SecurinetsENIT{11d09b7e8da39b9a969865c0fa4d9ded}`
