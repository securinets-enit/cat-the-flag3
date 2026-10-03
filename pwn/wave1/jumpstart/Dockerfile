FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat gcc make && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf

WORKDIR /home/ctf

COPY jumpstart.c .
COPY Makefile .
RUN make && chmod 755 jumpstart

COPY flag.txt .
RUN chown -R root:root /home/ctf && \
    chmod 755 /home/ctf && \
    chmod 755 /home/ctf/jumpstart && \
    chmod 444 /home/ctf/flag.txt

USER ctf
EXPOSE 1338

CMD ["socat", "-T30", "TCP-LISTEN:1338,reuseaddr,fork", "EXEC:/home/ctf/jumpstart"]
