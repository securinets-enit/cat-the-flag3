# Task 1 — The Bait

Difficulty: Easy
Category: Browser Forensics
Flag: SecurinetsENIT{aa24756f4410809ecc650d58404ee1f7}

## Scenario

At 14:22 UTC, the SOC flagged unusual outbound traffic from workstation-04. The user is a developer who mentioned downloading a GitHub CLI update earlier in the day.

## Evidence

- places.sqlite — Firefox browsing history
- downloads.sqlite — Firefox downloads
- page.html — saved copy of the download page

## Walkthrough

### Step 1 — Extract the visited URL

Open the Firefox history database:

    sqlite3 places.sqlite "SELECT url, datetime(last_visit_date/1000000,'unixepoch') FROM moz_places WHERE url LIKE '%cdnjs%';"

You get two rows:

    https://cdnjs-mirror.net/                                        2026-10-04 14:22:05
    https://cdnjs-mirror.net/downloads/gh_2.42.1_linux_amd64.tar.gz  2026-10-04 14:22:31

### Step 2 — Check the downloads table

    sqlite3 downloads.sqlite "SELECT source, target FROM moz_downloads;"

Confirms the tarball landed in the user's Downloads folder.

### Step 3 — Inspect the saved page

Open page.html. Scroll to the Checksums block:

    SecurinetsENIT{aa24756f4410809ecc650d58404ee1f7}  gh_2.42.1_linux_amd64.tar.gz
    b4e6d9eae2c3a5b7d8e9f0a1b2c3d4e5                gh_2.42.1_windows_amd64.zip
    c5f7eafbf3d4b6c8e9f0a1b2c3d4e5f6                gh_2.42.1_darwin_amd64.tar.gz

The first one is not a valid MD5. That is the flag.

## Flag

SecurinetsENIT{aa24756f4410809ecc650d58404ee1f7}

## What you learn

- Firefox stores history in places.sqlite
- moz_places holds the URLs, moz_historyvisits holds timestamps
- Downloads are in downloads.sqlite
- Published checksums are untrusted — always verify against the actual file

## MITRE

T1566 — Phishing
T1204.002 — User Execution: Malicious File
