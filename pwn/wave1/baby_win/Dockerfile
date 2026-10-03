FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/ctf ctf
WORKDIR /home/ctf

COPY chall ./chall
COPY flag.txt ./flag.txt

RUN chmod 755 ./chall && \
    chmod 644 ./flag.txt

# Players only ever get a raw socket to the binary (no shell), so the
# only path to flag.txt is through win()'s fopen() inside the program.
USER ctf

EXPOSE 5000
CMD ["socat", "-T30", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:./chall,pty,echo=0,stderr"]