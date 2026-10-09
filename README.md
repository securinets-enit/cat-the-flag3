# cat-the-flag3
Official Cat The Flag CTF Third Edition.

| Category | Folder | Deploy | Ports |
|---|---|---|---|
| DFIR | [`dfir/`](dfir) | `cd dfir && make up` (+ `make build-containers`) | 9994-9999 |
| Threat Intelligence | [`threat-intel/`](threat-intel) | `cd threat-intel && make up` | 5010-5019 |

Each folder has its own README with the full list of `make` targets.

## Testing a deployment

    python3 solvers/solve_askers.py            # play every asker on asker.securinets-enit.club, check each answer + flag
    python3 solvers/solve_askers.py --wrong    # also check that wrong answers are rejected
    python3 solvers/solve_askers.py zebrocy    # only some askers
    python3 solvers/solve_askers.py --list     # show askers/ports found in the repo (no network)

Questions and answers are read from each asker's Go source and ports from its Dockerfile, so new askers are picked up automatically.
