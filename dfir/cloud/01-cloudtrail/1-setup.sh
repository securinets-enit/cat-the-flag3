#!/bin/bash
# 1-setup.sh — create the AWS infrastructure for the cloud forensics task
# Author: 7ankalis — Securinets ENIT

set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
source ./config.env

echo "=================================================="
echo " Cloud Forensics — Infrastructure Setup"
echo "=================================================="
echo

# ---------------------------------------------------------------
# 1. Clean up any leftover victim user
# ---------------------------------------------------------------
echo "[*] Cleaning up any leftover 'samir.benali' or 'dev-jdoe'"
aws iam delete-user-policy --user-name "$VICTIM_USER" --policy-name "$VICTIM_POLICY_NAME" 2>/dev/null || true
aws iam list-access-keys --user-name "$VICTIM_USER" 2>/dev/null | \
    jq -r '.AccessKeyMetadata[].AccessKeyId' 2>/dev/null | while read -r key; do
    [ -n "$key" ] && aws iam delete-access-key --user-name "$VICTIM_USER" --access-key-id "$key" || true
done
aws iam delete-user --user-name "$VICTIM_USER" 2>/dev/null || true

# ---------------------------------------------------------------
# 2. Create the victim user
# ---------------------------------------------------------------
echo "[*] Creating victim user: $VICTIM_USER"
aws iam create-user --user-name "$VICTIM_USER" >/dev/null
echo "    [+] User created"

# ---------------------------------------------------------------
# 3. Create an access key for the victim
# ---------------------------------------------------------------
echo "[*] Creating access key for $VICTIM_USER"
KEY_JSON=$(aws iam create-access-key --user-name "$VICTIM_USER")
VICTIM_AK=$(echo "$KEY_JSON" | jq -r '.AccessKey.AccessKeyId')
VICTIM_SK=$(echo "$KEY_JSON" | jq -r '.AccessKey.SecretAccessKey')
echo "    [+] Access key ID: $VICTIM_AK"

# ---------------------------------------------------------------
# 4. Create the S3 buckets
# ---------------------------------------------------------------
SUFFIX=$(date +%s)
BUCKET_INTERNAL="${BUCKET_INTERNAL_PREFIX}-${SUFFIX}"
BUCKET_SOURCE="${BUCKET_SOURCE_PREFIX}-${SUFFIX}"

echo "[*] Creating buckets"
aws s3 mb "s3://${BUCKET_INTERNAL}" --region "$AWS_REGION" >/dev/null
aws s3 mb "s3://${BUCKET_SOURCE}" --region "$AWS_REGION" >/dev/null
echo "    [+] $BUCKET_INTERNAL"
echo "    [+] $BUCKET_SOURCE"

# ---------------------------------------------------------------
# 5. Create the privileged role
# ---------------------------------------------------------------
echo "[*] Creating role: $ROLE_NAME"

cat > /tmp/trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::${AWS_ACCOUNT_ID}:user/${VICTIM_USER}"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Delete leftover role if it exists
aws iam detach-role-policy --role-name "$ROLE_NAME" \
    --policy-arn arn:aws:iam::aws:policy/AdministratorAccess 2>/dev/null || true
aws iam delete-role --role-name "$ROLE_NAME" 2>/dev/null || true

aws iam create-role \
    --role-name "$ROLE_NAME" \
    --assume-role-policy-document file:///tmp/trust-policy.json >/dev/null

aws iam attach-role-policy \
    --role-name "$ROLE_NAME" \
    --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

echo "    [+] Role created with AdministratorAccess"

# ---------------------------------------------------------------
# 6. Give the victim permission to assume the role
# ---------------------------------------------------------------
cat > /tmp/user-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::${AWS_ACCOUNT_ID}:role/${ROLE_NAME}"
    }
  ]
}
EOF

aws iam put-user-policy \
    --user-name "$VICTIM_USER" \
    --policy-name "$VICTIM_POLICY_NAME" \
    --policy-document file:///tmp/user-policy.json >/dev/null

echo "    [+] Inline policy attached to $VICTIM_USER"

# ---------------------------------------------------------------
# 7. Save state
# ---------------------------------------------------------------
cat > "$DIR/.state" << EOF
export SUFFIX="$SUFFIX"
export BUCKET_INTERNAL="$BUCKET_INTERNAL"
export BUCKET_SOURCE="$BUCKET_SOURCE"
export VICTIM_AK="$VICTIM_AK"
export VICTIM_SK="$VICTIM_SK"
EOF

chmod 600 "$DIR/.state"

echo
echo "=================================================="
echo " Setup complete"
echo "=================================================="
echo
echo "Summary:"
echo "  Account ID:      $AWS_ACCOUNT_ID"
echo "  Victim user:     $VICTIM_USER"
echo "  Victim key:      $VICTIM_AK"
echo "  Role:            $ROLE_NAME"
echo "  Bucket internal: $BUCKET_INTERNAL"
echo "  Bucket source:   $BUCKET_SOURCE"
echo
echo "Next: ./2-upload-files.sh"
# Create a decoy "backup-service" user the attacker will backdoor
aws iam delete-user --user-name backup-service 2>/dev/null || true
aws iam create-user --user-name backup-service >/dev/null
# Ensure a trail exists so the cover-up attempt is realistic
if ! aws cloudtrail get-trail --name management-events --region "$AWS_REGION" >/dev/null 2>&1; then
    aws cloudtrail create-trail \
        --name management-events \
        --s3-bucket-name "${BUCKET_SOURCE}" \
        --is-multi-region-trail \
        --region "$AWS_REGION"
    aws cloudtrail start-logging --name management-events --region "$AWS_REGION"
fi
