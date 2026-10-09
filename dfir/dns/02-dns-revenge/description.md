# DNS Revenge

**Difficulty:** Hard
**Category:** DNS Enumeration
**Points:** 600

## Brief

Investigators found a second typosquat domain during the ENIT
impersonation case:

    login-aws-amazon.cloud

This one is different. The attacker registered a subdomain that
delegates to their own nameservers. Not everything lives in Cloudflare.

Six flags are hidden across the parent zone and the delegated zone.
You will need to know how DNS actually works.

## Objectives

1. Enumerate records in the parent zone (Cloudflare-hosted)
2. Discover the delegated subdomain
3. Query the attacker's authoritative nameservers directly
4. Attempt a zone transfer against the delegated zone
5. Read records only visible from the authoritative server
6. Follow CNAME chains that cross zone boundaries

## Tools

    dig
    host
    nslookup
    dnsrecon
    dnsx
    amass

## Hints

- Not everything is answered by your default resolver
- `dig @` lets you ask a specific server
- Some nameservers are more cooperative than others
- AXFR is a legitimate operation that most servers refuse

## Flag format

    SecurinetsENIT{...}
