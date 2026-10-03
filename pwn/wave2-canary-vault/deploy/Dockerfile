FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat gcc make && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf

WORKDIR /home/ctf

COPY src/canary_vault.c .
COPY src/Makefile .
RUN make && chmod 755 canary_vault

COPY deploy/flag.txt .
RUN chown -R root:root /home/ctf && \
    chmod 755 /home/ctf && \
    chmod 755 /home/ctf/canary_vault && \
    chmod 444 /home/ctf/flag.txt

USER ctf
EXPOSE 1342

CMD ["socat", "-T30", "TCP-LISTEN:1342,reuseaddr,fork", "EXEC:/home/ctf/canary_vault"]
