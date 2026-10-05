#!/usr/bin/env bash
#
# solve-enitt.sh — verify all 9 ENIT Impersonation flags from a remote host.
#

set -u

DOMAIN="enitt.online"

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
echo " ENIT Impersonation — Remote Flag Verification"
echo " Target: ${DOMAIN}"
echo "=================================================="
echo

# ---------- Flag 1 ----------
printf "${YELLOW}[1/9]${NC} basic_dns_recon\n"
OUT=$(dig +short TXT "_verify.${DOMAIN}" @1.1.1.1)
check "Flag 1" "SecurinetsENIT{b451c_dn5_r3c0n}" "$OUT"
echo

# ---------- Flag 2 ----------
printf "${YELLOW}[2/9]${NC} mail_policy_weak (inside DMARC rua)\n"
OUT=$(dig +short TXT "_dmarc.${DOMAIN}" @1.1.1.1)
check "Flag 2" "SecurinetsENIT{m41l_p0l1cy_w34k}" "$OUT"
echo

# ---------- Flag 3 ----------
printf "${YELLOW}[3/9]${NC} subdomain_hunt_complete\n"
OUT=$(dig +short TXT "_acme-challenge.${DOMAIN}" @1.1.1.1)
check "Flag 3" "SecurinetsENIT{5ubd0m41n_hun7_c0mpl3t3}" "$OUT"
echo

# ---------- Flag 4 ----------
printf "${YELLOW}[4/9]${NC} mx_hidden\n"
OUT=$(dig +short TXT "mail.${DOMAIN}" @1.1.1.1)
check "Flag 4" "SecurinetsENIT{mx_h1dd3n}" "$OUT"
echo

# ---------- Flag 5 ----------
printf "${YELLOW}[5/9]${NC} cname_chain\n"
OUT=$(dig +short TXT "final.${DOMAIN}" @1.1.1.1)
check "Flag 5" "SecurinetsENIT{cn4m3_ch41n}" "$OUT"
echo

# ---------- Flag 6 ----------
printf "${YELLOW}[6/9]${NC} srv_record_pivot\n"
OUT=$(dig +short TXT "auth.${DOMAIN}" @1.1.1.1)
check "Flag 6" "SecurinetsENIT{5rv_r3c0rd_p1v07}" "$OUT"
echo

# ---------- Flag 7 ----------
printf "${YELLOW}[7/9]${NC} caa_authority_limited\n"
OUT=$(dig +short TXT "_caa.${DOMAIN}" @1.1.1.1)
check "Flag 7" "SecurinetsENIT{c44_4u7h0r17y_l1m173d}" "$OUT"
echo

# ---------- Flag 8 ----------
printf "${YELLOW}[8/9]${NC} dnssec_not_enabled\n"
OUT=$(dig +short TXT "_dnssec.${DOMAIN}" @1.1.1.1)
check "Flag 8" "SecurinetsENIT{dn55ec_n07_3n4bl3d}" "$OUT"
echo

# ---------- Flag 9 ----------
printf "${YELLOW}[9/9]${NC} zone_transfer_blocked\n"
OUT=$(dig +short TXT "_axfr.${DOMAIN}" @1.1.1.1)
check "Flag 9" "SecurinetsENIT{20n3_7r4n5f3r_bl0ck3d}" "$OUT"
echo

echo "=================================================="
printf " Results: ${GREEN}%d passed${NC}  ${RED}%d failed${NC}  (total %d)\n" \
    "$PASS" "$FAIL" "$((PASS + FAIL))"
echo "=================================================="

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
