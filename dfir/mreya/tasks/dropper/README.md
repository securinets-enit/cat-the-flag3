# Task 3 — The Dropper

**Difficulty:** Medium

## Brief

The user ran the installer from the downloaded archive with `sudo`. Read the
installer, reconstruct what it does, answer the analysis questions.

## Running

    docker compose run --rm task-03

Inside the container:

    cd /case
    mkdir -p /tmp/x
    tar -xzf evidence/gh_2.42.1_linux_amd64.tar.gz -C /tmp/x
    cat /tmp/x/gh_2.42.1_linux_amd64/install.sh
    ./dropper

## Flag format

`SecurinetsENIT{...}`
