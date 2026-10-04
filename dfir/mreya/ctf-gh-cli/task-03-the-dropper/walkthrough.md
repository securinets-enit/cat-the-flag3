# Walkthrough — Task 3

`install.sh` does four things:

1. Copies a fake `gh` binary to `/usr/local/bin/`
2. Fetches a second-stage binary from a CDN URL constructed from variables
3. Installs cron persistence (`*/30` + `@reboot`)
4. Executes the binary immediately in the background

The `_BUILD` variable is the flag.

## Flag

`SecurinetsENIT{75efb0959defbc4b1bdcc6247381b437}`
