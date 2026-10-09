# Container series

Three independent Docker-forensics images, increasing difficulty.

| # | Dir | Image | Flags |
|---|---|---|---|
| 1 | `01-docker-basics` | sitaha/docker-basics:1.0 | 3 |
| 2 | `02-sysdiag` | sitaha/sysdiag:3.1.2 | 5 |
| 3 | `03-webhook-relay` | sitaha/webhook-relay:2.4.0 | 5 |

    ./0N-*/build.sh      # build one
    ./0N-*/solver.sh     # verify flags (02, 03)
    make -C .. build-containers

Players pull the images from Docker Hub; nothing is hosted here.
