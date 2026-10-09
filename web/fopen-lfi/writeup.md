# 01 · fopen-lfi (easy)

A news site renders articles with `?page=about`, which the app turns into
`pages/about.php` and includes. The filename is attacker-controlled.

## Vulnerability
`index.php` builds the include path by concatenating the `page` parameter with no
sanitisation:

```php
$path = "pages/" . $_GET['page'] . ".php";
@include $path;
```

The trailing `.php` is appended, so a plain traversal to `flag.txt` won't resolve
— but the `php://filter` wrapper reads a file and base64-encodes it, and the
appended `.php` just becomes part of the resource name.

## Exploitation
Read the source of `index.php` through the filter wrapper:

```
GET /?page=php://filter/convert.base64-encode/resource=index
```

Base64-decode the response to recover the source, which contains the flag.

## Flag
```
SecurinetsENIT{tr4v3rs4l_1s_th3_d00r_y0u_alw4ys_kn0ck}
```

## Fix
Map a fixed allow-list of article names to files, or `realpath()` the resolved
path and reject anything outside `pages/`.
