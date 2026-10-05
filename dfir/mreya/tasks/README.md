# gh-cli-supply-chain

A four-part DFIR challenge. A developer downloaded what looked like a GitHub
CLI update from `cdnjs-mirror.net`. Trace the intrusion from browser history
to network capture.

## Tasks

| # | Name | Focus |
|---|---|---|
| 1 | The Bait | Browser forensics |
| 2 | The Recon | Domain intelligence |
| 3 | The Dropper | Installer analysis |
| 4 | The Implant | Binary + network forensics |

## Running

    docker compose run --rm task-01
    docker compose run --rm task-02
    docker compose run --rm task-03
    docker compose run --rm task-04

Flag format: `SecurinetsENIT{...}`
