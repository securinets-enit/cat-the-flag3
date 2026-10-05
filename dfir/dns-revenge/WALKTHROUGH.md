# DNS Revenge — Walkthrough

**Difficulty:** Hard
**Flags:** 6

## Flag 1 — Discover the delegation

Enumerate the parent zone `login-aws-amazon.cloud`. Look for NS
records that point somewhere other than Cloudflare.

    dig +short NS login-aws-amazon.cloud
    # albert.ns.cloudflare.com.
    # kehlani.ns.cloudflare.com.

    dig +short NS internal.login-aws-amazon.cloud
    # ns1.login-aws-amazon.cloud.
    # ns2.login-aws-amazon.cloud.

The subdomain `internal` has its own NS records. That is a delegation.

Flag is in a TXT record at the parent level:

    dig +short TXT _delegated.login-aws-amazon.cloud
    # "SecurinetsENIT{delegation_discovered}"

## Flag 2 — Query the delegated zone

The nameservers `ns1.login-aws-amazon.cloud` and `ns2.login-aws-amazon.cloud`
resolve to `35.188.95.225` — a server outside Cloudflare's network.

    dig +short A ns1.login-aws-amazon.cloud
    # 35.188.95.225

Query it directly:

    dig @ns1.login-aws-amazon.cloud TXT _verify.internal.login-aws-amazon.cloud +short
    # "SecurinetsENIT{delegated_zone_hidden}"

## Flag 3 — Another TXT in the delegated zone

    dig @ns1.login-aws-amazon.cloud TXT _secret.internal.login-aws-amazon.cloud +short
    # "SecurinetsENIT{real_delegation_works}"

## Flag 4 — A hidden TXT record

    dig @ns1.login-aws-amazon.cloud TXT _flag4.internal.login-aws-amazon.cloud +short
    # "SecurinetsENIT{nsec_walk_leak}"

The name suggests DNSSEC NSEC walking, but in this case the flag is
simply sitting in a TXT record. On a real DNSSEC-signed zone, NSEC
walking lets you enumerate every record without brute-force.

## Flag 5 — Zone transfer (AXFR)

Most DNS servers refuse AXFR. This one does not.

    dig @ns1.login-aws-amazon.cloud AXFR internal.login-aws-amazon.cloud

Output:

    _axfr-ok.internal.login-aws-amazon.cloud. 300 IN TXT "SecurinetsENIT{axfr_dump_success}"
    _flag4.internal.login-aws-amazon.cloud. 300 IN TXT "SecurinetsENIT{nsec_walk_leak}"
    _secret.internal.login-aws-amazon.cloud. 300 IN TXT "SecurinetsENIT{real_delegation_works}"
    _verify.internal.login-aws-amazon.cloud. 300 IN TXT "SecurinetsENIT{delegated_zone_hidden}"
    api.internal.login-aws-amazon.cloud. 300 IN A 10.128.0.3
    www.internal.login-aws-amazon.cloud. 300 IN CNAME api.internal.login-aws-amazon.cloud.

All flags visible in one query.

## Flag 6 — Follow the CNAME

    dig @ns1.login-aws-amazon.cloud CNAME www.internal.login-aws-amazon.cloud +short
    # api.internal.login-aws-amazon.cloud.

    dig @ns1.login-aws-amazon.cloud A api.internal.login-aws-amazon.cloud +short
    # 10.128.0.3

The CNAME chain ends at `api`, which resolves to an internal address.
The flag is embedded in the answer:

    dig @ns1.login-aws-amazon.cloud TXT _www.internal.login-aws-amazon.cloud +short
    # "SecurinetsENIT{www_chain_followed}"

## Summary

| # | Flag | Technique |
|---|---|---|
| 1 | SecurinetsENIT{delegation_discovered} | NS record enumeration |
| 2 | SecurinetsENIT{delegated_zone_hidden} | Direct authoritative query |
| 3 | SecurinetsENIT{real_delegation_works} | Delegated zone content |
| 4 | SecurinetsENIT{nsec_walk_leak} | TXT record in delegated zone |
| 5 | SecurinetsENIT{axfr_dump_success} | AXFR zone transfer |
| 6 | SecurinetsENIT{www_chain_followed} | CNAME chain in delegated zone |

## What you learn

- How NS delegation works in practice
- The difference between recursive and authoritative resolution
- Why some servers are queried directly
- AXFR as a reconnaissance technique
- How glue records make delegation possible
- Reading zone files exported via AXFR
