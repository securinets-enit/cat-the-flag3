# Hints · 01 fopen-lfi

**Hint 1 (free):** The URL picks *which file* the page shows. What if you asked
for a file that isn't an article?

**Hint 2:** The app reads `pages/<your input>`. There's no filter on `../`.

**Hint 3:** The flag isn't in the web folder. Climb up with `../` until you hit
the filesystem root, then grab `flag.txt`.

**Solution:** `?page=../../../../../flag.txt`
