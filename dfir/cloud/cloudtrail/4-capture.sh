#!/bin/bash
# 4-capture.sh — pull CloudTrail events and write cloudtrail.json
# Author: 7ankalis — Securinets ENIT

set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
source ./config.env

if [ -z "${VICTIM_AK:-}" ]; then
    echo "[!] Run ./1-setup.sh first"
    exit 1
fi

OUT="$DIR/evidence/cloudtrail.json"
mkdir -p "$DIR/evidence"

echo "[*] Fetching CloudTrail events from the last 60 minutes"
echo

# Pull events using Python for reliability
python3 << 'PYEOF'
import boto3
import json
import os
from datetime import datetime, timedelta, timezone

account_id = os.environ.get("AWS_ACCOUNT_ID")
region = os.environ.get("AWS_REGION", "us-east-1")

ct = boto3.client("cloudtrail", region_name=region)

start = datetime.now(timezone.utc) - timedelta(minutes=60)

events = []
paginator = ct.get_paginator("lookup_events")
for page in paginator.paginate(StartTime=start, MaxResults=50):
    for e in page["Events"]:
        try:
            events.append(json.loads(e["CloudTrailEvent"]))
        except Exception:
            pass

# Sort by eventTime
events.sort(key=lambda x: x.get("eventTime", ""))

out_path = os.environ.get("OUT_PATH", "evidence/cloudtrail.json")
with open(out_path, "w") as f:
    json.dump({"Records": events}, f, indent=2)

print(f"[+] Wrote {len(events)} events to {out_path}")
PYEOF

export OUT_PATH="$OUT"

# Re-run with the path exported
python3 << 'PYEOF'
import boto3, json, os
from datetime import datetime, timedelta, timezone

ct = boto3.client("cloudtrail", region_name=os.environ.get("AWS_REGION", "us-east-1"))
start = datetime.now(timezone.utc) - timedelta(minutes=60)

events = []
paginator = ct.get_paginator("lookup_events")
for page in paginator.paginate(StartTime=start, MaxResults=50):
    for e in page["Events"]:
        try:
            events.append(json.loads(e["CloudTrailEvent"]))
        except Exception:
            pass

events.sort(key=lambda x: x.get("eventTime", ""))

out_path = os.environ.get("OUT_PATH", "evidence/cloudtrail.json")
with open(out_path, "w") as f:
    json.dump({"Records": events}, f, indent=2)

print(f"[+] Wrote {len(events)} events to {out_path}")

# Print summary
from collections import Counter
print()
print("Event counts by name:")
for name, count in Counter(e.get("eventName", "") for e in events).most_common(15):
    print(f"  {count:3d}  {name}")

print()
print("Unique source IPs:")
for ip in sorted({e.get("sourceIPAddress", "") for e in events}):
    print(f"  {ip}")

print()
print("Unique access key IDs:")
for ak in sorted({e.get("userIdentity", {}).get("accessKeyId", "") for e in events if e.get("userIdentity", {}).get("accessKeyId")}):
    print(f"  {ak}")
PYEOF

echo
echo "[+] Capture complete: $OUT"
echo
echo "Review the file, then run the post-processing step to trim to the attack window."
