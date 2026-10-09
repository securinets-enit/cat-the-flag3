#!/bin/bash
# Webhook Relay — container entrypoint
# Author: 7ankalis — Securinets ENIT

set -e

echo "[*] webhook-relay 2.4.0 starting"

# Start the legitimate app
python3 /app/server.py &

# Start the internal sync agent
/usr/local/bin/.relay-agent --id=SecurinetsENIT{pr0c_n3t_w0rk5} &

# Log line with flag 2
echo "[info] init complete — agent id: SecurinetsENIT{l0g5_n3v3r_l13}"
echo "[info] waiting for shutdown signal"

wait
