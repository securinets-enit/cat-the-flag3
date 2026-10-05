# CTF Infrastructure — Master Reference

Author-side documentation for all challenges. Everything needed to
recover, rebuild, or debug the infrastructure.

## Overview

| Chain / Task | Domain | Flags | Purpose |
|---|---|---|---|
| gh-cli-supply-chain | cdnjs-mirror.net | 5 | Fake GitHub CLI download site, real Mythic C2 |
| npm-supply-chain | webhook-relay.cloud | 1 | Malicious npm package + live C2 |
| enitt-impersonation | enitt.online | 9 | DNS enumeration on a single domain |
| dns-revenge | login-aws-amazon.cloud | 6 | DNS delegation + AXFR |

## GCP VMs

All VMs run on the `rotato-paper` GCP project. Zones are us-central1-a.

### gh-cli-fake-vm

| Property | Value |
|---|---|
| Machine type | e2-small |
| Network | default |
| Internal IP | 10.128.0.2 |
| External IP | 34.135.159.63 |
| Tags | http-server |
| Purpose | Fake GitHub CLI site, evidence hosting, task askers |
| Runs | nginx (fake site), 4 Go asker containers |

Ports:
- 80 (nginx)
- 9996, 9997, 9998, 9999 (askers)

Domains:
- cdnjs-mirror.net → Cloudflare proxied → this VM

Recovery:

    gcloud compute instances start gh-cli-fake-vm --zone=us-central1-a
    gcloud compute ssh gh-cli-fake-vm --zone=us-central1-a
    cd ~/gh-cli-fake && sudo docker compose up -d
    cd ~/askers && sudo docker compose up -d

### rt-c2-usw1-01 (Mythic)

| Property | Value |
|---|---|
| Machine type | e2-medium |
| Network | rotato-vpc |
| Internal IP | 10.0.0.9 |
| External IP | 34.170.160.245 |
| Tags | c2-mythic, rotato |
| Purpose | Mythic C2 |
| Runs | Mythic Docker stack |

Ports:
- 22 (SSH)
- 7443 (Mythic UI, localhost only)
- 80 (HTTP profile)

Domains:
- gh-actions-runner.xyz → Cloudflare proxied → this VM

Recovery:

    gcloud compute instances start rt-c2-usw1-01 --zone=us-central1-a
    gcloud compute ssh rt-c2-usw1-01 --zone=us-central1-a
    cd ~/Mythic && sudo ./mythic-cli start

### c2-webhook-relay

| Property | Value |
|---|---|
| Machine type | e2-micro |
| Network | rotato-vpc |
| Internal IP | 10.0.0.x |
| External IP | (see gcloud describe) |
| Tags | rotato, webhook-relay |
| Purpose | NPM supply-chain C2 |
| Runs | Docker container `webhook-relay` (Flask + gunicorn) |

Ports:
- 22 (SSH)
- 80 (HTTP, Cloudflare-only via firewall)

Domains:
- webhook-relay.cloud → Cloudflare proxied → this VM

Recovery:

    gcloud compute instances start c2-webhook-relay --zone=us-central1-a
    gcloud compute ssh c2-webhook-relay --zone=us-central1-a
    cd ~/relay && sudo docker compose up -d

### dns-ns

| Property | Value |
|---|---|
| Machine type | e2-micro |
| Network | default |
| Internal IP | 10.128.0.3 |
| External IP | 35.188.95.225 |
| Tags | dns-server |
| Purpose | Authoritative nameserver for DNS Revenge |
| Runs | BIND 9.18 on Ubuntu 22.04 |

Ports:
- 22 (SSH)
- 53 TCP/UDP (DNS)

Zones served:
- internal.login-aws-amazon.cloud

Recovery:

    gcloud compute instances start dns-ns --zone=us-central1-a
    gcloud compute ssh dns-ns --zone=us-central1-a
    sudo systemctl start named

### Redirectors (unused)

- rt-rdr-usw1-01 — 10.0.0.7
- rt-rdr-usw1-02 — 10.0.0.8

### Management

- rt-mgmt-usw1-01 — 10.0.0.6

## Firewall Rules

| Rule | Network | Ports | Source | Target tag |
|---|---|---|---|---|
| allow-http | default | tcp:80 | 0.0.0.0/0 | http-server |
| allow-https | default | tcp:443 | 0.0.0.0/0 | http-server |
| allow-ctf-askers | default | tcp:9996-9999 | 0.0.0.0/0 | http-server |
| allow-dns | default | tcp:53,udp:53 | 0.0.0.0/0 | dns-server |
| allow-ssh-myip | rotato-vpc | tcp:22 | (admin IP) | rotato |
| allow-ssh-webhook | rotato-vpc | tcp:22 | 0.0.0.0/0 | webhook-relay |
| allow-http-webhook | rotato-vpc | tcp:80 | Cloudflare | webhook-relay |
| allow-http-c2-public | rotato-vpc | tcp:80,tcp:443 | 0.0.0.0/0 | c2-mythic |

## Cloudflare Domains

| Domain | Purpose | Origin VM | SSL mode | Notes |
|---|---|---|---|---|
| cdnjs-mirror.net | Fake GitHub CLI site | gh-cli-fake-vm | Flexible | |
| gh-actions-runner.xyz | Mythic C2 | rt-c2-usw1-01 | Flexible | |
| webhook-relay.cloud | NPM C2 | c2-webhook-relay | Flexible | Bypass cache on /api/ |
| enitt.online | ENIT Impersonation | (Cloudflare-only) | — | 9 TXT records only |
| login-aws-amazon.cloud | DNS Revenge parent | (Cloudflare-only) | — | NS delegation + glue |
| login-aws-amazon.biz | Decoy | (Cloudflare-only) | — | Empty |
| login-aws-amazon.shop | Decoy | (Cloudflare-only) | — | Empty |
| login-aws-amazon.net | Decoy | (Cloudflare-only) | — | Empty |
| login-aws-amazon.info | Decoy | (Cloudflare-only) | — | Empty |
| login-aws-amazon.club | Decoy | (Cloudflare-only) | — | Empty |
| login-aws-amazon.store | Decoy | (Cloudflare-only) | — | Empty |

## gh-cli-supply-chain

Five tasks. Handouts are evidence files served by cdnjs-mirror.net.

### Task 1 — The Bait

- Evidence: places.sqlite, downloads.sqlite, page.html
- Flag: SecurinetsENIT{aa24756f4410809ecc650d58404ee1f7}

### Task 2 — The Recon

- Interface: nc <gh-cli-fake-vm-ip> 9999
- Flag: SecurinetsENIT{9b6d946fc44eb755d906b366c7c794f1}

### Task 3 — The Dropper

- Evidence: gh_2.42.1_linux_amd64.tar.gz
- Flag: SecurinetsENIT{75efb0959defbc4b1bdcc6247381b437}

### Task 4 — The Implant

- Evidence: gh-completion, traffic.pcapng, host telemetry
- Interface: nc <gh-cli-fake-vm-ip> 9997
- Flag: SecurinetsENIT{5398f82818903750fc0d72e94c5f3304}

### Task 5 — The Beacon

- Evidence: beacon.pcapng
- Interface: nc <gh-cli-fake-vm-ip> 9996
- Flag: SecurinetsENIT{4b094f5e62c3ca3257c2571d8ab1d059}

## npm-supply-chain

Single task — The Merge.

- Repo: github.com/john-milner/meterex
- C2: webhook-relay.cloud/api/v2/telemetry/ingest
- Header: X-Analytics-Signature: telemetry_2026_report_ac03
- Flag: SecurinetsENIT{5a005bab5fed4fc5bf3e56259ed0e284}

## enitt-impersonation

Nine flags in Cloudflare DNS. All TXT records.

| # | Flag | Record |
|---|---|---|
| 1 | SecurinetsENIT{b451c_dn5_r3c0n} | TXT _verify.enitt.online |
| 2 | SecurinetsENIT{m41l_p0l1cy_w34k} | TXT _dmarc.enitt.online (rua) |
| 3 | SecurinetsENIT{5ubd0m41n_hun7_c0mpl3t3} | TXT _acme-challenge.enitt.online |
| 4 | SecurinetsENIT{mx_h1dd3n} | TXT mail.enitt.online |
| 5 | SecurinetsENIT{cn4m3_ch41n} | TXT final.enitt.online |
| 6 | SecurinetsENIT{5rv_r3c0rd_p1v07} | TXT auth.enitt.online + SRV _sso._tcp |
| 7 | SecurinetsENIT{c44_4u7h0r17y_l1m173d} | TXT _caa.enitt.online |
| 8 | SecurinetsENIT{dn55ec_n07_3n4bl3d} | TXT _dnssec.enitt.online |
| 9 | SecurinetsENIT{20n3_7r4n5f3r_bl0ck3d} | TXT _axfr.enitt.online |

Recovery: none needed. Cloudflare hosts everything.

Flag changes: edit each TXT in Cloudflare dashboard.

## dns-revenge

Six flags across Cloudflare and BIND.

| # | Flag | Where |
|---|---|---|
| 1 | SecurinetsENIT{d3l3g4710n_d15c0v3r3d} | TXT _delegated.login-aws-amazon.cloud (Cloudflare) |
| 2 | SecurinetsENIT{d3l3g473d_20n3_h1dd3n} | TXT _verify.internal.login-aws-amazon.cloud (BIND) |
| 3 | SecurinetsENIT{r34l_d3l3g4710n_w0rk5} | TXT _secret.internal.login-aws-amazon.cloud (BIND) |
| 4 | SecurinetsENIT{n53c_w4lk_l34k} | TXT _flag4.internal.login-aws-amazon.cloud (BIND) |
| 5 | SecurinetsENIT{4xfr_dump_5ucc355} | TXT _axfr-ok.internal.login-aws-amazon.cloud (BIND) |
| 6 | SecurinetsENIT{www_ch41n_f0ll0w3d} | TXT _www.internal.login-aws-amazon.cloud (BIND) |

Cloudflare records:

    _delegated.login-aws-amazon.cloud    TXT    "SecurinetsENIT{d3l3g4710n_d15c0v3r3d}"

    ns1.login-aws-amazon.cloud           A      35.188.95.225 (DNS only)
    ns2.login-aws-amazon.cloud           A      35.188.95.225 (DNS only)
    internal.login-aws-amazon.cloud      NS     ns1.login-aws-amazon.cloud
    internal.login-aws-amazon.cloud      NS     ns2.login-aws-amazon.cloud

BIND zone file: `/etc/bind/zones/internal.login-aws-amazon.cloud.zone` on dns-ns

Config: `/etc/bind/named.conf.local`

    zone "internal.login-aws-amazon.cloud" {
        type master;
        file "/etc/bind/zones/internal.login-aws-amazon.cloud.zone";
        allow-transfer { any; };
    };

Change a flag:

    gcloud compute ssh dns-ns --zone=us-central1-a
    sudo vim /etc/bind/zones/internal.login-aws-amazon.cloud.zone
    sudo named-checkzone internal.login-aws-amazon.cloud /etc/bind/zones/internal.login-aws-amazon.cloud.zone
    sudo systemctl reload named

## Solver Scripts

- solve-enitt.sh — verifies 9 ENIT Impersonation flags
- solve-dns-revenge.sh — verifies 6 DNS Revenge flags

Both run from any machine with dig installed.

## Rebuild Order

If rebuilding everything from scratch:

1. gh-cli-fake-vm
   - Clone project from local backup
   - docker compose up -d
   - Confirm cdnjs-mirror.net resolves and serves

2. rt-c2-usw1-01
   - Mythic install
   - Install http profile + Poseidon agent
   - Point gh-actions-runner.xyz at this VM

3. c2-webhook-relay
   - Deploy relay container
   - Point webhook-relay.cloud at this VM

4. dns-ns
   - Install BIND
   - Deploy zone file
   - Add Cloudflare NS delegation + glue records

5. Cloudflare
   - Verify all A records point at correct VMs
   - Verify all TXT records contain correct flags
   - Verify SSL modes are Flexible

6. Test
   - Run solve-enitt.sh
   - Run solve-dns-revenge.sh
   - Test webhook-relay.cloud with the exact request
   - Visit cdnjs-mirror.net in a browser

## Points Summary

| Task | Points |
|---|---|
| gh-cli Task 1 | 100 |
| gh-cli Task 2 | 100 |
| gh-cli Task 3 | 100 |
| gh-cli Task 4 | 200 |
| gh-cli Task 5 | 300 |
| npm The Merge | 200 |
| ENIT Impersonation | 900 |
| DNS Revenge | 600 |
| Total | 2500 |
