# Walkthrough — Task 1

## Step 1 — Browser history

    sqlite3 places.sqlite \
      "SELECT url, datetime(last_visit_date/1000000,'unixepoch') \
       FROM moz_places WHERE url LIKE '%cdnjs%';"

Output:

    https://cdnjs-mirror.net/                                   2026-10-04 14:22:05
    https://cdnjs-mirror.net/downloads/gh_2.42.1_linux_amd64.tar.gz  2026-10-04 14:22:31

## Step 2 — Downloads

    sqlite3 downloads.sqlite \
      "SELECT source, target FROM moz_downloads;"

Confirms the tarball was saved locally.

## Step 3 — Verify checksums

Open `page.html`. The Checksums section lists an MD5 for the linux tarball
that is 32 chars but does not correspond to any real MD5 of the shipped file.
That value is the flag.

## Flag

`SecurinetsENIT{aa24756f4410809ecc650d58404ee1f7}`
