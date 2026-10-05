#!/usr/bin/env bash
#
# solve-dns-revenge.sh — verify all 6 DNS Revenge flags from a remote host.
#
# Usage: ./solve-dns-revenge.sh
#

set -u

PARENT="login-aws-amazon.cloud"
SUBDOMAIN="internal.${PARENT}"
NS1="ns1.${PARENT}"
NS2="ns2.${PARENT}"

# ---------- Colors ----------
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASS=0
FAIL=0

check() {
    local label="$1"
    local expected="$2"
    local got="$3"

    if echo "$got" | grep -qF "$expected"; then
        printf "${GREEN}[PASS]${NC} %s\n" "$label"
        printf "       %s\n" "$expected"
        PASS=$((PASS + 1))
    else
        printf "${RED}[FAIL]${NC} %s\n" "$label"
        printf "       expected: %s\n" "$expected"
        printf "       got:      %s\n" "${got:-<empty>}"
        FAIL=$((FAIL + 1))
    fi
}

echo "=================================================="
echo " DNS Revenge — Remote Flag Verification"
echo " Target: ${PARENT}"
echo "=================================================="
echo

# ---------- Preflight ----------
printf "${BLUE}[*]${NC} Checking delegation of %s\n" "$SUBDOMAIN"
DELEGATION=$(dig +short NS "$SUBDOMAIN" @1.1.1.1)
if [ -z "$DELEGATION" ]; then
    printf "${RED}[!]${NC} No NS records for %s\n" "$SUBDOMAIN"
    printf "     The delegation is not live. Aborting.\n"
    exit 1
fi
printf "    Delegated to:\n"
echo "$DELEGATION" | sed 's/^/      /'
echo

printf "${BLUE}[*]${NC} Checking that %s resolves to an IP\n" "$NS1"
NS_IP=$(dig +short A "$NS1" @1.1.1.1 | head -1)
if [ -z "$NS_IP" ]; then
    printf "${RED}[!]${NC} %s does not resolve. Aborting.\n" "$NS1"
    exit 1
fi
printf "    %s -> %s\n" "$NS1" "$NS_IP"
echo

# ---------- Flag checks ----------
echo "=================================================="
echo " Flag Verification"
echo "=================================================="
echo

# Flag 1 — Cloudflare TXT
printf "${YELLOW}[1/6]${NC} Flag 1 — delegation_discovered (Cloudflare TXT)\n"
OUT=$(dig +short TXT "_delegated.${PARENT}" @1.1.1.1)
check "Flag 1" "SecurinetsENIT{d3l3g4710n_d15c0v3r3d}" "$OUT"
echo

# Flag 2 — BIND TXT
printf "${YELLOW}[2/6]${NC} Flag 2 — delegated_zone_hidden (authoritative TXT)\n"
OUT=$(dig +short TXT "_verify.${SUBDOMAIN}" "@${NS1}")
check "Flag 2" "SecurinetsENIT{d3l3g473d_20n3_h1dd3n}" "$OUT"
echo

# Flag 3 — BIND TXT
printf "${YELLOW}[3/6]${NC} Flag 3 — real_delegation_works (authoritative TXT)\n"
OUT=$(dig +short TXT "_secret.${SUBDOMAIN}" "@${NS1}")
check "Flag 3" "SecurinetsENIT{r34l_d3l3g4710n_w0rk5}" "$OUT"
echo

# Flag 4 — BIND TXT
printf "${YELLOW}[4/6]${NC} Flag 4 — nsec_walk_leak (authoritative TXT)\n"
OUT=$(dig +short TXT "_flag4.${SUBDOMAIN}" "@${NS1}")
check "Flag 4" "SecurinetsENIT{n53c_w4lk_l34k}" "$OUT"
echo

# Flag 5 — AXFR
printf "${YELLOW}[5/6]${NC} Flag 5 — axfr_dump_success (zone transfer)\n"
OUT=$(dig "@${NS1}" AXFR "$SUBDOMAIN" 2>/dev/null)
check "Flag 5" "SecurinetsENIT{4xfr_dump_5ucc355}" "$OUT"
echo

# Flag 6 — BIND TXT
printf "${YELLOW}[6/6]${NC} Flag 6 — www_chain_followed (authoritative TXT)\n"
OUT=$(dig +short TXT "_www.${SUBDOMAIN}" "@${NS1}")
check "Flag 6" "SecurinetsENIT{www_ch41n_f0ll0w3d}" "$OUT"
echo

# ---------- Summary ----------
echo "=================================================="
printf " Results: ${GREEN}%d passed${NC}  ${RED}%d failed${NC}  (total %d)\n" \
    "$PASS" "$FAIL" "$((PASS + FAIL))"
echo "=================================================="

if [ "$FAIL" -eq 0 ]; then
    exit 0
else
    exit 1
fi
