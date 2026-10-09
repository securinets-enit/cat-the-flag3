# DNS Revenge

A hard DNS enumeration challenge. Real NS delegation, real AXFR,
real authoritative queries.

## Overview

A second attacker domain was found during the investigation:
`login-aws-amazon.cloud`. Unlike the first typosquat, this one has a
delegated subdomain that points at attacker-controlled nameservers.

Players must discover the delegation, query the authoritative
nameservers directly, and extract flags from the delegated zone.

## Difficulty

Hard.

## Category

DNS Enumeration

## Points

600 (6 flags, 100 each)

## Flags

| # | Flag |
|---|---|
| 1 | SecurinetsENIT{delegation_discovered} |
| 2 | SecurinetsENIT{delegated_zone_hidden} |
| 3 | SecurinetsENIT{real_delegation_works} |
| 4 | SecurinetsENIT{nsec_walk_leak} |
| 5 | SecurinetsENIT{axfr_dump_success} |
| 6 | SecurinetsENIT{www_chain_followed} |

## Infrastructure

- Cloudflare zone: login-aws-amazon.cloud
- Delegated subdomain: internal.login-aws-amazon.cloud
- Authoritative NS: ns1.login-aws-amazon.cloud / ns2.login-aws-amazon.cloud
- Nameserver VM: dns-ns (GCP, 35.188.95.225)
- BIND 9 authoritative server

## Skills

- NS delegation discovery
- Authoritative queries with dig @
- Zone transfer attempts (AXFR)
- Reading glue records
- Following CNAME chains in delegated zones
- Understanding recursive vs authoritative resolution
