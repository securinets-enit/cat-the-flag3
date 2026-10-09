# CTF Infrastructure — Master Reference

Author-side documentation. Everything needed to recover, rebuild, or
debug the infrastructure.

## Overview

| Series / Task | Domain / Image | Flags | Purpose |
|---|---|---|---|
| gh-cli-supply-chain | cdnjs-mirror.net | 5 | Fake GitHub CLI download site, real Mythic C2 |
| npm-supply-chain | webhook-relay.cloud | 1 | Malicious npm package + live C2 |
| enitt-impersonation | enitt.online | 9 | DNS enumeration on a single domain |
| dns-revenge | login-aws-amazon.cloud | 6 | DNS delegation + AXFR |
| container-series-1 | sitaha/docker-basics:1.0 | 3 | Docker fundamentals tutorial |
| container-series-2 | sitaha/sysdiag:3.1.2 | 5 | Static image forensics |
| container-series-3 | sitaha/webhook-relay:2.4.0 | 5 | Runtime container forensics |
| Total | | 34 | |

Author branding:
- Hosting infrastructure: GCP project rotato-paper
- Docker Hub account: sitaha
- CTF author credit: 7ankalis — Securinets ENIT

## GCP VMs

All VMs run on the rotato-paper project. Zone us-central1-a.

### gh-cli-fake-vm

| Property | Value |
|---|---|
| Machine type | e2-small |
| Network | default |
| Internal IP | 10.128.0.2 |
| External IP | 34.135.159.63 |
| Tags | http-server |
| Purpose | Fake GitHub CLI site, evidence hosting, task askers |

Ports:
- 80 (nginx, fake site)
- 9996, 9997, 9998, 9999 (task askers)

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
| Tags | rotato, webhook-relay |
| Purpose | NPM supply-chain C2 |

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

Ports:
- 22 (SSH)
- 53 TCP/UDP (DNS)

Zones served:
- internal.login-aws-amazon.cloud

Recovery:

    gcloud compute instances start dns-ns --zone=us-central1-a
    gcloud compute ssh dns-ns --zone=us-central1-a
    sudo systemctl start named

### Other VMs

- rt-mgmt-usw1-01 (10.0.0.6) — management
- rt-rdr-usw1-01 (10.0.0.7) — redirector, unused
- rt-rdr-usw1-02 (10.0.0.8) — redirector, unused

## Firewall Rules

| Rule | Network | Ports | Source | Target tag |
|---|---|---|---|---|
| allow-http | default | tcp:80 | 0.0.0.0/0 | http-server |
| allow-https | default | tcp:443 | 0.0.0.0/0 | http-server |
| allow-ctf-askers | default | tcp:9996-9999 | 0.0.0.0/0 | http-server |
| allow-dns | default | tcp:53,udp:53 | 0.0.0.0/0 | dns-server |
| allow-ssh-myip | rotato-vpc | tcp:22 | admin IP | rotato |
| allow-ssh-webhook | rotato-vpc | tcp:22 | 0.0.0.0/0 | webhook-relay |
| allow-http-webhook | rotato-vpc | tcp:80 | Cloudflare | webhook-relay |
| allow-http-c2-public | rotato-vpc | tcp:80,tcp:443 | 0.0.0.0/0 | c2-mythic |

## Cloudflare Domains

| Domain | Purpose | Origin VM | SSL mode |
|---|---|---|---|
| cdnjs-mirror.net | Fake GitHub CLI site | gh-cli-fake-vm | Flexible |
| gh-actions-runner.xyz | Mythic C2 | rt-c2-usw1-01 | Flexible |
| webhook-relay.cloud | NPM C2 | c2-webhook-relay | Flexible |
| enitt.online | ENIT Impersonation | (Cloudflare DNS only) | — |
| login-aws-amazon.cloud | DNS Revenge parent | (Cloudflare DNS only) | — |
| login-aws-amazon.biz | Decoy | (empty) | — |
| login-aws-amazon.shop | Decoy | (empty) | — |
| login-aws-amazon.net | Decoy | (empty) | — |
| login-aws-amazon.info | Decoy | (empty) | — |
| login-aws-amazon.club | Decoy | (empty) | — |
| login-aws-amazon.store | Decoy | (empty) | — |

## Docker Hub Images

| Image | Digest | Size |
|---|---|---|
| sitaha/docker-basics:1.0 | sha256:3873105aeadcd08b593f492b88f5787ddcfac8a5f39a12a6236abbbb88955d4b | ~11 MB |
| sitaha/sysdiag:3.1.2 | sha256:1668d81bb895f8f85745841cd5b5392d8e47aa07ac17138e27af7b782eebf9c0 | ~15 MB |
| sitaha/webhook-relay:2.4.0 | sha256:91ff120658367cb3c817ea7823730dd31975151cadeca9aa11c18e5ba02b0b58 | ~60 MB |

Build sources on disk:

- ~/securinets/ctf/cat-the-flag3/dfir/containers/01-docker-basics
- ~/securinets/ctf/cat-the-flag3/dfir/containers/02-sysdiag
- ~/securinets/ctf/cat-the-flag3/dfir/containers/03-webhook-relay

## gh-cli-supply-chain

Five tasks. Handouts served from cdnjs-mirror.net.

| Task | Evidence | Interface | Flag |
|---|---|---|---|
| 1 — The Bait | places.sqlite, downloads.sqlite, page.html | none | SecurinetsENIT{aa24756f4410809ecc650d58404ee1f7} |
| 2 — The Recon | none | nc :9999 | SecurinetsENIT{9b6d946fc44eb755d906b366c7c794f1} |
| 3 — The Dropper | gh_2.42.1_linux_amd64.tar.gz | nc :9998 | SecurinetsENIT{75efb0959defbc4b1bdcc6247381b437} |
| 4 — The Implant | gh-completion, traffic.pcapng, telemetry | nc :9997 | SecurinetsENIT{5398f82818903750fc0d72e94c5f3304} |
| 5 — The Beacon | beacon.pcapng | nc :9996 | SecurinetsENIT{4b094f5e62c3ca3257c2571d8ab1d059} |

## npm-supply-chain

Single task — The Merge.

| Property | Value |
|---|---|
| Repo | github.com/john-milner/meterex |
| C2 | webhook-relay.cloud/api/v2/telemetry/ingest |
| Header | X-Analytics-Signature: telemetry_2026_report_ac03 |
| Flag | SecurinetsENIT{5a005bab5fed4fc5bf3e56259ed0e284} |

## enitt-impersonation

Nine flags in Cloudflare DNS TXT records. No servers.

| # | Flag | Record |
|---|---|---|
| 1 | SecurinetsENIT{b451c_dn5_r3c0n} | TXT _verify.enitt.online |
| 2 | SecurinetsENIT{m41l_p0l1cy_w34k} | TXT _dmarc.enitt.online (rua) |
| 3 | SecurinetsENIT{5ubd0m41n_hun7_c0mpl3t3} | TXT _acme-challenge.enitt.online |
| 4 | SecurinetsENIT{mx_h1dd3n} | TXT mail.enitt.online |
| 5 | SecurinetsENIT{cn4m3_ch41n} | TXT final.enitt.online |
| 6 | SecurinetsENIT{5rv_r3c0rd_p1v07} | TXT auth.enitt.online |
| 7 | SecurinetsENIT{c44_4u7h0r17y_l1m173d} | TXT _caa.enitt.online |
| 8 | SecurinetsENIT{dn55ec_n07_3n4bl3d} | TXT _dnssec.enitt.online |
| 9 | SecurinetsENIT{20n3_7r4n5f3r_bl0ck3d} | TXT _axfr.enitt.online |

Recovery: none needed. Cloudflare hosts everything.

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

BIND zone: /etc/bind/zones/internal.login-aws-amazon.cloud.zone on dns-ns

Change a flag:

    gcloud compute ssh dns-ns --zone=us-central1-a
    sudo vim /etc/bind/zones/internal.login-aws-amazon.cloud.zone
    sudo named-checkzone internal.login-aws-amazon.cloud /etc/bind/zones/internal.login-aws-amazon.cloud.zone
    sudo systemctl reload named

## container-series-1 — Docker Basics

| Property | Value |
|---|---|
| Image | sitaha/docker-basics:1.0 |
| Difficulty | Easy |
| Flags | 3 |
| Source | ~/securinets/ctf/cat-the-flag3/dfir/containers/01-docker-basics |

Flags:

| # | Flag | Where |
|---|---|---|
| 1 | SecurinetsENIT{d0ck3r_b451c5_f1l3_4cc355} | /tutorial/.hidden_flag |
| 2 | SecurinetsENIT{3nv1r0nm3n7_v4r14bl35} | FLAG2 env var |
| 3 | SecurinetsENIT{d0ck3r_1n5p3c7_l4b3l5} | Image label 'flag' |

Rebuild:

    cd ~/securinets/ctf/cat-the-flag3/dfir/containers/01-docker-basics
    ./build.sh
    docker push sitaha/docker-basics:1.0

## container-series-2 — Image Forensics

| Property | Value |
|---|---|
| Image | sitaha/sysdiag:3.1.2 |
| Difficulty | Medium |
| Flags | 5 |
| Source | ~/securinets/ctf/cat-the-flag3/dfir/containers/02-sysdiag |

Flags:

| # | Flag | Where |
|---|---|---|
| 1 | SecurinetsENIT{curl_p1p3_4bu53} | docker history RUN command |
| 2 | SecurinetsENIT{r3v1510n_fl4g} | Image label revision |
| 3 | SecurinetsENIT{d3l373d_l4y3r5_r3v34l_4ll} | Deleted file in a layer blob |
| 4 | SecurinetsENIT{b4ckd00r_u53r_p4sswd} | /etc/passwd GECOS field |
| 5 | SecurinetsENIT{5tr1ng5_1n_b1n4ry_n3v3r_l13} | strings on the diag binary |

Rebuild:

    cd ~/securinets/ctf/cat-the-flag3/dfir/containers/02-sysdiag
    ./build.sh
    ./solver.sh
    docker push sitaha/sysdiag:3.1.2

Note: docker save produces OCI format. Layers are in blobs/sha256/,
not in */layer.tar. The solver handles both.

## container-series-3 — Runtime Forensics

| Property | Value |
|---|---|
| Image | sitaha/webhook-relay:2.4.0 |
| Difficulty | Medium-Hard |
| Flags | 5 |
| Source | ~/securinets/ctf/cat-the-flag3/dfir/containers/03-webhook-relay |

Flags:

| # | Flag | Where |
|---|---|---|
| 1 | SecurinetsENIT{3nv_1n5p3c7_5h0w5_4ll} | docker inspect env |
| 2 | SecurinetsENIT{l0g5_n3v3r_l13} | docker logs |
| 3 | SecurinetsENIT{c2_c0nf1g_3xp053d} | /etc/relay.conf |
| 4 | SecurinetsENIT{cr0n_p3r51573nc3_f0und} | /etc/cron.d/webhook-sync |
| 5 | SecurinetsENIT{pr0c_n3t_w0rk5} | ps aux inside container |

Rebuild:

    cd ~/securinets/ctf/cat-the-flag3/dfir/containers/03-webhook-relay
    ./build.sh
    ./solver.sh
    docker push sitaha/webhook-relay:2.4.0

Note: the .relay-agent C binary must be compiled for musl, not
glibc. build.sh compiles it inside a temporary Alpine container.

## Solver Scripts

| Script | Location | Verifies |
|---|---|---|
| solve-enitt.sh | local | 9 ENIT Impersonation flags |
| solve-dns-revenge.sh | local | 6 DNS Revenge flags |
| solver.sh (docker-2) | image-forensics dir | 5 Image Forensics flags |
| solver.sh (webhook-relay) | runtime-forensics dir | 5 Runtime Forensics flags |

## Rebuild Order

If rebuilding from scratch:

1. Restore source from local backup (~/securinets/ctf/cat-the-flag3/)

2. gh-cli-fake-vm
   - docker compose up -d in ~/gh-cli-fake
   - docker compose up -d in ~/askers
   - Confirm cdnjs-mirror.net serves

3. rt-c2-usw1-01
   - Mythic install, http profile, Poseidon agent
   - Point gh-actions-runner.xyz at this VM

4. c2-webhook-relay
   - Deploy relay container
   - Point webhook-relay.cloud at this VM

5. dns-ns
   - Install BIND, deploy zone file
   - Add Cloudflare NS delegation + glue

6. Cloudflare
   - Verify all A records and TXT records
   - SSL modes: Flexible for all proxied zones

7. Docker Hub
   - make build-containers (or cd each containers/0N-* dir)
   - ./build.sh
   - docker push sitaha/<image>

8. Test
   - ./solve-enitt.sh
   - ./solve-dns-revenge.sh
   - cd containers/01-docker-basics && docker run -it --rm sitaha/docker-basics:1.0
   - cd containers/02-sysdiag && ./solver.sh
   - cd containers/03-webhook-relay && ./solver.sh

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
| container-series-1 | 300 |
| container-series-2 | 500 |
| container-series-3 | 500 |
| Total | 3800 |

## Container Series Digests

| Image | Digest |
|---|---|
| sitaha/docker-basics:1.0 | sha256:3873105aeadcd08b593f492b88f5787ddcfac8a5f39a12a6236abbbb88955d4b |
| sitaha/sysdiag:3.1.2 | sha256:1668d81bb895f8f85745841cd5b5392d8e47aa07ac17138e27af7b782eebf9c0 |
| sitaha/webhook-relay:2.4.0 | sha256:91ff120658367cb3c817ea7823730dd31975151cadeca9aa11c18e5ba02b0b58 |

## Container Series Build Dependencies

| Build step | Requires |
|---|---|
| Task 1 | Docker only |
| Task 2 | Docker + gcc (compiled on host, glibc-linked) |
| Task 3 | Docker + a Docker daemon that can run Alpine (compiled inside Alpine for musl) |

## Author Branding

- CTF author: 7ankalis — Securinets ENIT
- Docker Hub: sitaha
- Container images embed: maintainer=7ankalis, vendor=Securinets ENIT
