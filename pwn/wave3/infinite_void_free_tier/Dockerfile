FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat gcc make && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf

WORKDIR /home/ctf

COPY main.c .
COPY Makefile .
RUN make && chmod 755 main

COPY flag.txt /flag
RUN chown root:root /flag && \
    chmod 444 /flag && \
    chown -R root:root /home/ctf && \
    chmod 755 /home/ctf && \
    chmod 755 /home/ctf/main

USER ctf
EXPOSE 1351

CMD ["socat", "-T4", "TCP-LISTEN:1351,reuseaddr,fork", "EXEC:/home/ctf/main"]
