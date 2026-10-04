# gh-cli-fake

Fake GitHub CLI download site used for DFIR CTF scenario authoring.

## Architecture

- Cloudflare (Flex mode) fronts the origin
- Nginx serves static HTML + download tarballs on port 80
- Victim's real IP extracted from `CF-Connecting-IP`

## Quick start

    ./build-downloads.sh
    docker compose up -d
    docker compose logs -f

Origin listens on `0.0.0.0:80`. Point Cloudflare A record at the VM's
static IP, set SSL mode to "Flexible", and enable proxy.

## Evidence

- `logs/access.log` — nginx forensic log (real client IP, UA, referer, cf_ray)
- `site/downloads/` — the served payloads
