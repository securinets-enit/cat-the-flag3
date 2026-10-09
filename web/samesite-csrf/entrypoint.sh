#!/bin/sh
# Lock egress so an XSS running as admin cannot exfiltrate the flag; needs NET_ADMIN.
set -e

if ! iptables -A OUTPUT -d 127.0.0.11 -j DROP 2>/dev/null; then
  echo "[entrypoint] FATAL: cannot set iptables (need cap_add: NET_ADMIN)." >&2
  exit 1
fi
iptables -A OUTPUT -p udp --dport 53 -j DROP
iptables -A OUTPUT -p tcp --dport 53 -j DROP
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -j DROP
echo "[entrypoint] egress locked: no DNS, loopback + established only"

exec gosu node node server.js
