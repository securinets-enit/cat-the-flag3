# Hints · 06 upload-htaccess

**Hint 1 (free):** The uploader blocks `.php`, `.phtml`, etc. — but it uses a
**blacklist** of extensions. What files that aren't on the list can still change
how the server behaves?

**Hint 2:** Apache reads a per-directory config file if `AllowOverride` permits.
That filename isn't a "PHP" extension, so the blacklist lets it through. Map an
innocent extension to the PHP handler: `AddType application/x-httpd-php .xyz`.

**Hint 3:** Now try to upload your `shell.xyz` webshell — it gets rejected even
though the extension is fine. The server also **reads the file contents** and
blocks anything containing `<?php`. The extension filter was only the first gate.

**Hint 4:** `<?php` is not the only way to open a PHP block. PHP 8 always enables
the **short echo tag** `<?=`, regardless of `short_open_tag`. It never contains
the string `<?php`, so it sails past the content filter:
`<?=shell_exec($_GET['c'])?>`. Upload that as `shell.xyz` and request
`/uploads/shell.xyz?c=cat /flag.txt`.
