# Hints · 04 phar-image

**Hint 1 (free):** Two features matter: an avatar **upload** (GIF only) and a
"check avatar" box that **stats a path you give it**.

**Hint 2:** What does PHP do when a filesystem function (`file_exists`,
`filesize`, `is_file`) is handed a `phar://` path? It parses the archive's
**metadata** — and unserializes it.

**Hint 3:** The app defines classes with magic methods (`__destruct`). If your
phar's metadata is an object graph of those classes, you control what runs when
it deserializes. Look at `gadgets.php` (readable via earlier challenges, or infer
it): `Template -> Renderer -> file_put_contents`.

**Hint 4:** Build a phar with a `GIF89a` stub so the upload filter passes, set its
metadata to `Template{engine: Renderer{out: webshell path, tpl: <?php system... }}`,
upload it, then `?check=phar://uploads/evil.gif/x.txt`. The chain drops a webshell.
