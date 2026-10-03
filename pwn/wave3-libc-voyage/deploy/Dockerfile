FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat gcc make && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf

WORKDIR /home/ctf

COPY src/libc_voyage.c .
COPY src/Makefile .
RUN make && chmod 755 libc_voyage

COPY deploy/flag.txt .
RUN chown -R root:root /home/ctf && \
    chmod 755 /home/ctf && \
    chmod 755 /home/ctf/libc_voyage && \
    chmod 444 /home/ctf/flag.txt

USER ctf
EXPOSE 1344

CMD ["socat", "-T30", "TCP-LISTEN:1344,reuseaddr,fork", "EXEC:/home/ctf/libc_voyage"]
