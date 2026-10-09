# Hints · 08 prepared-sqli

**Hint 1 (free):** This is white-box — grab `/source.zip` and read it. The app
uses PDO prepared statements. Look closely at *what* is parameterized and what
isn't.

**Hint 2:** Every user *value* (the search term, the `active` flag) is bound with
a `?` placeholder, so those are safe. But a prepared statement can only bind a
value — it can't bind a column name or sort direction. Where does the app build
part of the query from `$_GET` by string concatenation?

**Hint 3:** The `ORDER BY` clause is `"... ORDER BY $sort $dir"` with `?sort=` and
`?dir=` dropped in raw. That's your injection point. Confirm it: compare
`?sort=title` with `?sort=(select 1)` and with something invalid — the page
prints the database error.

**Hint 4:** You can't `UNION` inside `ORDER BY`, so go error-based. `updatexml()`
throws an XPATH error containing a string you control:
```
?sort=updatexml(1,concat(0x7e,(select secret from internal_notes)),1)&dir=
```

**Hint 5:** The `updatexml`/`extractvalue` error is truncated to 32 characters, so
you'll only see the first part of the flag. Read it in slices with `SUBSTRING`
and concatenate:
```
?sort=updatexml(1,concat(0x7e,substring((select secret from internal_notes),1,25)),1)&dir=
?sort=updatexml(1,concat(0x7e,substring((select secret from internal_notes),26,25)),1)&dir=
```
