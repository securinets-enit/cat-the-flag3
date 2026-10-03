FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat gcc make && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf

WORKDIR /home/ctf

COPY src/format_oracle.c .
COPY src/Makefile .
RUN make && chmod 755 format_oracle

COPY deploy/flag.txt .
RUN chown -R root:root /home/ctf && \
    chmod 755 /home/ctf && \
    chmod 755 /home/ctf/format_oracle && \
    chmod 444 /home/ctf/flag.txt

USER ctf
EXPOSE 1343

CMD ["socat", "-T30", "TCP-LISTEN:1343,reuseaddr,fork", "EXEC:/home/ctf/format_oracle"]
