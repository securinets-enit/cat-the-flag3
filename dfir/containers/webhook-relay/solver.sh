#!/usr/bin/env bash
set -u

IMAGE="sitaha/webhook-relay:2.4.0"
NAME="wr-solve-$$"

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
        printf "${GREEN}[PASS]${NC} %s\n       %s\n" "$label" "$expected"
        PASS=$((PASS + 1))
    else
        printf "${RED}[FAIL]${NC} %s\n       expected: %s\n       got:      %s\n" "$label" "$expected" "${got:-<empty>}"
        FAIL=$((FAIL + 1))
    fi
}

echo "=================================================="
echo " Runtime Forensics — Flag Verification"
echo " Image: $IMAGE"
echo "=================================================="
echo

docker rm -f "$NAME" >/dev/null 2>&1 || true

printf "${BLUE}[*]${NC} Starting container\n"
docker run -d --name "$NAME" -p 0:8080 "$IMAGE" >/dev/null
sleep 3

# Flag 1
printf "${YELLOW}[1/5]${NC} Flag 1 — 3nv_1n5p3c7_5h0w5_4ll\n"
OUT=$(docker inspect "$NAME" --format '{{json .Config.Env}}')
check "Flag 1" "SecurinetsENIT{3nv_1n5p3c7_5h0w5_4ll}" "$OUT"
echo

# Flag 2
printf "${YELLOW}[2/5]${NC} Flag 2 — l0g5_n3v3r_l13\n"
OUT=$(docker logs "$NAME" 2>&1)
check "Flag 2" "SecurinetsENIT{l0g5_n3v3r_l13}" "$OUT"
echo

# Flag 3
printf "${YELLOW}[3/5]${NC} Flag 3 — c2_c0nf1g_3xp053d\n"
OUT=$(docker exec "$NAME" cat /etc/relay.conf 2>&1)
check "Flag 3" "SecurinetsENIT{c2_c0nf1g_3xp053d}" "$OUT"
echo

# Flag 4
printf "${YELLOW}[4/5]${NC} Flag 4 — cr0n_p3r51573nc3_f0und\n"
OUT=$(docker exec "$NAME" cat /etc/cron.d/webhook-sync 2>&1)
check "Flag 4" "SecurinetsENIT{cr0n_p3r51573nc3_f0und}" "$OUT"
echo

# Flag 5
printf "${YELLOW}[5/5]${NC} Flag 5 — pr0c_n3t_w0rk5\n"
OUT=$(docker exec "$NAME" ps aux 2>&1)
check "Flag 5" "SecurinetsENIT{pr0c_n3t_w0rk5}" "$OUT"
echo

docker rm -f "$NAME" >/dev/null 2>&1 || true

echo "=================================================="
printf " Results: ${GREEN}%d passed${NC}  ${RED}%d failed${NC}  (total %d)\n" \
    "$PASS" "$FAIL" "$((PASS + FAIL))"
echo "=================================================="

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
