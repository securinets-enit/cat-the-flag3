# Docker Basics

**Difficulty:** Easy
**Category:** Containers
**Author:** 7ankalis — Securinets ENIT
**Points:** 300

## Brief

A suspicious container image was found on a compromised server. Before
you can analyze it, you need to understand how Docker works.

Pull and run the tutorial image:

    docker pull sitaha/docker-basics:1.0
    docker run -it --rm sitaha/docker-basics:1.0

The container will guide you through the fundamentals. Three flags are
hidden along the way.

## Prerequisites

- Docker installed

## Flag format

    SecurinetsENIT{...}

## Hints

- Some files are hidden
- Environment variables are per-container
- Image metadata is visible from the host
