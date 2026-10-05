#!/bin/bash
# Build the sysdiag image with all layers and flags
# Author: 7ankalis — Securinets ENIT

set -e

IMAGE="sitaha/sysdiag:3.1.2"
DIAG_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[*] Building diag binary"
cd "$DIAG_DIR/diag"

if ! command -v gcc >/dev/null 2>&1; then
    echo "[!] gcc not found. Install it first:"
    echo "    Debian/Ubuntu: sudo apt-get install gcc"
    echo "    macOS:         xcode-select --install"
    exit 1
fi

gcc -O2 -s -w -o diag diag.c

echo "[+] diag binary built: $(file diag)"
echo "[*] Size: $(ls -lh diag | awk '{print $5}')"

cd "$DIAG_DIR"

echo
echo "[*] Building $IMAGE"
docker build -t "$IMAGE" .

echo
echo "[*] Verifying layers"
docker history --no-trunc "$IMAGE" | head -20

echo
echo "[*] Verifying labels"
docker inspect "$IMAGE" --format '{{json .Config.Labels}}' | jq .

echo
echo "[+] Build complete."
