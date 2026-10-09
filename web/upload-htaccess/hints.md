# Hints · 06 upload-htaccess

**Hint 1 (free):** The uploader blocks `.php`, `.phtml`, etc. — but it uses a
**blacklist** of extensions. What files that aren't on the list can still change
how the server behaves?

**Hint 2:** Apache reads a per-directory config file if `AllowOverride` permits.
That filename isn't a "PHP" extension, so the blacklist lets it through.

**Hint 3:** Upload a `.htaccess` that maps an innocent extension to the PHP
handler: `AddType application/x-httpd-php .jpg`.

**Hint 4:** Then upload `shell.jpg` containing `<?php system($_GET['c']); ?>` and
request `/uploads/shell.jpg?c=cat /flag.txt`.
