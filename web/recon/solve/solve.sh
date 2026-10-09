#!/usr/bin/env bash
# 00 · recon reference solver
# Usage: ./solve.sh http://TARGET:PORT
set -euo pipefail
BASE="${1:?usage: solve.sh http://host:port}"

echo "[*] The home page comment points at robots.txt. Read it:"
curl -s "${BASE}/robots.txt"

echo "[*] Follow the Disallow'd path:"
curl -s "${BASE}/internal-notes-9f2a1c/notes.txt" | grep -oE 'SecurinetsENIT\{[^}]+\}'
