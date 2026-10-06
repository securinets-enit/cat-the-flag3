# WWE Smackdown: Ring of Chaos

Welcome to the main event! The crowd is roaring, the champion is waiting, and the ring is yours. But watch out—the boundaries of the ring are a bit loose, and the ref isn't paying close attention.

## Deployment

Build the challenge binary locally with:

```bash
make
```

To build and start the challenge locally, simply run:

```bash
docker-compose up --build
```

You can then connect to the challenge using netcat:

```bash
nc localhost 1337
```

## Objective

Exploit the application to read the contents of `flag.txt`. Good luck in the ring!
