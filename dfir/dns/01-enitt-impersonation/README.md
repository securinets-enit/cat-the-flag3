# ENIT Portal Impersonation

A DNS enumeration challenge. Nine flags hidden across standard service-
discovery and authentication records.

## Overview

Students at ENIT reported emails about a "student portal migration" and
"SSO re-enrollment". The link goes to a page designed to look like the
school's portal. The security team captured a single indicator from a
student's browser history: `enitt.online`.

The attacker is impersonating the school's domain. The player must
enumerate DNS records to recover nine flags.

## Difficulty

Medium.

## Category

DNS Enumeration

## Points

900 total, 100 per flag.

## Flags

| # | Flag |
|---|---|
| 1 | SecurinetsENIT{spf_policy_recon} |
| 2 | SecurinetsENIT{mail_policy_weak} |
| 3 | SecurinetsENIT{dkim_selector_found} |
| 4 | SecurinetsENIT{mta_sts_missing} |
| 5 | SecurinetsENIT{acme_challenge_leak} |
| 6 | SecurinetsENIT{srv_service_pivot} |
| 7 | SecurinetsENIT{sip_discovery} |
| 8 | SecurinetsENIT{autodiscover_leak} |
| 9 | SecurinetsENIT{matrix_homeserver} |

## Skills

- DNS record enumeration across multiple record types
- Understanding of standard underscore-prefixed records (SPF, DMARC,
  DKIM, MTA-STS, ACME)
- Service discovery via SRV records
- Reading TXT records for mail authentication policy
- Subdomain enumeration with wordlists

## Infrastructure

Pure Cloudflare DNS on the `enitt.online` zone. No servers, no askers.

## Task folder

- `README.md` — this file
- `description.md` — what the player sees
- `walkthrough.md` — full solution
