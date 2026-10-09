# DFIR — Cat The Flag 3

Each top-level folder is one **series** that deploys independently.

| Series | What | Deploy |
|---|---|---|
| [`mreya/`](mreya) | gh-cli supply chain, 5 linked tasks | `make up SERIES=mreya` |
| [`cloud/`](cloud) | Leaked AWS key, 2 linked tasks | `make up SERIES=cloud` |
| [`dns/`](dns) | Domain impersonation + DNS revenge | Cloudflare/BIND (no containers) |
| [`containers/`](containers) | 3 Docker forensics images | `make build-containers` |
| [`npm-supply-chain/`](npm-supply-chain) | The Merge (live C2) | see its README |
| [`docs/`](docs) | Author-side infrastructure reference | — |

`make up` starts every compose-based series; `make down`, `make ps` likewise.

## Conventions

Every task folder follows the same shape (only what applies):

    NN-name/
      README.md        player-facing brief
      WALKTHROUGH.md   author solution (contains flags — keep repo private)
      asker/           Dockerfile + asker.go + flag.txt (TCP question server)
      evidence/        handout files
      solver.sh        automated verification

Numeric prefixes give the order within a series. Ports: 9999-9996 mreya, 9995-9994 cloud.
