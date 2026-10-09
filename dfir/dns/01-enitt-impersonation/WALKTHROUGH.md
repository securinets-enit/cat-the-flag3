# ENIT Portal Impersonation — Walkthrough

**Difficulty:** Medium
**Flags:** 9

## Overview

The task is pure DNS enumeration. Nine flags are hidden across standard
service-discovery and authentication records. Each flag teaches a
different record type.

The underscore-prefix convention matters: `_dmarc`, `_domainkey`,
`_acme-challenge`, `_spf`, and SRV records like `_sso._tcp` are defined
by protocols. They are not discoverable by generic subdomain brute-
forcing. They require understanding what record types exist.

## Flag 1 — SPF record

SPF defines which mail servers are allowed to send email for the domain.

    dig +short TXT _spf.enitt.online
    # "SecurinetsENIT{spf_policy_recon}"

Players may also find it by querying the SPF record at the root:

    dig +short TXT enitt.online
    # "v=spf1 -all"

The root record is a decoy — a valid SPF policy that denies all mail.
The real SPF-related flag lives at the `_spf` subdomain.

Learn: SPF records are published as TXT records. Attackers sometimes
publish empty SPF records to appear legitimate while blocking all outbound
mail.

## Flag 2 — DMARC policy

DMARC tells receiving mail servers what to do when SPF or DKIM fails.

    dig +short TXT _dmarc.enitt.online
    # "v=DMARC1; p=reject; rua=mailto:SecurinetsENIT{mail_policy_weak}@dmarc.enitt.online"

The flag is embedded in the `rua` (aggregate report URI) field. In a real
scenario, this field is often an email address an analyst would collect.

Learn: DMARC records contain contact information. That contact info is
often useful during IR — it points to the domain owner or registrar.

## Flag 3 — DKIM selector

DKIM publishes public keys so receiving servers can verify email
signatures. Keys are stored at `<selector>._domainkey.<domain>`.

Common selectors: `default`, `mail`, `s1`, `google`, `k1`.

    dig +short TXT default._domainkey.enitt.online
    # "v=DKIM1; k=rsa; p=SecurinetsENIT{dkim_selector_found}"

The public key field contains the flag instead of a real RSA key.

Learn: DKIM selectors are a common subdomain enumeration target. Attackers
who forget to remove DKIM records expose the mail infrastructure they were
using.

## Flag 4 — MTA-STS policy

MTA-STS publishes a policy that tells senders to use strict TLS when
delivering mail.

    dig +short TXT _mta-sts.enitt.online
    # "SecurinetsENIT{mta_sts_missing}"

An empty MTA-STS record (or one containing the flag) means the attacker
never configured it — leaving the domain open to downgrade attacks.

Learn: MTA-STS absence is a real finding in phishing investigations. The
attacker's infrastructure is often misconfigured in ways that reveal
their operational patterns.

## Flag 5 — ACME challenge

ACME challenge records are used by Let's Encrypt and other CAs to verify
domain ownership.

    dig +short TXT _acme-challenge.enitt.online
    # "SecurinetsENIT{acme_challenge_leak}"

In a real scenario, a leftover `_acme-challenge` TXT record reveals
historical certificate issuance.

Learn: ACME challenge records are supposed to be transient — created
during validation and removed after. Leftover records indicate the
attacker's workflow and reveal which CAs they use.

## Flag 6 — SSO service discovery

SRV records advertise internal services. `_sso._tcp` suggests a single
sign-on endpoint.

    dig +short SRV _sso._tcp.enitt.online
    # 0 5 443 auth.enitt.online.

Follow the target hostname:

    dig +short TXT auth.enitt.online
    # "SecurinetsENIT{srv_service_pivot}"

Learn: SRV records point at hostnames. The target hostnames may have
their own A, CNAME, or TXT records worth enumerating.

## Flag 7 — SIP service discovery

SIP is used for VoIP. `_sip._tcp` advertises a SIP server.

    dig +short SRV _sip._tcp.enitt.online
    # 0 5 5060 sip.enitt.online.

    dig +short TXT sip.enitt.online
    # "SecurinetsENIT{sip_discovery}"

Learn: Enumerate every SRV prefix in the standard IANA service registry.
Common ones: `_sip`, `_sips`, `_xmpp`, `_ldap`, `_kerberos`,
`_autodiscover`, `_imap`, `_submission`, `_caldavs`, `_carddavs`,
`_matrix`.

## Flag 8 — Autodiscover service

`_autodiscover._tcp` is used by Microsoft Exchange clients to find their
mail server automatically.

    dig +short SRV _autodiscover._tcp.enitt.online
    # 0 5 443 autodiscover.enitt.online.

    dig +short TXT autodiscover.enitt.online
    # "SecurinetsENIT{autodiscover_leak}"

Learn: Autodiscover is a common reconnaissance target. If a domain has an
autodiscover record, it usually runs Microsoft Exchange or Office 365 —
useful intelligence about the target organization.

## Flag 9 — Matrix homeserver

Matrix is a decentralized messaging protocol. `_matrix._tcp` advertises
the homeserver.

    dig +short SRV _matrix._tcp.enitt.online
    # 0 5 443 matrix.enitt.online.

    dig +short TXT matrix.enitt.online
    # "SecurinetsENIT{matrix_homeserver}"

Learn: Federation protocols like Matrix publish their endpoint via SRV.
Enumerating federation records reveals what other infrastructure a
domain is connected to.

## Full enumeration script

    #!/bin/bash

    DOMAIN=enitt.online

    echo "=== Authentication records ==="
    dig +short TXT _spf.$DOMAIN
    dig +short TXT _dmarc.$DOMAIN
    dig +short TXT default._domainkey.$DOMAIN
    dig +short TXT _mta-sts.$DOMAIN

    echo "=== ACME ==="
    dig +short TXT _acme-challenge.$DOMAIN

    echo "=== Service discovery ==="
    for svc in _sso._tcp _sip._tcp _autodiscover._tcp _matrix._tcp; do
      echo "--- $svc ---"
      dig +short SRV $svc.$DOMAIN
    done

    echo "=== Follow targets ==="
    dig +short TXT auth.$DOMAIN
    dig +short TXT sip.$DOMAIN
    dig +short TXT autodiscover.$DOMAIN
    dig +short TXT matrix.$DOMAIN

## Summary

| # | Flag | Record |
|---|---|---|
| 1 | SecurinetsENIT{spf_policy_recon} | TXT _spf |
| 2 | SecurinetsENIT{mail_policy_weak} | TXT _dmarc |
| 3 | SecurinetsENIT{dkim_selector_found} | TXT default._domainkey |
| 4 | SecurinetsENIT{mta_sts_missing} | TXT _mta-sts |
| 5 | SecurinetsENIT{acme_challenge_leak} | TXT _acme-challenge |
| 6 | SecurinetsENIT{srv_service_pivot} | SRV _sso._tcp + TXT auth |
| 7 | SecurinetsENIT{sip_discovery} | SRV _sip._tcp + TXT sip |
| 8 | SecurinetsENIT{autodiscover_leak} | SRV _autodiscover._tcp + TXT autodiscover |
| 9 | SecurinetsENIT{matrix_homeserver} | SRV _matrix._tcp + TXT matrix |

## What the player learns

- The underscore-prefix convention and which protocols use it
- The difference between hostname enumeration and protocol enumeration
- The value of SRV records for infrastructure mapping
- How misconfigured mail and certificate records leak operational intel
- The pattern of chaining records (SRV target → TXT lookup)
