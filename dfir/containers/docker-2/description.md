# Image Forensics

**Difficulty:** Medium
**Category:** Container Forensics
**Author:** 7ankalis — Securinets ENIT
**Points:** 500 (5 flags, 100 each)

## Brief

A suspicious image was pulled on a compromised server:

    sitaha/sysdiag:3.1.2

The image presents itself as a system diagnostics tool. It is not.

Analyze the image **statically** — without running it. Five flags are
hidden in the image's layers, metadata, and filesystem.

## Objectives

1. Read the image's build history
2. Inspect image metadata and labels
3. Extract the image tar and analyze individual layers
4. Recover files that were deleted in later layers
5. Extract the embedded binary and inspect it

## Tools

    docker history
    docker inspect
    docker save
    tar
    strings
    jq

## Hints

- The image is not the container
- Every RUN command creates a layer
- "Deleted" files are not really gone
- Binaries contain more than they print

## Flag format

    SecurinetsENIT{...}
