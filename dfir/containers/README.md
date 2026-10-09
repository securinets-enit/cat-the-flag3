# Container series

Three independent Docker-forensics images, increasing difficulty.

| # | Dir | Image | Flags |
|---|---|---|---|
| 1 | `01-docker-basics` | securinets-enit/docker-basics:1.0 | 3 |
| 2 | `02-sysdiag` | sitaha/sysdiag:3.1.2 | 5 |
| 3 | `03-webhook-relay` | sitaha/webhook-relay:2.4.0 | 5 |

Image names are the ones each `build.sh` tags (the solvers use the same names).

    cd 0N-*/ && ./build.sh    # build one (run it from inside its folder)
    cd 0N-*/ && ./solver.sh   # verify its flags against the local image (02, 03 only)
    make -C .. build-containers   # build all three
    make -C .. test-containers    # run the 02 and 03 solvers

Players pull the images from Docker Hub; nothing is hosted here.
