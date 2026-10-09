# Docker Basics — Walkthrough

**Author:** 7ankalis — Securinets ENIT
**Flags:** 3

## Pull and run

    docker pull sitaha/docker-basics:1.0
    docker run -it --rm sitaha/docker-basics:1.0

The -it flags give you an interactive terminal.

## Flag 1 — Hidden file

Follow the tutorial through steps 1–3. Eventually:

    cat .hidden_flag

    # SecurinetsENIT{d0ck3r_b451c5_f1l3_4cc355}

## Flag 2 — Environment variable

Step 4 asks you to run:

    env

The output contains:

    FLAG2=SecurinetsENIT{3nv1r0nm3n7_v4r14bl35}

## Flag 3 — Image metadata

Exit the container:

    exit

Then from the host:

    docker inspect sitaha/docker-basics:1.0 | jq -r '.[0].Config.Labels.flag'

    # SecurinetsENIT{d0ck3r_1n5p3c7_l4b3l5}

## Summary

| # | Flag | Location |
|---|---|---|
| 1 | SecurinetsENIT{d0ck3r_b451c5_f1l3_4cc355} | /tutorial/.hidden_flag |
| 2 | SecurinetsENIT{3nv1r0nm3n7_v4r14bl35} | FLAG2 env var |
| 3 | SecurinetsENIT{d0ck3r_1n5p3c7_l4b3l5} | Image label 'flag' |

## What the player learns

- docker pull
- docker run -it
- Container filesystem isolation
- Hidden files
- Environment variables
- docker inspect
- Image labels
