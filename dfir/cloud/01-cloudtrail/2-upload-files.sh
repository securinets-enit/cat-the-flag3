#!/bin/bash
# 2-upload-files.sh — upload decoy files to the buckets
# Author: 7ankalis — Securinets ENIT

set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
source ./config.env

if [ -z "${BUCKET_INTERNAL:-}" ]; then
    echo "[!] Run ./1-setup.sh first"
    exit 1
fi

echo "[*] Creating decoy files in /tmp"

# Replace these with your real files if you want
cat > /tmp/q4-forecast-2026.xlsx << 'EOF'
Q4 2026 Forecast - Confidential
Not for external distribution.
Author: 7ankalis — Securinets ENIT
EOF

cat > /tmp/employee-salary-data.csv << 'EOF'
employee_id,name,salary,department
EMP001,Samir Benali,85000,Engineering
EMP002,Ahmed Trabelsi,72000,Sales
EMP-CONFIDENTIAL-DO-NOT-DISTRIBUTE,,,
EOF

cat > /tmp/main.zip << 'EOF'
Fake backend archive — placeholder for CTF
Author: 7ankalis — Securinets ENIT
EOF

cat > /tmp/database-config.json << 'EOF'
{
  "db_host": "prod-db.internal",
  "db_name": "securinets_prod",
  "db_user": "app_user",
  "db_password": "placeholder-do-not-use",
  "author": "7ankalis — Securinets ENIT"
}
EOF

echo "[*] Uploading to buckets"

aws s3 cp /tmp/q4-forecast-2026.xlsx "s3://${BUCKET_INTERNAL}/finance/q4-forecast-2026.xlsx"
aws s3 cp /tmp/employee-salary-data.csv "s3://${BUCKET_INTERNAL}/hr/employee-salary-data.csv"
aws s3 cp /tmp/main.zip "s3://${BUCKET_SOURCE}/backend/main.zip"
aws s3 cp /tmp/database-config.json "s3://${BUCKET_SOURCE}/backend/database-config.json"

echo
echo "[+] Files uploaded:"
echo "    s3://${BUCKET_INTERNAL}/finance/q4-forecast-2026.xlsx"
echo "    s3://${BUCKET_INTERNAL}/hr/employee-salary-data.csv"
echo "    s3://${BUCKET_SOURCE}/backend/main.zip"
echo "    s3://${BUCKET_SOURCE}/backend/database-config.json"
echo
echo "Next: ./3-attack.sh"
