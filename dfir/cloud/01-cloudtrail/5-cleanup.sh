#!/bin/bash
# 5-cleanup.sh — delete all AWS resources created by 1-setup.sh
# Author: 7ankalis — Securinets ENIT

set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
source ./config.env

echo "=================================================="
echo " Cloud Forensics — Cleanup"
echo "=================================================="
echo
echo "This will delete:"
echo "  - Victim user: $VICTIM_USER"
echo "  - Role:        $ROLE_NAME"
echo "  - Buckets:     ${BUCKET_INTERNAL:-<not set>}, ${BUCKET_SOURCE:-<not set>}"
echo
read -p "Continue? [y/N] " confirm
[[ "$confirm" =~ ^[Yy]$ ]] || exit 0

echo
echo "[*] Emptying and deleting buckets"
if [ -n "${BUCKET_INTERNAL:-}" ]; then
    aws s3 rm "s3://${BUCKET_INTERNAL}" --recursive >/dev/null 2>&1 || true
    aws s3 rb "s3://${BUCKET_INTERNAL}" >/dev/null 2>&1 || true
fi
if [ -n "${BUCKET_SOURCE:-}" ]; then
    aws s3 rm "s3://${BUCKET_SOURCE}" --recursive >/dev/null 2>&1 || true
    aws s3 rb "s3://${BUCKET_SOURCE}" >/dev/null 2>&1 || true
fi

echo "[*] Deleting IAM role"
aws iam detach-role-policy --role-name "$ROLE_NAME" \
    --policy-arn arn:aws:iam::aws:policy/AdministratorAccess 2>/dev/null || true
aws iam delete-role --role-name "$ROLE_NAME" 2>/dev/null || true

echo "[*] Deleting victim user"
aws iam delete-user-policy --user-name "$VICTIM_USER" --policy-name "$VICTIM_POLICY_NAME" 2>/dev/null || true
aws iam list-access-keys --user-name "$VICTIM_USER" 2>/dev/null | \
    jq -r '.AccessKeyMetadata[].AccessKeyId' 2>/dev/null | while read -r key; do
    [ -n "$key" ] && aws iam delete-access-key --user-name "$VICTIM_USER" --access-key-id "$key" || true
done
aws iam delete-user --user-name "$VICTIM_USER" 2>/dev/null || true

echo "[*] Removing state file"
rm -f "$DIR/.state"

echo
echo "[+] Cleanup complete."
