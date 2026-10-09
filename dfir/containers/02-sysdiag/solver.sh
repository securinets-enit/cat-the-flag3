#!/usr/bin/env bash
# solver.sh — verify all 5 Image Forensics flags
# Author: 7ankalis — Securinets ENIT
#
# Handles both classic and OCI docker-save formats.

set -u

IMAGE="sitaha/sysdiag:3.1.2"
WORKDIR="/tmp/sysdiag-solve"

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

# Collect layer blobs from either classic or OCI layout
list_layers() {
    local dir="$1"
    # Classic: */layer.tar
    find "$dir" -name "layer.tar" -type f 2>/dev/null
    # OCI: blobs/sha256/*
    find "$dir" -path "*/blobs/sha256/*" -type f 2>/dev/null
}

rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"

echo "=================================================="
echo " Image Forensics — Flag Verification"
echo " Image: $IMAGE"
echo "=================================================="
echo

# ---------- Flag 1 ----------
printf "${YELLOW}[1/5]${NC} Flag 1 — curl_p1p3_4bu53\n"
OUT=$(docker history --no-trunc --format '{{.CreatedBy}}' "$IMAGE")
check "Flag 1" "SecurinetsENIT{curl_p1p3_4bu53}" "$OUT"
echo

# ---------- Flag 2 ----------
printf "${YELLOW}[2/5]${NC} Flag 2 — r3v1510n_fl4g\n"
OUT=$(docker inspect "$IMAGE" --format '{{json .Config.Labels}}')
check "Flag 2" "SecurinetsENIT{r3v1510n_fl4g}" "$OUT"
echo

printf "${BLUE}[*]${NC} Saving image to $WORKDIR/sysdiag.tar\n"
docker save "$IMAGE" -o "$WORKDIR/sysdiag.tar"
cd "$WORKDIR"
mkdir -p extracted
tar xf sysdiag.tar -C extracted
cd extracted

LAYERS=$(list_layers .)

# ---------- Flag 3 ----------
printf "${YELLOW}[3/5]${NC} Flag 3 — d3l373d_l4y3r5\n"
FOUND3=""
for layer in $LAYERS; do
    if tar tf "$layer" 2>/dev/null | grep -q "etc/backup/notes.txt"; then
        CONTENT=$(tar xfO "$layer" etc/backup/notes.txt 2>/dev/null)
        FOUND3="$FOUND3 $CONTENT"
    fi
done
check "Flag 3" "SecurinetsENIT{d3l373d_l4y3r5_r3v34l_4ll}" "$FOUND3"
echo

# ---------- Flag 4 ----------
printf "${YELLOW}[4/5]${NC} Flag 4 — b4ckd00r_u53r_p4sswd\n"
FOUND4=""
for layer in $LAYERS; do
    if tar tf "$layer" 2>/dev/null | grep -qE "(^|/)etc/passwd$"; then
        CONTENT=$(tar xfO "$layer" etc/passwd 2>/dev/null | grep support)
        [ -n "$CONTENT" ] && FOUND4="$FOUND4 $CONTENT"
    fi
done
check "Flag 4" "SecurinetsENIT{b4ckd00r_u53r_p4sswd}" "$FOUND4"
echo

# ---------- Flag 5 ----------
printf "${YELLOW}[5/5]${NC} Flag 5 — 5tr1ng5_1n_b1n4ry\n"
FOUND5=""
for layer in $LAYERS; do
    if tar tf "$layer" 2>/dev/null | grep -q "usr/local/bin/diag"; then
        tar xfO "$layer" usr/local/bin/diag 2>/dev/null > /tmp/diag-binary
        if [ -s /tmp/diag-binary ]; then
            FOUND5=$(strings /tmp/diag-binary | grep "Securinets")
        fi
    fi
done
check "Flag 5" "SecurinetsENIT{5tr1ng5_1n_b1n4ry_n3v3r_l13}" "$FOUND5"
echo

echo "=================================================="
printf " Results: ${GREEN}%d passed${NC}  ${RED}%d failed${NC}  (total %d)\n" \
    "$PASS" "$FAIL" "$((PASS + FAIL))"
echo "=================================================="

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
